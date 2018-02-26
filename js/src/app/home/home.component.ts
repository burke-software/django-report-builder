import { Component, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { IReport } from '../models/api';
import { MatSort, MatTableDataSource, MatDialog } from '@angular/material';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import {
  GetReport,
  GetReportList,
  DeleteReport,
  CopyReport,
} from '../actions/reports';
import { getReports } from '../selectors';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../confirm/confirm-modal.component';
import { Go } from '../actions/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, AfterViewInit {
  @ViewChild(MatSort) sort: MatSort;

  displayedColumns = ['actions', 'name', 'user', 'date'];
  dataSource = new MatTableDataSource<IReport>();
  listReports$ = this.store.select(getReports);
  constructor(private store: Store<State>, public dialog: MatDialog) {}

  ngOnInit() {
    this.store.dispatch(new GetReportList());
    this.listReports$.subscribe(reports => (this.dataSource.data = reports));
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  deleteReport(report: IReport) {
    const dialogRef = this.dialog.open(ConfirmModalComponent, {
      data: {
        title: `Are you sure you want to delete ${report.name}`,
        subtitle: 'You will not be able to undo this action.',
        confirmText: 'Delete',
      } as IConfirmModalData,
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.store.dispatch(new DeleteReport(report.id));
      }
    });
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

  newReport(event: MouseEvent) {
    event.preventDefault();
    this.store.dispatch(new Go({ path: ['/report/add'] }));
  }

  openReport(event: MouseEvent, reportId: number) {
    event.preventDefault();
    this.store.dispatch(new Go({ path: ['/report/', reportId] }));
  }
}
