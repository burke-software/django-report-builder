import {
  Component,
  ViewChild,
  OnInit,
  AfterViewInit,
  OnDestroy,
} from '@angular/core';
import { IReport } from '../models/api';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import { DeleteReport, CopyReport, SearchReports } from '../actions/reports';
import { getReports } from '../selectors';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../confirm/confirm-modal.component';
import { Go } from '../actions/router';
import { ApiService } from '../api.service';
import { Subscription } from 'rxjs';

interface IReportSortable extends IReport {
  modifiedDate: Date;
  sortName: string;
}

function modifiedStringToDate(report: IReport): IReportSortable {
  return {
    ...report,
    modifiedDate: new Date(report.modified),
    sortName: report.name.toLowerCase(),
  };
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  // private searchSubject = new Subject<string>();
  displayedColumns = ['actions', 'name', 'user', 'date'];
  dataSource = new MatTableDataSource<IReportSortable>();
  listReports$ = this.store.select(getReports);
  private subscriptions = new Subscription();

  constructor(
    private store: Store<State>,
    public dialog: MatDialog,
    public api: ApiService
  ) {}

  ngOnInit() {
    this.subscriptions.add(
      this.listReports$.subscribe(reports => {
        this.dataSource.data = reports.map(modifiedStringToDate);
      })
    );
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.sortingDataAccessor = (data, sortHeaderId) => {
      switch (sortHeaderId.toLowerCase()) {
        case 'name':
          return data.sortName;
        case 'date':
          return data.modified;
        default:
          return data[sortHeaderId];
      }
    };
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
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

  searchReports(event: KeyboardEvent, text: string) {
    event.preventDefault();

    if (text && text.trim()) {
      this.store.dispatch(new SearchReports(text));
    }
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
