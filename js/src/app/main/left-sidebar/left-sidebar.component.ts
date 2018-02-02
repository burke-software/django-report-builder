import {
  Component,
  Input,
  EventEmitter,
  Output,
  ViewChild,
} from '@angular/core';
import { IReport } from '../../api.interfaces';
import { MatSort, MatTableDataSource, Sort } from '@angular/material';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss'],
})
export class LeftSidebarComponent {
  @Input() searchTerm: string;
  @Input() leftNavIsOpen: boolean;
  @Input() rightNavIsOpen: boolean;

  @Output() onClickReport = new EventEmitter<number>();
  @Output() searchReports = new EventEmitter<string>();
  @Output() sortReports = new EventEmitter<string>();
  @Output() onToggleLeftNav = new EventEmitter();
  @Output() onToggleRightNav = new EventEmitter();

  @ViewChild(MatSort) sort: MatSort;

  @Input()
  set listReports(value: IReport[]) {
    this.sortedData = value;
    this.reports = value;
    this.dataSource = new MatTableDataSource(value);
  }

  sortedData;
  reports;
  dataSource: MatTableDataSource<IReport>;

  title = 'Reports';

  displayedColumns = ['name', 'user', 'date'];

  constructor() {}

  clickReport(reportId: number) {
    this.onToggleLeftNav.emit();
    this.onClickReport.emit(reportId);
    if (this.rightNavIsOpen === false) {
      this.onToggleRightNav.emit();
    }
  }

  toggleLeftNav() {
    if (this.leftNavIsOpen === true) {
      this.onToggleLeftNav.emit();
    }
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim();
    filterValue = filterValue.toLowerCase();
    this.dataSource.filter = filterValue;
  }

  sortData(sort: Sort) {
    const data = this.reports.slice();
    if (!sort.active || sort.direction === '') {
      this.sortedData = data;
      return;
    }

    this.sortedData = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'name':
          return compare(a.name, b.name, isAsc);
        case 'User':
          return compare(
            +a.user_created.first_name,
            +b.user_created.first_name,
            isAsc
          );
        case 'Date':
          return compare(+a.modified, +b.modified, isAsc);

        default:
          return 0;
      }
    });
  }
}

function compare(a, b, isAsc) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
