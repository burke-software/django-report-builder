import { TestBed, fakeAsync } from '@angular/core/testing';
import { provideMockActions } from '@ngrx/effects/testing';
import { hot, cold, getTestScheduler } from 'jasmine-marbles';
import { RouterTestingModule } from '@angular/router/testing';
import { StoreModule } from '@ngrx/store';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';

import { ReportEffects } from './reports';
import * as Actions from '../actions/reports';
import {
  IRelatedField,
  IField,
  INewReport,
  IReportDetailed,
  INestedRelatedField,
  IAggregate,
} from '../models/api';
import { ApiService } from '../api.service';
import { reducers, metaReducers } from '../reducers';
import { initialState } from './mockStoreInit';

describe('Report Effects', () => {
  let effects: ReportEffects;
  let actions: Observable<any>;
  let service: jasmine.SpyObj<ApiService>;

  const makeTestbedConfig = state => ({
    imports: [
      RouterTestingModule.withRoutes([]),
      StoreModule.forRoot(reducers, { metaReducers, initialState: state }),
      MatSnackBarModule,
    ],
    providers: [
      ReportEffects,
      provideMockActions(() => actions),
      {
        provide: ApiService,
        // Next line mocks all the functions provided in api.service.ts
        useValue: jasmine.createSpyObj(
          'ApiService',
          Object.getOwnPropertyNames(ApiService.prototype)
        ),
      },
    ],
  });
  describe('using default initial state', () => {
    beforeEach(() => {
      TestBed.configureTestingModule(makeTestbedConfig(initialState));

      effects = TestBed.get(ReportEffects);
      service = TestBed.get(ApiService);
    });

    it('GetFields should get fields from a related field', () => {
      const relatedField: IRelatedField = {
        field_name: 'scheduledreport',
        verbose_name: 'scheduledreport_set',
        path: '',
        help_text: '',
        model_id: 24,
        parent_model_name: 'scheduledreport',
        parent_model_app_label: false,
        included_model: true,
      };
      actions = hot('a-', { a: new Actions.GetFields(relatedField) });

      const responseFields: IField[] = [
        {
          name: 'last_run_at',
          field: 'last_run_at',
          field_verbose: 'last run at',
          field_type: 'DateTimeField',
          is_default: true,
          field_choices: [],
          can_filter: true,
          path: 'scheduledreport__',
          path_verbose: 'scheduledreport',
          help_text: '',
        },
      ];
      const response = cold('-b', { b: responseFields });
      service.getFields.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.GetFieldsSuccess(responseFields),
      });

      expect(effects.getFields$).toBeObservable(expected);
    });

    it('GetRelatedFields should get fields from a related field', () => {
      const relatedField: INestedRelatedField = {
        field_name: 'scheduledreport',
        verbose_name: 'scheduledreport_set',
        path: '',
        help_text: '',
        model_id: 24,
        parent_model_name: 'scheduledreport',
        parent_model_app_label: false,
        included_model: true,
        children: [],
        id: 0,
      };
      actions = hot('a-', { a: new Actions.GetRelatedFields(relatedField) });

      const responseFields: IRelatedField[] = [
        {
          field_name: 'last_run_at',
          verbose_name: 'last run at',
          path: 'scheduledreport__',
          help_text: '',
          model_id: 5,
          parent_model_name: 'scheduledreport__',
          parent_model_app_label: false,
          included_model: true,
        },
      ];
      const response = cold('-b', { b: responseFields });
      service.getRelatedFields.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.GetRelatedFieldsSuccess({
          parentId: relatedField.id,
          relatedFields: responseFields,
        }),
      });

      expect(effects.getRelatedFields$).toBeObservable(expected);
    });

    it('DeleteReport should delete the current report', () => {
      actions = hot('a-', { a: new Actions.DeleteReport(4) });

      const response = cold('-b', { b: { id: 4 } });

      service.deleteReport.and.returnValue(response);

      const expected = cold('-c', { c: new Actions.DeleteReportSuccess(4) });
      expect(effects.deleteReport$).toBeObservable(expected);
    });

    it('GeneratePreview should get a preview of the currently selected report', () => {
      actions = hot('a-', { a: new Actions.GeneratePreview() });

      const reportPreview = {
        data: [['place', 10], ['user', 4]],
        meta: { titles: ['model', 'id'] },
      };

      const response = cold('-b', { b: reportPreview });
      service.generatePreview.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.GeneratePreviewSuccess(reportPreview),
      });
      expect(effects.generatePreview$).toBeObservable(expected);
    });

    it('EditReport should save the changes to the current report', () => {
      actions = hot('a-', { a: new Actions.EditReport() });

      // prettier-ignore
      const savedReport = {"id":4,"name":"afasdf","description":"adgsasfg","modified":"2018-01-18","root_model":5,"root_model_name":"content type","displayfield_set":[{"id":1,"path":"","path_verbose":"","field":"model","field_verbose":"python model class name","name":"model","sort":null,"sort_reverse":false,"width":15,"aggregate":"" as IAggregate,"position":0,"total":false,"group":false,"report":4,"display_format":null,"field_type":"CharField"},{"id":2,"path":"","path_verbose":"","field":"id","field_verbose":"ID","name":"id","sort":null,"sort_reverse":false,"width":15,"aggregate":"" as IAggregate,"position":1,"total":false,"group":false,"report":4,"display_format":null,"field_type":"AutoField"}],"distinct":false,"user_created":1,"user_modified":null,"filterfield_set":[],"report_file":null,"report_file_creation":null}

      const response = cold('-b', { b: savedReport });
      service.editReport.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.EditReportSuccess(savedReport),
      });
      expect(effects.editReport$).toBeObservable(expected);
    });

    it('CreateReport should make an api call and return a success', () => {
      const newReport: INewReport = {
        name: 'testy',
        description: 'descy',
        root_model: 2,
      };
      actions = hot('a-', { a: new Actions.CreateReport(newReport) });
      // prettier-ignore
      const newReportDetailed: IReportDetailed = {"id":8,"name":"asdad","description":"asdadc","modified":"2018-01-24","root_model":1,"root_model_name":"log entry","displayfield_set":[],"distinct":false,"user_created":1,"user_modified":null,"filterfield_set":[],"report_file":null,"report_file_creation":null}

      const response = cold('-b', { b: newReportDetailed });
      service.submitNewReport.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.CreateReportSuccess(newReportDetailed),
      });
      expect(effects.createReport$).toBeObservable(expected);
    });
  });

  describe('with async === false', () => {
    const state = Object.assign({}, initialState, {
      config: { async_report: false },
    });
    const reportId = state.reports.selectedReport.id;

    beforeEach(() => {
      TestBed.configureTestingModule(makeTestbedConfig(state));

      effects = TestBed.get(ReportEffects);
      service = TestBed.get(ApiService);
    });

    it('ExportReport should dispatch a download action', () => {
      const type = 'csv';

      actions = hot('a', { a: new Actions.ExportReport(type) });

      const expected = hot('c', {
        c: new Actions.DownloadExportedReport(
          `api/report/${reportId}/download_file/${type}/`
        ),
      });
      expect(effects.exportReport$).toBeObservable(expected);
    });
  });

  describe('with async === true', () => {
    const state = Object.assign({}, initialState, {
      config: { async_report: true },
    });
    const reportId = state.reports.selectedReport.id;
    const taskId = '12345';

    beforeEach(() => {
      TestBed.configureTestingModule(makeTestbedConfig(state));

      effects = TestBed.get(ReportEffects);
      service = TestBed.get(ApiService);
    });

    it('ExportReport should start the task', () => {
      const type = 'csv';

      actions = hot('a-', { a: new Actions.ExportReport(type) });
      const response = cold('-b', { b: { task_id: taskId } });

      service.exportReport.and.returnValue(response);

      const expected = cold('-c', {
        c: new Actions.CheckExportStatus({ reportId, taskId }),
      });
      expect(effects.exportReport$).toBeObservable(expected);
    });

    it("CheckExportStatus should dispatch another CheckExportStatus action if the download isn't ready", () => {
      actions = hot('a', {
        a: new Actions.CheckExportStatus({ reportId, taskId }),
      });
      const response = cold('-b', { b: { state: 'newp' } });
      const expected = cold('---c', {
        c: new Actions.CheckExportStatus({ reportId, taskId }),
      });

      service.checkStatus.and.returnValue(response);
      const actual = effects.checkExportStatus$({
        delayTime: 20,
        scheduler: getTestScheduler(),
      });

      expect(actual).toBeObservable(expected);
    });

    it('CheckExportStatus should dispatch a download request if the download is ready', fakeAsync(() => {
      const link = 'place/download';
      actions = hot('a', {
        a: new Actions.CheckExportStatus({ reportId, taskId }),
      });
      const response = cold('-b', { b: { state: 'SUCCESS', link } });
      const expected = cold('---c', {
        c: new Actions.DownloadExportedReport(link),
      });

      service.checkStatus.and.returnValue(response);
      const actual = effects.checkExportStatus$({
        delayTime: 20,
        scheduler: getTestScheduler(),
      });

      expect(actual).toBeObservable(expected);
    }));
  });
});
