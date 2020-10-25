import { Component, HostListener, ViewChild } from '@angular/core';
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
import { MatDialog } from '@angular/material/dialog';
import { MatSidenav } from '@angular/material/sidenav';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../confirm/confirm-modal.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements ComponentCanDeactivate {
  @ViewChild(MatSidenav, { static: true }) sidenav: MatSidenav;
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

  mode: 'over' | 'side' = 'over';
  lockOpen = false;

  constructor(
    private store: Store<State>,
    public dialog: MatDialog,
    breakpointObserver: BreakpointObserver
  ) {
    store
      .select(hasEditedSinceLastSave)
      .subscribe(edited => (this.edited = edited));

    breakpointObserver
      .observe([Breakpoints.Handset, Breakpoints.TabletPortrait])
      .subscribe(result => {
        this.mode = result.matches ? 'over' : 'side';
      });

    breakpointObserver.observe(['(min-width: 2000px)']).subscribe(result => {
      this.lockOpen = result.matches;
    });
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

  openNav(bool?: boolean) {
    if (!this.lockOpen) {
      if (bool === undefined) {
        this.sidenav.toggle();
      } else if (bool) {
        this.sidenav.open();
      } else {
        this.sidenav.close();
      }
    }
  }

  onClickReport(reportId: number) {
    this.store.dispatch(new GetReport(reportId));
  }

  selectRelatedField(relatedField: INestedRelatedField) {
    this.store.dispatch(new GetFields(relatedField));
  }

  expandRelatedField(relatedField: INestedRelatedField) {
    this.store.dispatch(new GetRelatedFields(relatedField));
  }

  toggleRightNav(open: boolean) {
    this.store.dispatch(new ToggleRightNav(open));
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
