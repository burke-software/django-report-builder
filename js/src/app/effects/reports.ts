import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/do';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/withLatestFrom';
import 'rxjs/add/observable/forkJoin';

import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Effect, Actions } from '@ngrx/effects';
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
import { MatSnackBar } from '@angular/material';
const { ReportActionTypes } = fromReports;

@Injectable()
export class ReportEffects {
  @Effect()
  getReports$: Observable<Action> = this.actions$
    .ofType(ReportActionTypes.GET_REPORT_LIST)
    .mergeMap(() =>
      this.api
        .getReports()
        .map(reports => new fromReports.SetReportList(reports))
    );

  constructor(
    private actions$: Actions,
    private store$: Store<State>,
    private api: ApiService,
    private router: Router,
    public snackBar: MatSnackBar
  ) {}

  @Effect()
  getReport$: Observable<Action> = this.actions$
    .ofType(ReportActionTypes.GET_REPORT)
    .map((action: fromReports.GetReport) => action.payload)
    .mergeMap(reportId =>
      this.api
        .getReport(reportId)
        .map(report => new fromReports.GetReportSuccess(report))
    );

  @Effect()
  loadDisplayFields$ = this.actions$
    .ofType(
      ReportActionTypes.GET_REPORT_SUCCESS,
      ReportActionTypes.EDIT_REPORT_SUCCESS
    )
    .map(
      (action: fromReports.GetReportSuccess | fromReports.EditReportSuccess) =>
        new fromDisplay.LoadAll(action.payload.displayfield_set)
    );

  @Effect()
  loadFilterFields$ = this.actions$
    .ofType(
      ReportActionTypes.GET_REPORT_SUCCESS,
      ReportActionTypes.EDIT_REPORT_SUCCESS
    )
    .map(
      (action: fromReports.GetReportSuccess | fromReports.EditReportSuccess) =>
        new fromFilter.LoadAll(action.payload.filterfield_set)
    );

  @Effect()
  getReportSuccess$ = this.actions$
    .ofType(ReportActionTypes.GET_REPORT_SUCCESS)
    .map((action: fromReports.GetReportSuccess) => action.payload)
    .mergeMap(report => {
      const request: IGetRelatedFieldRequest = {
        model: report.root_model,
        path: '',
        field: '',
      };
      return Observable.forkJoin(
        this.api.getRelatedFields(request),
        this.api.getFields(request)
      ).map(
        ([relatedFields, fields]) =>
          new fromReports.GetReportFieldsSuccess({ relatedFields, fields })
      );
    });

  @Effect()
  getFields$ = this.actions$
    .ofType(ReportActionTypes.GET_FIELDS)
    .map((action: fromReports.GetFields) => action.payload)
    .mergeMap(relatedField => {
      const fieldReq: IGetRelatedFieldRequest = {
        model: relatedField.model_id,
        path: relatedField.path,
        field: relatedField.field_name,
      };
      return this.api
        .getFields(fieldReq)
        .map(fields => new fromReports.GetFieldsSuccess(fields));
    });

  @Effect()
  getRelatedFields$ = this.actions$
    .ofType(ReportActionTypes.GET_RELATED_FIELDS)
    .map((action: fromReports.GetRelatedFields) => action.payload)
    .mergeMap(relatedField => {
      const fieldReq: IGetRelatedFieldRequest = {
        model: relatedField.model_id,
        path: relatedField.path,
        field: relatedField.field_name,
      };
      return this.api.getRelatedFields(fieldReq).map(
        fields =>
          new fromReports.GetRelatedFieldsSuccess({
            parentId: relatedField.id,
            relatedFields: fields,
          })
      );
    });

  @Effect()
  deleteReport$ = this.actions$
    .ofType(ReportActionTypes.DELETE_REPORT)
    .map((action: fromReports.DeleteReport) => action.payload)
    .mergeMap(reportId => {
      return this.api
        .deleteReport(reportId)
        .map(() => new fromReports.DeleteReportSuccess(reportId));
    });

  @Effect({ dispatch: false })
  deleteReportSuccess$ = this.actions$
    .ofType(ReportActionTypes.DELETE_REPORT_SUCCESS)
    .do(_ => this.router.navigate(['']));

  @Effect()
  editReport$ = this.actions$
    .ofType(ReportActionTypes.EDIT_REPORT)
    .withLatestFrom(this.store$)
    .mergeMap(([_, storeState]) => {
      const editedReport = getEditedReport(storeState);
      return this.api
        .editReport(editedReport)
        .map(response => new fromReports.EditReportSuccess(response))
        .catch(error =>
          Observable.of(new fromReports.EditReportFailure(error))
        );
    });

  @Effect()
  generatePreview$ = this.actions$
    .ofType(ReportActionTypes.GENERATE_PREVIEW)
    .withLatestFrom(this.store$)
    .mergeMap(([_, storeState]) => {
      const reportId = getSelectedReportId(storeState);
      return this.api
        .generatePreview(reportId)
        .map(response => new fromReports.GeneratePreviewSuccess(response));
    });

  @Effect()
  exportReport$ = this.actions$
    .ofType(ReportActionTypes.EXPORT_REPORT)
    .withLatestFrom(this.store$)
    .mergeMap(([action, storeState]: [fromReports.ExportReport, State]) => {
      const reportId = getSelectedReportId(storeState);
      const async = getIsAsyncReport(storeState);
      const type = action.payload;

      if (!async) {
        return Observable.create(observer => {
          observer.next(
            new fromReports.DownloadExportedReport(
              `/report_builder/report/${reportId}/download_file/${type}/`
            )
          );
          observer.complete();
        });
      }

      return this.api
        .exportReport({ reportId, type })
        .map(
          ({ task_id }) =>
            new fromReports.CheckExportStatus({ reportId, taskId: task_id })
        );
    });

  @Effect({ dispatch: false })
  downloadExportedReport$ = this.actions$
    .ofType(ReportActionTypes.DOWNLOAD_EXPORTED_REPORT)
    .mergeMap(
      (action: fromReports.DownloadExportedReport) =>
        (window.location.pathname = action.payload)
    );

  @Effect()
  checkExportStatus$ = this.actions$
    .ofType(ReportActionTypes.CHECK_EXPORT_STATUS)
    .delay(500)
    .mergeMap(
      ({ payload: { reportId, taskId } }: fromReports.CheckExportStatus) =>
        this.api.checkStatus({ reportId, taskId }).map(({ state, link }) => {
          if (state === 'SUCCESS') {
            return new fromReports.DownloadExportedReport(link);
          } else if (state === 'FAILURE') {
            return new fromReports.CancelExportReport();
          } else {
            return new fromReports.CheckExportStatus({ reportId, taskId });
          }
        })
    );

  @Effect({ dispatch: false })
  cancelExportReport$ = this.actions$
    .ofType(ReportActionTypes.CANCEL_EXPORT_REPORT)
    .do(() => this.snackBar.open('Sorry, something went wrong!'));

  @Effect()
  createReport$ = this.actions$
    .ofType(ReportActionTypes.CREATE_REPORT)
    .map((action: fromReports.CreateReport) => action.payload)
    .mergeMap(newReport => this.api.submitNewReport(newReport))
    .map(createdReport => new fromReports.CreateReportSuccess(createdReport));

  @Effect()
  createReportSuccess$ = this.actions$
    .ofType(ReportActionTypes.CREATE_REPORT_SUCCESS)
    .map((action: fromReports.CreateReportSuccess) => action.payload.id)
    .do(reportId => this.router.navigate([`/report/${reportId}/`]))
    .map(() => new fromReports.ChangeTab(0));

  @Effect()
  copyReport$ = this.actions$
    .ofType(ReportActionTypes.COPY_REPORT)
    .map((action: fromReports.CopyReport) => action.payload)
    .mergeMap(reportId => this.api.copyReport(reportId))
    .map(createdReport => new fromReports.CreateReportSuccess(createdReport));
}
