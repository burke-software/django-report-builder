import {
  Component,
  ElementRef,
  ViewChild,
  OnInit,
  AfterViewInit,
} from '@angular/core';
import { IReport } from '../models/api';
import { MatSort, MatTableDataSource } from '@angular/material';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import {
  GetReport,
  GetReportList,
  DeleteReport,
  CopyReport,
} from '../actions/reports';
import { getReports } from '../selectors';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, AfterViewInit {
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('filter') filter: ElementRef;

  displayedColumns = ['actions', 'name', 'user', 'date'];
  dataSource = new MatTableDataSource<IReport>();
  listReports$ = this.store.select(getReports);
  constructor(private store: Store<State>) {}

  ngOnInit() {
    this.store.dispatch(new GetReportList());
    this.listReports$.subscribe(reports => (this.dataSource.data = reports));
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  deleteReport(reportId: number) {
    this.store.dispatch(new DeleteReport(reportId));
  }

  copyReport(reportId: number) {
    this.store.dispatch(new CopyReport(reportId));
  }

  clickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}
