import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IFilter } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-filter-tab',
  templateUrl: './filter-tab.component.html',
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
export class FilterTabComponent {
  constructor() {}
  @Input() filters: IFilter[];
  @Output() deleteFilter = new EventEmitter<number>();
  @Output() updateFilter = new EventEmitter<Update<IFilter>>();
}
