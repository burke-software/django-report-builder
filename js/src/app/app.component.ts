import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import { Router, RoutesRecognized } from '@angular/router';
import { Store } from '@ngrx/store';
import { State } from './reducers';
import { GetReport } from './actions/reports';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store<State>,
  ) {
    let firstLoad = true;
    router.events.subscribe((event) => {
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
  }
}
