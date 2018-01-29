import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import 'rxjs/add/observable/combineLatest';
import { Observable } from 'rxjs/Observable';
import { filterSearch } from './utils/filterSearch';
import { sortReports } from './utils/sort';

import {
  State,
  getReports,
  getRelatedFields,
  getFields,
  getShowReports,
  getSearchTerm,
  getSelectedReport,
  getSortTerm,
  getSortOrder
} from '../reducers';
import { IRelatedField } from '../api.interfaces';
import {
  GetReportList,
  GetReport,
  GetFields,
  GetRelatedFields,
  SetSearchText,
  SortReports
} from '../actions/reports';

@Component({
  selector: 'app-main',
  template: `
    <mat-sidenav-container class="left-sidenav-container">
      <app-left-sidebar
        [listReports]="listReports$ | async"
        (onClickReport)="onClickReport($event)"
        (searchReports)="setSearchTerm($event)"
        (sortReports)="sortReports($event)"
        [showReports]="showReports$ | async"
      ></app-left-sidebar>
      <div class="example-sidenav-content" style="padding-left: 100px;">
        <app-tabs>
        </app-tabs>
      </div>
      <app-right-sidebar
        [modelName]="(selectedReport$ | async)?.name"
        [fields]="fields$ | async"
        [relatedFields]="relatedFields$ | async"
        (selectRelatedField)="selectRelatedField($event)"
      ></app-right-sidebar>
    </mat-sidenav-container>
  `
})
export class MainComponent implements OnInit {

  sortReportsBy$ = Observable.combineLatest(
    this.store.select(getSortTerm),
    this.store.select(getReports),
    this.store.select(getSortOrder),
    sortReports
  );

  listReports$ = Observable.combineLatest(
    this.sortReportsBy$,
    this.store.select(getSearchTerm),
    filterSearch
  );

  selectedReport$ = this.store.select(getSelectedReport);
  showReports$ = this.store.select(getShowReports);
  fields$ = this.store.select(getFields);
  relatedFields$ = this.store.select(getRelatedFields);

  constructor(private store: Store<State>) {
    this.relatedFields$.subscribe((value) => console.log(value));
  }

  ngOnInit() {
    this.store.dispatch(new GetReportList());
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }

  selectRelatedField(relatedField: IRelatedField) {
    this.store.dispatch(new GetFields(relatedField));
    this.store.dispatch(new GetRelatedFields(relatedField));
  }

  setSearchTerm(searchTerm: string) {
    this.store.dispatch(new SetSearchText(searchTerm));
  }

  sortReports(sortBy: string) {
    this.store.dispatch(new SortReports(sortBy));
  }

}
