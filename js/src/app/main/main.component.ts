import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getReports } from '../reducers';
import { GetReportList, GetReport } from '../actions/reports';

@Component({
  selector: 'app-main',
  template: `
    <mat-sidenav-container style="height: 700px">
      <app-left-sidebar
        [listReports]="listReports$ | async"
        (onClickReport)="onClickReport($event)"
      ></app-left-sidebar>
      <div class="example-sidenav-content" style="padding-left: 100px;">
        <app-tabs></app-tabs>
      </div>
      <app-right-sidebar
      ></app-right-sidebar>
    </mat-sidenav-container>
  `,
})
export class MainComponent implements OnInit {
  listReports$ = this.store.select(getReports);

  constructor(private store: Store<State>) { }

  ngOnInit() {
    this.store.dispatch(new GetReportList());
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }
}
