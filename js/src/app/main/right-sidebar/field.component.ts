import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IField } from '../../models/api';

@Component({
  selector: 'app-field-component',
  template: `<div>
    <span (click)="selectField.emit(field)">{{field.name}}</span><mat-icon (click)="addReportField.emit(field)">add</mat-icon>
  </div>`,
})
export class FieldComponent {
  constructor() {}

  @Input() field: IField;
  @Output() addReportField = new EventEmitter<IField>();
  @Output() selectField = new EventEmitter<IField>();
}
