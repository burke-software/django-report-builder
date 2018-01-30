import { Component, Input, EventEmitter, Output, OnInit } from '@angular/core';
import { IReport } from '../../api.interfaces';
import {Sort} from '@angular/material';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss']
})
export class LeftSidebarComponent implements OnInit {
  @Input() listReports: IReport[];
  @Input() searchTerm: string;
  @Input() leftNavIsOpen: boolean;
  @Input() rightNavIsOpen: boolean;

  @Output() onClickReport = new EventEmitter<number>();
  @Output() searchReports = new EventEmitter<string>();
  @Output() sortReports = new EventEmitter<string>();
  @Output() onToggleLeftNav = new EventEmitter();
  @Output() onToggleRightNav = new EventEmitter();
  
  sortedData;
  
  constructor() {
    // this.sortedData = this.listReports.slice(0);
  }

  ngOnInit() {
    this.sortedData = this.listReports.slice();
  }

  clickReport(reportId: number) {
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

  sortData(sort: Sort) {
    console.log(sort);
    console.log(this.sortedData);
    const data = this.listReports.slice();
    console.log(data);
    if (!sort.active || sort.direction === '') {
      this.sortedData = data;
      return;
    }

    this.sortedData = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'name': return compare(a.name, b.name, isAsc);
        case 'User': return compare(+a.user_created.first_name, +b.user_created.first_name, isAsc);
        case 'Date': return compare(+a.modified, +b.modified, isAsc);
        default: return 0;
      }
    });
  }
}

function compare(a, b, isAsc) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}