import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IFilter } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-filter-tab-row',
  templateUrl: './filter-tab-row.component.html',
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
export class FilterTabRowComponent {
  constructor() {}
  @Input() filter: IFilter;
  @Output() deleteFilter = new EventEmitter<number>();
  @Output() updateFilter = new EventEmitter<Update<IFilter>>();

  editFilter(changes) {
    this.updateFilter.emit({ changes, id: this.filter.position });
  }
}
