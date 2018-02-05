import { Component, Input } from '@angular/core';
import { ApiService } from '../../../api.service';

@Component({
  selector: 'app-copy-report',
  template: `<mat-list-item (click)="this.copy($event)" class="icon-link"><mat-icon matListIcon>content_copy</mat-icon><a matLine href="/report_builder/report/{{this.id}}/create_copy/">Copy this report</a></mat-list-item>`,
})
export class CopyReportComponent {
  constructor(private api: ApiService) {}
  @Input() id: number;

  // this isn't ideal. Should have a real API route to call and put it in an effect
  copy(e: MouseEvent) {
    e.preventDefault();

    const redirect = response => {
      const redirectId = response.url.match(/\/report\/(\d+)\//)[1];
      window.location.pathname = `/report/${redirectId}/`;
    };

    this.api
      .copyReport(this.id)
      .then(redirect)
      .catch(redirect);
  }
}
