import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-saved-timestamp',
  template: `<span class="saved-timestamp">{{this.lastSaved ? 'Last saved: ' + this.lastSaved : this.notSaved}}</span>`,
})
export class SavedTimestampComponent {
  constructor() {}
  @Input() lastSaved?: Date;
  notSaved = 'Report has not been saved';
}
