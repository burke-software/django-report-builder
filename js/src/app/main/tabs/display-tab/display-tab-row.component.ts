import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IDisplayField } from '../../../models/api';
import { Update } from '@ngrx/entity';

@Component({
  selector: 'app-display-tab-row',
  templateUrl: './display-tab-row.component.html',
  styleUrls: ['../tabs.component.scss'],
})
export class DisplayTabRowComponent {
  constructor() {}
  @Input() field: IDisplayField;
  @Output() deleteField = new EventEmitter<number>();
  @Output() updateField = new EventEmitter<Update<IDisplayField>>();

  editField(changes) {
    this.updateField.emit({ changes, id: this.field.position });
  }
}
