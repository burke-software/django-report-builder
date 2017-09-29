import { Component, Input, EventEmitter, Output } from '@angular/core';
import { Store } from '@ngrx/store';
import { IReport } from '../../api.interfaces';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
})
export class LeftSidebarComponent {
  @Input() listReports: IReport[];
  @Output() onClickReport = new EventEmitter<number>();

  constructor() { }

  clickReport(reportId: number) {
    this.onClickReport.emit(reportId);
  }
}
