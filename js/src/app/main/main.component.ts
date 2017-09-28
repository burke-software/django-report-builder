import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getReports } from '../reducers';
import { GetReportList } from '../actions/reports';

@Component({
  selector: 'app-main',
  template: `
    <app-left-sidebar
      [listReports]="listReports$ | async"
    ></app-left-sidebar>
  `,
})
export class MainComponent implements OnInit {
  listReports$ = this.store.select(getReports);

  constructor(private store: Store<State>) { }

  ngOnInit() {
    this.store.dispatch(new GetReportList());
  }

}
