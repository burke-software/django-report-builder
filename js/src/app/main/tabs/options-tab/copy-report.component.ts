import { Component, Input } from '@angular/core';
import {Router} from '@angular/router';
import { ApiService } from '../../../api.service';
import { INewReport } from '../../../api.interfaces';

@Component({
  selector: 'app-copy-report',
  template: `<div><a href="#" *ngIf="report" (click)="this.copy($event)">Copy this report</a></div>`
})
export class CopyReportComponent {
  constructor(private router: Router, private api: ApiService) { }

  @Input() report?: INewReport;

  copy(e) {
    e.preventDefault();
    const name = this.report.name + ' (copy)';
    const report: INewReport = {...this.report, name};

    this.api.submitNewReport(report).then((resp: {id: number}) => {
      this.router.navigate([`/report/${resp.id}`]);
    });
  }
}
