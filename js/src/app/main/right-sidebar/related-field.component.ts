import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IRelatedField } from '../../api.interfaces';

@Component({
  selector: 'app-related-field',
  template: `
  <div *ngFor="let relatedField of relatedFields">
    <span (click)="selectRelatedField.emit(relatedField)">{{ relatedField.verbose_name }}</span>
    <app-related-field [relatedFields]="relatedFields.children">
    </app-related-field>
  </div>
  `,
})
export class RelatedFieldComponent {
  @Input() relatedFields: IRelatedField[];
  @Output() selectRelatedField = new EventEmitter<IRelatedField>();

  constructor() { }
}
