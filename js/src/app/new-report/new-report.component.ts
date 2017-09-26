import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
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

  constructor(private router: Router, private api: ApiService) { }

  ngOnInit() {
    this.form = {
      'name': '',
      'description': '',
      'root_model': null,
    };
  }

  submit() {
    this.api.submitNewReport(this.form).then((resp) => {
      if (resp.status === 201) {
        this.router.navigate(['']);
      }
    });
  }

}
