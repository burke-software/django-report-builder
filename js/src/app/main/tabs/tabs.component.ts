import { Component, OnInit, ViewEncapsulation, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { ChangeTab, EditReport } from '../../actions/reports';
import * as DisplayFieldActions from '../../actions/display-field';
import * as FilterActions from '../../actions/filter';
import { State } from '../../reducers';
import {
  getActiveTab,
  getDisplayFields,
  getFilters,
  getFormatOptions,
  getSelectedReport,
  hasEditedSinceLastSave,
  getErrors,
} from '../../selectors';
import { MatTabGroup } from '@angular/material/tabs';
import { Update } from '@ngrx/entity';
import { IDisplayField, IFilter } from '../../models/api';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.component.html',
  styleUrls: ['./tabs.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class TabsComponent implements OnInit {
  constructor(private store: Store<State>) {}
  displayFields$ = this.store.select(getDisplayFields);
  filters$ = this.store.select(getFilters);
  activeTab$ = this.store.select(getActiveTab);
  formatOptions$ = this.store.select(getFormatOptions);
  report$ = this.store.select(getSelectedReport);
  hasChanged$ = this.store.select(hasEditedSinceLastSave);
  errors$ = this.store.select(getErrors);
  @ViewChild('tabs', { static: true }) tabs: MatTabGroup;

  ngOnInit() {
    this.activeTab$.subscribe(number => (this.tabs.selectedIndex = number));
  }

  tabChange(index: number) {
    this.store.dispatch(new ChangeTab(index));
  }

  updateDisplayField(update: Update<IDisplayField>) {
    this.store.dispatch(new DisplayFieldActions.UpdateOne(update));
  }

  deleteDisplayField(id: number) {
    this.store.dispatch(new DisplayFieldActions.DeleteOne(id));
  }

  updateFilter(update: Update<IFilter>) {
    this.store.dispatch(new FilterActions.UpdateOne(update));
  }

  deleteFilter(id: number) {
    this.store.dispatch(new FilterActions.DeleteOne(id));
  }

  saveReport() {
    this.store.dispatch(new EditReport());
  }
}
