import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../../reducers';
import { EditReport } from '../../../actions/reports';

@Component({
  selector: 'app-report-tab',
  template: `
  <div>
    <button mat-button (click)="this.onSave()">Save</button>
    <button mat-button>Preview</button>
    <button mat-button>XLSX</button>
    <button mat-button>CSV</button>
    Info here about last save
  </div>
  `
})
export class ReportTabComponent {
  constructor(private store: Store<State>) { }

  onSave() {
    this.store.dispatch(new EditReport());
  }
}
