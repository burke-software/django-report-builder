import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { INewReport } from '../api.interfaces';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import { CreateReport } from '../actions/reports';

@Component({
  selector: 'app-new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css']
})
export class NewReportComponent implements OnInit {
  root_model_choices$ = this.api.getRootModels();
  form: INewReport;

  constructor(private store: Store<State>, private api: ApiService) {}

  ngOnInit() {
    this.form = {
      name: '',
      description: '',
      root_model: null
    };
  }

  submit() {
    this.store.dispatch(new CreateReport(this.form));
  }
}
