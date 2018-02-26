import { Component, HostListener } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../reducers';
import {
  getReports,
  getRelatedFields,
  getFields,
  getTitle,
  getRightNavIsOpen,
  getActiveTab,
  getSelectedReport,
  getSelectedField,
  hasEditedSinceLastSave,
  getSelectedReportName,
} from '../selectors';
import { INestedRelatedField, IField } from '../models/api';
import {
  GetReport,
  GetFields,
  GetRelatedFields,
  ToggleRightNav,
  AddReportField,
  SelectField,
  ChangeReportTitle,
} from '../actions/reports';
import { Go } from '../actions/router';
import { ComponentCanDeactivate } from '../generic.guard';
import { MatDialog } from '@angular/material';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../confirm/confirm-modal.component';

@Component({
  selector: 'app-main',
  template: `
    <mat-sidenav-container class="left-sidenav-container">
      <app-header
        (onToggleRightNav)="onToggleRightNav()"
        (changeTitleInput)="editTitle($event)"
        [title]="title$ | async"
        [showRightNavButton]="(activeTab$ | async) <= 1"
        [reportName]="(selectedReportName$ | async)"
        (goHome)="goHome()">
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
export class MainComponent implements ComponentCanDeactivate {
  title$ = this.store.select(getTitle);
  activeTab$ = this.store.select(getActiveTab);

  listReports$ = this.store.select(getReports);

  fields$ = this.store.select(getFields);

  relatedFields$ = this.store.select(getRelatedFields);

  selectedReport$ = this.store.select(getSelectedReport);
  selectedReportName$ = this.store.select(getSelectedReportName);
  rightNavIsOpen$ = this.store.select(getRightNavIsOpen);
  getFields$ = this.store.select(getFields);
  selectedField$ = this.store.select(getSelectedField);
  edited = false;

  constructor(private store: Store<State>, public dialog: MatDialog) {
    store
      .select(hasEditedSinceLastSave)
      .subscribe(edited => (this.edited = edited));
  }

  canDeactivate() {
    if (this.edited) {
      const dialogRef = this.dialog.open(ConfirmModalComponent, {
        data: {
          title: 'Are you sure you want to navigate away from this report?',
          subtitle: 'All of your changes will be lost.',
        } as IConfirmModalData,
      });
      return dialogRef.afterClosed();
    }
    return true;
  }

  @HostListener('window:beforeunload')
  beforeUnload() {
    if (this.edited) {
      return confirm();
    }
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }

  selectRelatedField(relatedField: INestedRelatedField) {
    this.store.dispatch(new GetFields(relatedField));
    this.store.dispatch(new GetRelatedFields(relatedField));
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

  editTitle(title: string) {
    this.store.dispatch(new ChangeReportTitle(title));
  }

  goHome() {
    this.store.dispatch(new Go({ path: ['/'] }));
  }
}
