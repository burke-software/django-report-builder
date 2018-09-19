import { Component, Input } from '@angular/core';

interface ReportInput {
  report_file: string;
  report_file_creation: string;
}

@Component({
  selector: 'app-last-report',
  template: `
  <a mat-button href="{{ report.report_file }}" matTooltip="Download report generated at {{ report.report_file_creation }}">
    <mat-icon>file_download</mat-icon>Download
  </a>`,
})
export class LastReportComponent {
  @Input() report: ReportInput;

  constructor() {}
}
