import { Observable, forkJoin, of, asyncScheduler } from 'rxjs';
import {
  map,
  mergeMap,
  tap,
  withLatestFrom,
  catchError,
  delay,
} from 'rxjs/operators';

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Effect, Actions, ofType } from '@ngrx/effects';
import { Action, Store } from '@ngrx/store';

import { ApiService } from '../api.service';
import * as fromReports from '../actions/reports';
import * as fromDisplay from '../actions/display-field';
import * as fromFilter from '../actions/filter';
import { IGetRelatedFieldRequest } from '../models/api';
import { State } from '../reducers';
import {
  getEditedReport,
  getSelectedReportId,
  getIsAsyncReport,
} from '../selectors';
import { MatSnackBar } from '@angular/material/snack-bar';
const { ReportActionTypes } = fromReports;

@Injectable()
export class ReportEffects {
  @Effect()
  getReports$: Observable<Action> = this.actions$.pipe(
    ofType(ReportActionTypes.GET_REPORT_LIST),
    mergeMap(() =>
      this.api
        .getReports()
        .pipe(map(reports => new fromReports.SetReportList(reports)))
    )
  );

  constructor(
    private actions$: Actions,
    private store$: Store<State>,
    private api: ApiService,
    private router: Router,
    public snackBar: MatSnackBar
  ) {}

  @Effect()
  getReport$: Observable<Action> = this.actions$.pipe(
    ofType(ReportActionTypes.GET_REPORT),
    map((action: fromReports.GetReport) => action.payload),
    mergeMap(reportId =>
      this.api
        .getReport(reportId)
        .pipe(map(report => new fromReports.GetReportSuccess(report)))
    )
  );

  @Effect()
  loadDisplayFields$ = this.actions$.pipe(
    ofType(
      ReportActionTypes.GET_REPORT_SUCCESS,
      ReportActionTypes.EDIT_REPORT_SUCCESS
    ),
    map(
      (action: fromReports.GetReportSuccess | fromReports.EditReportSuccess) =>
        new fromDisplay.LoadAll(action.payload.displayfield_set)
    )
  );

  @Effect()
  loadFilterFields$ = this.actions$.pipe(
    ofType(
      ReportActionTypes.GET_REPORT_SUCCESS,
      ReportActionTypes.EDIT_REPORT_SUCCESS
    ),
    map(
      (action: fromReports.GetReportSuccess | fromReports.EditReportSuccess) =>
        new fromFilter.LoadAll(action.payload.filterfield_set)
    )
  );

  @Effect()
  getReportSuccess$ = this.actions$.pipe(
    ofType(ReportActionTypes.GET_REPORT_SUCCESS),
    map((action: fromReports.GetReportSuccess) => action.payload),
    mergeMap(report => {
      const request: IGetRelatedFieldRequest = {
        model: report.root_model,
        path: '',
        field: '',
      };
      return forkJoin(
        this.api.getRelatedFields(request),
        this.api.getFields(request)
      ).pipe(
        map(
          ([relatedFields, fields]) =>
            new fromReports.GetReportFieldsSuccess({ relatedFields, fields })
        )
      );
    })
  );

  @Effect()
  getFields$ = this.actions$.pipe(
    ofType(ReportActionTypes.GET_FIELDS),
    map((action: fromReports.GetFields) => action.payload),
    mergeMap(relatedField => {
      const fieldReq: IGetRelatedFieldRequest = {
        model: relatedField.model_id,
        path: relatedField.path,
        field: relatedField.field_name,
      };
      return this.api
        .getFields(fieldReq)
        .pipe(map(fields => new fromReports.GetFieldsSuccess(fields)));
    })
  );

  @Effect()
  getRelatedFields$ = this.actions$.pipe(
    ofType(ReportActionTypes.GET_RELATED_FIELDS),
    map((action: fromReports.GetRelatedFields) => action.payload),
    mergeMap(relatedField => {
      const fieldReq: IGetRelatedFieldRequest = {
        model: relatedField.model_id,
        path: relatedField.path,
        field: relatedField.field_name,
      };
      return this.api.getRelatedFields(fieldReq).pipe(
        map(
          fields =>
            new fromReports.GetRelatedFieldsSuccess({
              parentId: relatedField.id,
              relatedFields: fields,
            })
        )
      );
    })
  );

  @Effect()
  deleteReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.DELETE_REPORT),
    map((action: fromReports.DeleteReport) => action.payload),
    mergeMap(reportId => {
      return this.api
        .deleteReport(reportId)
        .pipe(map(() => new fromReports.DeleteReportSuccess(reportId)));
    })
  );

  @Effect({ dispatch: false })
  deleteReportSuccess$ = this.actions$.pipe(
    ofType(ReportActionTypes.DELETE_REPORT_SUCCESS),
    tap(_ => this.router.navigate(['']))
  );

  @Effect()
  editReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.EDIT_REPORT),
    withLatestFrom(this.store$),
    mergeMap(([_, storeState]) => {
      const editedReport = getEditedReport(storeState);
      return this.api.editReport(editedReport).pipe(
        map(response => new fromReports.EditReportSuccess(response)),
        catchError(error => of(new fromReports.EditReportFailure(error)))
      );
    })
  );

  @Effect()
  generatePreview$ = this.actions$.pipe(
    ofType(ReportActionTypes.GENERATE_PREVIEW),
    withLatestFrom(this.store$),
    mergeMap(([_, storeState]) => {
      const reportId = getSelectedReportId(storeState);
      return this.api
        .generatePreview(reportId)
        .pipe(
          map(response => new fromReports.GeneratePreviewSuccess(response))
        );
    })
  );

  @Effect()
  exportReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.EXPORT_REPORT),
    withLatestFrom(this.store$),
    mergeMap(([action, storeState]: [fromReports.ExportReport, State]) => {
      const reportId = getSelectedReportId(storeState);
      const async = getIsAsyncReport(storeState);
      const type = action.payload;

      if (!async) {
        return Observable.create(observer => {
          observer.next(
            new fromReports.DownloadExportedReport(
              `api/report/${reportId}/download_file/${type}/`
            )
          );
          observer.complete();
        });
      }

      return this.api
        .exportReport({ reportId, type })
        .pipe(
          map(
            ({ task_id }) =>
              new fromReports.CheckExportStatus({ reportId, taskId: task_id })
          )
        );
    })
  );

  @Effect({ dispatch: false })
  downloadExportedReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.DOWNLOAD_EXPORTED_REPORT),
    mergeMap(
      (action: fromReports.DownloadExportedReport) =>
        (window.location.href = action.payload)
    )
  );

  @Effect({ dispatch: false })
  cancelExportReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.CANCEL_EXPORT_REPORT),
    tap(() =>
      this.snackBar.open('Sorry, something went wrong!', '', { duration: 5000 })
    )
  );

  @Effect()
  createReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.CREATE_REPORT),
    map((action: fromReports.CreateReport) => action.payload),
    mergeMap(newReport =>
      this.api.submitNewReport(newReport).pipe(
        map(
          createdReport => new fromReports.CreateReportSuccess(createdReport)
        ),
        catchError(error => of(new fromReports.CreateReportError(error)))
      )
    )
  );

  @Effect()
  createReportSuccess$ = this.actions$.pipe(
    ofType(ReportActionTypes.CREATE_REPORT_SUCCESS),
    map((action: fromReports.CreateReportSuccess) => action.payload.id),
    tap(reportId => this.router.navigate([`/report/${reportId}/`])),
    map(() => new fromReports.ChangeTab(0))
  );

  @Effect({ dispatch: false })
  createReportError$ = this.actions$.pipe(
    ofType(ReportActionTypes.CREATE_REPORT_ERROR),
    tap(error =>
      this.snackBar.open('Invalid report: please reload the page', '', {
        duration: 5000,
      })
    )
  );

  @Effect()
  copyReport$ = this.actions$.pipe(
    ofType(ReportActionTypes.COPY_REPORT),
    map((action: fromReports.CopyReport) => action.payload),
    mergeMap(reportId => this.api.copyReport(reportId)),
    map(createdReport => new fromReports.CreateReportSuccess(createdReport))
  );

  @Effect()
  checkExportStatus$ = ({
    delayTime = 500,
    scheduler = asyncScheduler
  } = {}) => this.actions$.pipe(
    ofType(ReportActionTypes.CHECK_EXPORT_STATUS),
    delay(delayTime, scheduler),
    mergeMap(
      ({ payload: { reportId, taskId } }: fromReports.CheckExportStatus) =>
        this.api.checkStatus({ reportId, taskId }).pipe(
          map(({ state, link }) => {
            if (state === 'SUCCESS') {
              return new fromReports.DownloadExportedReport(link);
            } else if (state === 'FAILURE') {
              return new fromReports.CancelExportReport();
            } else {
              return new fromReports.CheckExportStatus({ reportId, taskId });
            }
          })
        )
    )
  );

}
