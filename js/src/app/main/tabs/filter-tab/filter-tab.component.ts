import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IFilter } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-filter-tab',
  templateUrl: './filter-tab.component.html',
  styleUrls: ['../tabs.component.scss'],
})
export class FilterTabComponent {
  constructor() {}
  @Input() filters: IFilter[];
  @Output() deleteFilter = new EventEmitter<number>();
  @Output() updateFilter = new EventEmitter<Update<IFilter>>();
}
