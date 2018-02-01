import { Component, OnInit, Input } from '@angular/core';
import { Router, RoutesRecognized } from '@angular/router';
import { Store } from '@ngrx/store';
import { State } from './reducers';
import { GetReport, GetTitle, ToggleRightNav, ToggleLeftNav } from './actions/reports';
import { GetConfig } from './actions/config';
import { IReportDetailed } from './api.interfaces';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  @Input() selectedReport: IReportDetailed;

  constructor(router: Router, private store: Store<State>) {
    let firstLoad = true;
    router.events.subscribe(event => {
      if (event instanceof RoutesRecognized) {
        const child = event.state.root.firstChild;
        if (child) {
          if (child.data) {
            this.store.dispatch(new GetTitle(child.data['title']))
          }
          // Load in report if user opened app from this url (instead of clicking)
          if (child.params && child.params['id'] && firstLoad) {
            this.store.dispatch(new GetReport(child.params['id']));
          }
          firstLoad = false;
        }
      }
    });
  }

  ngOnInit() {
    this.store.dispatch(new GetConfig());
  }

  onToggleLeftNav() {
    this.store.dispatch(new ToggleLeftNav());
  }

  onToggleRightNav() {
      this.store.dispatch(new ToggleRightNav());
  }

}
