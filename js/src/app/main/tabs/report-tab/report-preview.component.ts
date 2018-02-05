import { Component, Input } from '@angular/core';

import { IReportPreview } from '../../../models/api';

@Component({
  selector: 'app-report-preview',
  template: `<table>
    <thead><tr><td *ngFor="let header of previewData.meta.titles">{{header}}</td></tr></thead>
    <tbody><tr *ngFor="let row of previewData.data"><td *ngFor="let cell of row">{{cell}}</td></tr></tbody>
  </table>`,
})
export class ReportPreviewComponent {
  constructor() {}
  @Input() previewData?: IReportPreview;
}
