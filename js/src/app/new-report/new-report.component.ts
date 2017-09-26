import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

import { IReportForm } from './interfaces';

@Component({
  selector: 'app-new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css']
})
export class NewReportComponent implements OnInit {
  root_model_choices$ = this.api.getRootModels();
  form: IReportForm;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.form = {
      'name': '',
      'description': '',
      'root_model': null,
    };
  }

  submit() {
    console.log(this.form);
  }

}
