import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getPreview, getLastSaved } from '../../../reducers';
import {
  EditReport,
  GeneratePreview,
  ExportReport,
} from '../../../actions/reports';

@Component({
  selector: 'app-report-tab',
  template: `
  <div class="app-report-tab">
    <div>
      <button mat-button (click)="this.onSave()">Save</button>
      <button mat-button (click)="this.makePreview()">Preview</button>
      <button mat-button (click)="this.exportReport('xlsx')">XLSX</button>
      <button mat-button (click)="this.exportReport('csv')">CSV</button>
      <app-saved-timestamp [lastSaved]="this.lastSaved$ | async" ></app-saved-timestamp>
    </div>
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

  onSave() {
    this.store.dispatch(new EditReport());
  }

  makePreview() {
    this.store.dispatch(new GeneratePreview());
  }

  exportReport(type: string) {
    this.store.dispatch(new ExportReport(type));
  }
}
