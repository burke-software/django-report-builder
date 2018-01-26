import { Component, Input, EventEmitter, Output } from '@angular/core';
import { IReport } from '../../api.interfaces';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss']
})
export class LeftSidebarComponent {
  @Input() listReports: IReport[];
  @Input() searchTerm: string;
  @Input() showReports: boolean;

  @Output() onClickReport = new EventEmitter<number>();
  @Output() searchReports = new EventEmitter<string>();
  @Output() sortReports = new EventEmitter<string>();

  constructor() {}

  clickReport(reportId: number) {
    this.onClickReport.emit(reportId);
  }

  onSortReports(searchTerm: string) {
    this.sortReports.emit(searchTerm);
  }

}
