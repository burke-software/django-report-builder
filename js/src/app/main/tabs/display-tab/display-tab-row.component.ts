import { Component, Input } from '@angular/core';
import { IDisplayField } from '../../../api.interfaces';

@Component({
  selector: 'app-display-tab-row',
  templateUrl: './display-tab-row.component.html',
  styles: [
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
export class DisplayTabRowComponent {
  constructor() {}
  @Input() field: IDisplayField;
}
