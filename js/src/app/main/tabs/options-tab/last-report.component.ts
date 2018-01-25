import { Component, Input } from '@angular/core';

interface ReportInput {
  report_file: string;
  report_file_creation: string;
}

@Component({
  selector: 'app-last-report',
  template: `
  <div>
    <a href="{{ report.report_file }}">Download existing report generated</a> at {{ report.report_file_creation }}
  </div>`
})
export class LastReportComponent {
  @Input() report: ReportInput;

  constructor() {}
}
