import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-copy-report',
  template: `<div><a href="/report_builder/report/{{this.id}}/create_copy/">Copy this report</a></div>`
})
export class CopyReportComponent {
  constructor() {}
  @Input() id: number;
}
