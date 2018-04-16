import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IDisplayField, IFormat } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-display-tab-row',
  templateUrl: './display-tab-row.component.html',
  styles: [
    `
  .mat-row,
  .mat-header-row {
    display: flex;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    align-items: center;
    min-height: 48px;
    padding: 0 24px;
  }`,
    `
  .mat-cell,
  .mat-header-cell {
    flex: 4;
    overflow: hidden;
    word-wrap: break-word;
  }`,
    `
  .narrow {
    flex: 1;
  }`,
  ],
})
export class DisplayTabRowComponent {
  constructor() {}
  @Input() field: IDisplayField;
  @Input() formatOptions: IFormat[];
  @Output() deleteField = new EventEmitter<number>();
  @Output() updateField = new EventEmitter<Update<IDisplayField>>();

  editField(changes) {
    this.updateField.emit({ changes, id: this.field.position });
  }
}
