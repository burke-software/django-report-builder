import { Component, Output, EventEmitter } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getDescriptionInput, getIsDistinct, getSelectedReportId } from '../../../reducers';
import { ChangeReportDescription, ToggleReportDistinct, DeleteReport } from '../../../actions/reports';

@Component({
  selector: 'app-report-tab',
  template: `
  <div>
    <button mat-button>Save</button>
    <button mat-button>Preview</button>
    <button mat-button>XLSX</button>
    <button mat-button>CSV</button>
    Info here about last save
  </div>
  `
})
export class ReportTabComponent {
  constructor(private store: Store<State>) { }
}
