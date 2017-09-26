import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-new-report',
  templateUrl: './new-report.component.html',
  styleUrls: ['./new-report.component.css']
})
export class NewReportComponent implements OnInit {
  root_model_choices$ = this.api.getRootModels();

  constructor(private api: ApiService) { }

  ngOnInit() {
  }

}
