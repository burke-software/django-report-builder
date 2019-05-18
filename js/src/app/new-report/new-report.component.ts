import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { EMPTY } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ApiService } from '../api.service';
import { INewReport } from '../models/api';
import { State } from '../reducers';
import { CreateReport } from '../actions/reports';

@Component({
  selector: 'app-new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css'],
})
export class NewReportComponent implements OnInit {
  errors: string[] = [];

  root_model_choices$ = this.api.getRootModels().pipe(
    map(models => {
      this.errors = [];
      return models.sort((x, y) =>
        x.name === y.name ? 0 : x.name > y.name ? 1 : -1
      );
    }),
    catchError(err => {
      if ('detail' in err) {
        this.errors = [err.detail];
      } else {
        this.errors = ['Unable to fetch models from Django'];
      }
      return EMPTY;
    })
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
