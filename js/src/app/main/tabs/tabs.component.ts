import { Component, OnInit, ViewEncapsulation, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { ChangeTab } from '../../actions/reports';
import { UpdateOne, DeleteOne } from '../../actions/display-field';
import { State, getActiveTab, getDisplayFields } from '../../reducers';
import { MatTabGroup } from '@angular/material';
import { Update } from '@ngrx/entity';
import { IDisplayField } from '../../api.interfaces';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.component.html',
  styleUrls: ['./tabs.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class TabsComponent implements OnInit {
  constructor(private store: Store<State>) {}
  displayFields$ = this.store.select(getDisplayFields);
  activeTab$ = this.store.select(getActiveTab);
  @ViewChild('tabs') tabs: MatTabGroup;

  tabChange(index: number) {
    this.store.dispatch(new ChangeTab(index));
  }

  updateDisplayField(update: Update<IDisplayField>) {
    this.store.dispatch(new UpdateOne(update));
  }

  deleteDisplayField(id: number) {
    this.store.dispatch(new DeleteOne(id));
  }

  ngOnInit() {
    this.activeTab$.subscribe(number => (this.tabs.selectedIndex = number));
  }
}
