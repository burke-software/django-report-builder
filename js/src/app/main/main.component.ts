import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getReports, getRelatedFields, getFields, getSelectedReport } from '../reducers';
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
        [modelName]="(selectedReport$ | async)?.name"
        [fields]="fields$ | async"
        [relatedFields]="relatedFields$ | async"
      ></app-right-sidebar>
    </mat-sidenav-container>
  `,
})
export class MainComponent implements OnInit {
  listReports$ = this.store.select(getReports);
  selectedReport$ = this.store.select(getSelectedReport);
  fields$ = this.store.select(getFields);
  relatedFields$ = this.store.select(getRelatedFields);

  constructor(private store: Store<State>) { }

  ngOnInit() {
    this.store.dispatch(new GetReportList());
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }
}
