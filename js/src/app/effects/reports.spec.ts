import { TestBed } from '@angular/core/testing';
import { provideMockActions } from '@ngrx/effects/testing';
import { hot, cold } from 'jasmine-marbles';
import { Observable } from 'rxjs/Observable';
import {RouterTestingModule} from '@angular/router/testing';

import { ReportEffects } from './reports';
import * as Actions from '../actions/reports';
import { IRelatedField, IField } from '../api.interfaces';
import { ApiService } from '../api.service';

describe('Report Effects', () => {
  let effects: ReportEffects;
  let actions: Observable<any>;
  let service: any;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule.withRoutes([]),
      ],
      providers: [
        ReportEffects,
        provideMockActions(() => actions),
        {
            provide: ApiService,
            useValue: jasmine.createSpyObj('ApiService', ['getFields']),
          },
      ],
    });

    effects = TestBed.get(ReportEffects);
    service = TestBed.get(ApiService);
  });

  it('should get fields from a related field', () => {
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
    actions = hot('a-', { a: new Actions.GetFields(relatedField)});

    const responseFields: IField[] = [{
        name: 'last_run_at',
        field: 'last_run_at',
        field_verbose: 'last run at',
        field_type: 'DateTimeField',
        is_default: true,
        field_choices: [],
        can_filter: true,
        path: 'scheduledreport__',
        path_verbose: 'scheduledreport',
        help_text: ''
    }];
    const response = cold('-b', {b: responseFields});
    service.getFields.and.returnValue(response);

    const expected = cold('-c', { c: new Actions.GetFieldsSuccess(responseFields) });

    expect(effects.getFields$).toBeObservable(expected);
  });
});
