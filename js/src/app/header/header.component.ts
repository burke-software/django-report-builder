import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  @Input() title: string;
  @Input() reportName: string;
  @Input() showRightNavButton: boolean;
  @Output() onToggleRightNav = new EventEmitter();
  @Output() changeTitleInput = new EventEmitter();
  @Output() goHome = new EventEmitter();

  clickGoHome(event: MouseEvent) {
    event.preventDefault();
    this.goHome.emit();
  }
}
