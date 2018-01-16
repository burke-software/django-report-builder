import * as ReportActions from '../actions/reports';
import * as ReportReducer from './reports';

import * as testdata from './testdata';

describe('ReportsReducer', () => {
  describe('GET_RELATED_FIELDS_SUCCESS', () => {
    it('Should put the related fields into the correct part of the data structure', () => {
      const successAction = new ReportActions.GetRelatedFieldsSuccess(
        testdata.relatedFieldsPayload
      );

      const result = ReportReducer.reducer(
        testdata.populatedReports,
        successAction
      );

      // debugger;

      const expectedParent = result.relatedFields.find(
        f => f.field_name === testdata.relatedFieldsPayload.parent.field_name
      );

      expect(expectedParent.children.map(f => f.field_name)).toEqual(
        testdata.relatedFieldsPayload.relatedFields.map(f => f.field_name)
      );
    });
  });
});
