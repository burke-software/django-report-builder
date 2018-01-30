import { Component, OnInit, ViewEncapsulation, ViewChild } from '@angular/core';
import { Store } from '@ngrx/store';
import { ChangeTab } from '../../actions/reports';
import { State, getActiveTab, getDisplayFields } from '../../reducers';
import { MatTabGroup } from '@angular/material';

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

  ngOnInit() {
    this.activeTab$.subscribe(number => (this.tabs.selectedIndex = number));
  }
}
