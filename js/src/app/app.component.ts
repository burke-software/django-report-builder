import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import { Router, RoutesRecognized } from '@angular/router';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title: string;

  constructor(private route: ActivatedRoute, private router: Router) {
    router.events.subscribe((event) => {
      if (event instanceof RoutesRecognized) {
        const child = event.state.root.firstChild;
        if (child && child.data) {
          this.title = child.data['title'];
        }
      }
    });
  }

  ngOnInit() {
  }
}
