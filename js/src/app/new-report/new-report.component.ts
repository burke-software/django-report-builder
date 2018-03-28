import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { INewReport } from '../models/api';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import { CreateReport } from '../actions/reports';

@Component({
  selector: 'app-new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css'],
})
export class NewReportComponent implements OnInit {
  root_model_choices$ = this.api
    .getRootModels()
    .map(models =>
      models.sort((x, y) => (x.name === y.name ? 0 : x.name > y.name ? 1 : -1))
    );
  form: INewReport;

  constructor(private store: Store<State>, private api: ApiService) {}

  ngOnInit() {
    this.form = {
      name: '',
      description: '',
      root_model: null,
    };
  }

  submit() {
    if (this.form.name.trim() && this.form.root_model) {
      this.store.dispatch(new CreateReport(this.form));
    }
  }
}
