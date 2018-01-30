import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getSelectedReport } from '../reducers';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() title: string;
  @Output() onToggleLeftNav = new EventEmitter();
  @Output() onToggleRightNav = new EventEmitter();

  reportName: string;

  constructor(private store: Store<State>) {
    this.store.select(getSelectedReport).subscribe(report => {
      if (report) {
        this.reportName = report.name;
      } else {
        this.reportName = null;
      }
    });
  }

  ngOnInit() {}

  toggleLeftNav() {
    this.onToggleLeftNav.emit();
  }

  toggleRightNav() {
    this.onToggleRightNav.emit();
  }


}
