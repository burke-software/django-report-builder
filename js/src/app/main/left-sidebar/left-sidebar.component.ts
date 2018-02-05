import {
  Component,
  Input,
  EventEmitter,
  ElementRef,
  Output,
  ViewChild,
  OnInit,
  OnChanges,
} from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { IReport } from '../../models/api';
import { MatSort } from '@angular/material';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/observable/fromEvent';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/filter';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
  selector: 'app-left-sidebar',
  templateUrl: './left-sidebar.component.html',
  styleUrls: ['./left-sidebar.component.scss'],
})
export class LeftSidebarComponent implements OnInit, OnChanges {
  @Input() searchTerm: string;
  @Input() leftNavIsOpen: boolean;
  @Input() rightNavIsOpen: boolean;

  @Output() onClickReport = new EventEmitter<number>();
  @Output() searchReports = new EventEmitter<string>();
  @Output() sortReports = new EventEmitter<string>();
  @Output() onToggleLeftNav = new EventEmitter();
  @Output() onToggleRightNav = new EventEmitter();

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('filter') filter: ElementRef;

  title = 'Reports';

  displayedColumns = ['name', 'user', 'date'];
  dataSource: TableDataSource;
  myData: IReport[];

  @Input() listReports: IReport[];

  constructor() {}

  ngOnInit() {
    Observable.fromEvent(this.filter.nativeElement, 'keyup')
      .debounceTime(150)
      .distinctUntilChanged()
      .subscribe(() => {
        if (!this.dataSource) {
          return;
        }
        this.dataSource.filter = this.filter.nativeElement.value;
      });
  }

  ngOnChanges() {
    this.myData = this.listReports;
    this.dataSource = new TableDataSource(this.myData, this.sort);
  }

  clickReport(reportId: number) {
    this.onClickReport.emit(reportId);
    this.toggleLeftNav();
  }

  toggleLeftNav() {
    if (this.leftNavIsOpen === true) {
      this.onToggleLeftNav.emit();
    }
  }
}

export class TableDataSource extends DataSource<IReport> {
  filteredData: IReport[] = [];
  renderedData: IReport[] = [];

  constructor(private dataBase: IReport[], private sort: MatSort) {
    super();
  }

  _filterChange = new BehaviorSubject('');
  get filter(): string {
    return this._filterChange.value;
  }
  set filter(filter: string) {
    this._filterChange.next(filter);
  }

  /** Connect function called by the table to retrieve one stream containing the data to render. */
  connect(): Observable<IReport[]> {
    const displayDataChanges = [
      Observable.of(this.dataBase),
      this.sort.sortChange,
      this._filterChange,
    ];

    return Observable.merge(...displayDataChanges).map(() => {
      this.filteredData = this.dataBase.slice().filter((item: IReport) => {
        const searchStr = (item.name + item.modified).toLowerCase();
        return searchStr.indexOf(this.filter.toLowerCase()) !== -1;
      });

      const sortedData = this.sortData(this.filteredData.slice());

      this.renderedData = sortedData.splice(0);
      return this.renderedData;
    });
  }

  disconnect() {}

  sortData(data: IReport[]): IReport[] {
    if (!this.sort.active || this.sort.direction === '') {
      return data;
    }

    return data.sort((a, b) => {
      let propertyA: number | string = '';
      let propertyB: number | string = '';

      switch (this.sort.active) {
        case 'name':
          [propertyA, propertyB] = [a.name, b.name];
          break;
        case 'user':
          [propertyA, propertyB] = [
            a.user_created.first_name,
            b.user_created.first_name,
          ];
          break;
        case 'date':
          [propertyA, propertyB] = [a.modified, b.modified];
          break;
      }

      const valueA = isNaN(+propertyA) ? propertyA : +propertyA;
      const valueB = isNaN(+propertyB) ? propertyB : +propertyB;

      return (
        (valueA < valueB ? -1 : 1) * (this.sort.direction === 'asc' ? 1 : -1)
      );
    });
  }
}
