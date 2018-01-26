import { Component, OnInit } from '@angular/core';
import { Router, RoutesRecognized } from '@angular/router';
import { Store } from '@ngrx/store';
import { State } from './reducers';
import { GetReport, ShowReports } from './actions/reports';
import { GetConfig } from './actions/config';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title: string;

  constructor(router: Router, private store: Store<State>) {
    let firstLoad = true;
    router.events.subscribe(event => {
      if (event instanceof RoutesRecognized) {
        const child = event.state.root.firstChild;
        if (child) {
          if (child.data) {
            this.title = child.data['title'];
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

  onToggleNav() {
    this.store.dispatch(new ShowReports());
  }


}
