import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IRelatedField } from '../../api.interfaces';

@Component({
  selector: 'app-related-field',
  template: `
  <div *ngFor="let relatedField of relatedFields">
    <span (click)="selectRelatedField.emit(relatedField)">{{ relatedField.verbose_name }}</span>
    <app-related-field [relatedFields]="relatedField.children" (selectRelatedField)="selectRelatedField.emit($event)">
    </app-related-field>
  </div>
  `,
})
export class RelatedFieldComponent {
  @Input() relatedFields: IRelatedField[];
  @Output() selectRelatedField = new EventEmitter<IRelatedField>();

  constructor() { }

  nodes = [
    {
      id: 1,
      name: 'root1',
      children: [
        { id: 2, name: 'child1' },
        { id: 3, name: 'child2' }
      ]
    },
    {
      id: 4,
      name: 'root2',
      children: [
        { id: 5, name: 'child2.1' },
        {
          id: 6,
          name: 'child2.2',
          children: [
            { id: 7, name: 'subsub' }
          ]
        }
      ]
    }
  ];
  options = this.relatedFields;
}

