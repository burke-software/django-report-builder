import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IFilter } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-filter-tab-row',
  templateUrl: './filter-tab-row.component.html',
  styleUrls: ['../tabs.component.scss'],
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
