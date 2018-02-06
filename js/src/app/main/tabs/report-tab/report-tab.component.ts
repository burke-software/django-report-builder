import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../../reducers';
import { getPreview, getLastSaved } from '../../../selectors';
import {
  EditReport,
  GeneratePreview,
  ExportReport,
} from '../../../actions/reports';

@Component({
  selector: 'app-report-tab',
  styleUrls: ['./report.component.scss'],
  template: `
  <div class="mat-table tab-table-header">
    <div class="mat-header-row">
      <div><button mat-button (click)="this.onSave()">SAVE</button></div>
      <div><button mat-button (click)="this.makePreview()">PREVIEW</button></div>
      <div><button mat-button (click)="this.exportReport('xlsx')">XLSX</button></div>
      <div><button mat-button (click)="this.exportReport('csv')">CSV</button></div>
      <div><app-saved-timestamp [lastSaved]="this.lastSaved$ | async" ></app-saved-timestamp></div>
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
