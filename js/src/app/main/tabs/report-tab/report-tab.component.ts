import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../../reducers';
import {
  getPreview,
  getLastSaved,
  getLastGeneratedReport,
  isGeneratingReport,
  getErrors,
  hasEditedSinceLastSave
} from '../../../selectors';
import {
  EditReport,
  GeneratePreview,
  ExportReport,
} from '../../../actions/reports';
import { IExportType } from '../../../models/api';

@Component({
  selector: 'app-report-tab',
  template: `
  <div class="app-report-tab">
    <div>
      <button mat-button [disabled]="!(dirty$ | async)" (click)="this.onSave()">Save</button>
      <button mat-button (click)="this.makePreview()">Preview</button>
      <button mat-button (click)="this.exportReport('xlsx')">XLSX</button>
      <button mat-button (click)="this.exportReport('csv')">CSV</button>
      <app-last-report *ngIf="lastGeneratedReport$ | async" [report]="lastGeneratedReport$ | async"></app-last-report>
      <app-saved-timestamp [lastSaved]="this.lastSaved$ | async" ></app-saved-timestamp>
    </div>
    <app-error [errors]="errors$ | async"></app-error>
    <mat-progress-bar mode="indeterminate" *ngIf="isGeneratingReport$ | async"></mat-progress-bar>
    <div *ngIf="this.previewData$ | async">
      <app-report-preview [previewData]="this.previewData$ | async" ></app-report-preview>
    </div>
  </div>
  `,
})
export class ReportTabComponent {
  constructor(private store: Store<State>) {}
  previewData$ = this.store.select(getPreview);
  lastSaved$ = this.store.select(getLastSaved);
  lastGeneratedReport$ = this.store.select(getLastGeneratedReport);
  isGeneratingReport$ = this.store.select(isGeneratingReport);
  errors$ = this.store.select(getErrors);
  dirty$ = this.store.select(hasEditedSinceLastSave);

  onSave() {
    this.store.dispatch(new EditReport());
  }

  makePreview() {
    this.store.dispatch(new GeneratePreview());
  }

  exportReport(type: IExportType) {
    this.store.dispatch(new ExportReport(type));
  }
}
