import { Component, Input } from '@angular/core';
import { IRelatedField } from '../../api.interfaces';

@Component({
  selector: 'app-related-field',
  template: `
  <div *ngFor="let relatedField of relatedFields">
    {{ relatedField.verbose_name }}
    <app-related-field relatedFields="relatedFields.children">
    </app-related-field>

  </div>
  `,
})
export class RelatedFieldComponent {
  @Input() relatedFields: IRelatedField[];

  constructor() { }
}

