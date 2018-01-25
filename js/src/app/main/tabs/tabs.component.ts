import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { ChangeTab } from '../../actions/reports';
import { State, getCurrentDisplayedFields } from '../../reducers';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.component.html',
  styleUrls: ['./tabs.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class TabsComponent implements OnInit {
  constructor(private store: Store<State>) {}
  displayFields$ = this.store.select(getCurrentDisplayedFields);

  tabChange(index: number) {
    this.store.dispatch(new ChangeTab(index));
  }

  ngOnInit() {}
}
