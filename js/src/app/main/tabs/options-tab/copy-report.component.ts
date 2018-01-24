import { Component, Input } from '@angular/core';
import {Router} from '@angular/router';
import { ApiService } from '../../../api.service';

interface NewReport {
  name: string;
  description: string;
  root_model: number;
}

@Component({
  selector: 'app-copy-report',
  template: `<div><a href="#" *ngIf="report" (click)="this.copy($event)">Copy this report</a></div>`
})
export class CopyReportComponent {
  constructor(private router: Router, private api: ApiService) { }

  @Input() report?: NewReport;

  copy(e) {
    e.preventDefault();
    const name = this.report.name + ' (copy)';
    const report: NewReport = {...this.report, name};

    this.api.submitNewReport(report).then((resp) => {
      this.router.navigate(['']);
    });
  }
}
