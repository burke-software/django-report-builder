import { Component, Input, EventEmitter, Output } from '@angular/core';
import { IReport } from '../../api.interfaces';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss']
})
export class LeftSidebarComponent {
  @Input() listReports: IReport[];
  @Output() onClickReport = new EventEmitter<number>();

  constructor() { }

  clickReport(reportId: number) {
    this.onClickReport.emit(reportId);
  }
}