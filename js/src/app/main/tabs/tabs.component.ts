import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../reducers';
import { ChangeTab } from '../../actions/reports';

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.component.html',
  styleUrls: ['./tabs.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class TabsComponent implements OnInit {
  constructor(private store: Store<State>) {}

  tabChange(index: number) {
    this.store.dispatch(new ChangeTab(index));
  }

  ngOnInit() {}
}
