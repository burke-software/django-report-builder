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
  @Input() showFields: boolean;

  @Output() onClickReport = new EventEmitter<number>();
  @Output() searchReports = new EventEmitter<string>();
  @Output() sortReports = new EventEmitter<string>();
  @Output() onToggleLeftNav = new EventEmitter();
  @Output() onToggleRightNav = new EventEmitter();

  constructor() {}

  clickReport(reportId: number) {
    this.onClickReport.emit(reportId);
    if (this.showFields === false) {
      this.onToggleRightNav.emit();
    }
  }

  onSortReports(searchTerm: string) {
    this.sortReports.emit(searchTerm);
  }

  toggleLeftNav() {
    if (this.showReports === true) {
      this.onToggleLeftNav.emit();
    }
  }

}
