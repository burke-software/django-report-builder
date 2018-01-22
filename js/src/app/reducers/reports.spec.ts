import * as ReportActions from '../actions/reports';
import * as ReportReducer from './reports';

import * as testdata from './testdata.spec';

describe('ReportsReducer', () => {
  describe('GET_REPORT', () => {
    it('should set the current active report to null', () => {
      const getReportAction = new ReportActions.GetReport(0);
      const result = ReportReducer.reducer(
        testdata.populatedReports,
        getReportAction
      );

      expect(result.selectedReport).toBeNull();
    });
  });

  describe('GET_REPORT_SUCCESS', () => {
    it('Should make this report the selected report and reset lists of fields', () => {
      const newReport = {
        id: 1,
        name: 'bopo',
        description: 'asdlkmad',
        modified: '2018-01-08',
        root_model: 16,
        root_model_name: 'comment',
        displayfield_set: [],
        distinct: false,
        user_created: 1,
        user_modified: null,
        filterfield_set: [],
        report_file: null,
        report_file_creation: null
      };

      const getReportSuccessAction = new ReportActions.GetReportSuccess(
        newReport
      );

      const result = ReportReducer.reducer(
        testdata.populatedReports,
        getReportSuccessAction
      );
      expect(result).toEqual(
        jasmine.objectContaining({
          selectedReport: newReport,
          relatedFields: ReportReducer.initialState.relatedFields,
          fields: ReportReducer.initialState.fields
        })
      );
    });
  });

  describe('GET_RELATED_FIELDS_SUCCESS', () => {
    it('Should put the related fields into the correct part of the data structure', () => {
      const parent = testdata.populatedReports.relatedFields[0];
      const successAction = new ReportActions.GetRelatedFieldsSuccess({
        parent,
        relatedFields: testdata.newRelatedFields
      });

      const result = ReportReducer.reducer(
        testdata.populatedReports,
        successAction
      );

      const expectedParent = result.relatedFields.find(
        f => f.field_name === parent.field_name
      );

      expect(expectedParent.children.map(f => f.field_name)).toEqual(
        testdata.newRelatedFields.map(f => f.field_name)
      );
    });
  });
});
