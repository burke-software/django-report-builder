import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getPreview } from '../../../reducers';
import { EditReport, GeneratePreview } from '../../../actions/reports';

@Component({
  selector: 'app-report-tab',
  template: `
  <div>
    <div>
      <button mat-button (click)="this.onSave()">Save</button>
      <button mat-button (click)="this.makePreview()">Preview</button>
      <button mat-button>XLSX</button>
      <button mat-button>CSV</button>
      Info here about last save
    </div>
    <div>
      <app-report-preview [previewData]="this.previewData$ | async" ></app-report-preview>
    </div>
  </div>
  `
})
export class ReportTabComponent {
  constructor(private store: Store<State>) {}
  previewData$ = this.store.select(getPreview);

  onSave() {
    this.store.dispatch(new EditReport());
  }

  makePreview() {
    this.store.dispatch(new GeneratePreview());
  }
}
