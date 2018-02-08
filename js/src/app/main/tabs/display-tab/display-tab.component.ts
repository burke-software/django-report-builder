import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IDisplayField, IFormat } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-display-tab',
  templateUrl: './display-tab.component.html',
  styles: [
    `.mat-table {
    display: block;
  }`,
    `.mat-row,
  .mat-header-row {
    display: flex;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    align-items: center;
    min-height: 48px;
    padding: 0 24px;
  }`,
    `.mat-cell,
.mat-header-cell {
  flex: 1;
  overflow: hidden;
  word-wrap: break-word;
}`,
  ],
})
export class DisplayTabComponent {
  constructor() {}
  @Input() fields: IDisplayField[];
  @Input() formatOptions: IFormat[];
  @Output() deleteField = new EventEmitter<number>();
  @Output() updateField = new EventEmitter<Update<IDisplayField>>();
}
