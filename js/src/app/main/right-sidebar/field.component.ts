import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IField } from '../../api.interfaces';

@Component({
  selector: 'app-field-component',
  template: `<div>
    <span (click)="addReportField.emit(field)">{{field.name}}</span>
  </div>`
})
export class FieldComponent {
  constructor() {}

  @Input() field: IField;
  @Output() addReportField = new EventEmitter<IField>();
}
