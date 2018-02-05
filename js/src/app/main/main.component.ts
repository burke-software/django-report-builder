import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import 'rxjs/add/observable/combineLatest';
import 'rxjs/add/observable/fromEventPattern';

import { State } from '../reducers';
import {
  getReports,
  getRelatedFields,
  getFields,
  getTitle,
  getRightNavIsOpen,
  getLeftNavIsOpen,
  getActiveTab,
  getSelectedReport,
  getSelectedField,
} from '../selectors';
import { INestedRelatedField, IField } from '../models/api';
import {
  GetReportList,
  GetReport,
  GetFields,
  GetRelatedFields,
  ToggleLeftNav,
  ToggleRightNav,
  AddReportField,
  SelectField,
} from '../actions/reports';

@Component({
  selector: 'app-main',
  template: `
    <mat-sidenav-container class="left-sidenav-container">
      <app-left-sidebar
        [listReports]="listReports$ | async"
        (onClickReport)="onClickReport($event)"
        (onToggleLeftNav)="onToggleLeftNav()"
        (onToggleRightNav)="onToggleRightNav()"
        [leftNavIsOpen]="leftNavIsOpen$ | async"
        [rightNavIsOpen]="rightNavIsOpen$ | async"
      ></app-left-sidebar>
      <app-header
      (onToggleLeftNav)="onToggleLeftNav()"
      (onToggleRightNav)="onToggleRightNav()"
      [title]="title$ | async"
      [activeTab]="activeTab$ | async">
      </app-header>
      <div class="example-sidenav-content">
        <app-tabs>
        </app-tabs>
      </div>
      <app-right-sidebar #rightMenu
        [modelName]="(selectedReport$ | async)?.name"
        [relatedFields]="relatedFields$ | async"
        [fields]="fields$ | async"
        [selectedField]="selectedField$ | async"
        (selectRelatedField)="selectRelatedField($event)"
        (onToggleRightNav)="onToggleRightNav()"
        [rightNavIsOpen]="rightNavIsOpen$ | async"
        (addReportField)="addReportField($event)"
        (selectField)="selectField($event)"
      ></app-right-sidebar>
    </mat-sidenav-container>
  `,
})
export class MainComponent implements OnInit {
  title$ = this.store.select(getTitle);
  activeTab$ = this.store.select(getActiveTab);

  listReports$ = this.store.select(getReports);

  fields$ = this.store.select(getFields);

  relatedFields$ = this.store.select(getRelatedFields);

  selectedReport$ = this.store.select(getSelectedReport);
  leftNavIsOpen$ = this.store.select(getLeftNavIsOpen);
  rightNavIsOpen$ = this.store.select(getRightNavIsOpen);
  getFields$ = this.store.select(getFields);
  selectedField$ = this.store.select(getSelectedField);

  constructor(private store: Store<State>) {}

  ngOnInit() {
    this.store.dispatch(new GetReportList());
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }

  selectRelatedField(relatedField: INestedRelatedField) {
    this.store.dispatch(new GetFields(relatedField));
    this.store.dispatch(new GetRelatedFields(relatedField));
  }

  onToggleLeftNav() {
    this.store.dispatch(new ToggleLeftNav());
  }

  onToggleRightNav() {
    this.store.dispatch(new ToggleRightNav());
  }

  addReportField(field: IField) {
    this.store.dispatch(new AddReportField(field));
  }

  selectField(field: IField) {
    this.store.dispatch(new SelectField(field));
  }
}
