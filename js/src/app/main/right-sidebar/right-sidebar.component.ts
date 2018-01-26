import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IField, IRelatedField } from '../../api.interfaces';

@Component({
  selector: 'app-right-sidebar',
  templateUrl: './right-sidebar.component.html',
  styleUrls: ['./right-sidebar.component.scss']
})
export class RightSidebarComponent {
  @Input() modelName: string;
  @Input() fields: IField[];
  @Input() relatedFields: IRelatedField[];
  @Output() selectRelatedField = new EventEmitter<IRelatedField>();

  constructor() {}
}
