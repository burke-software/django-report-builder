import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IField, IRelatedField } from '../../api.interfaces';
import { MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-right-sidebar',
  templateUrl: './right-sidebar.component.html',
  styleUrls: ['./right-sidebar.component.scss'],
})
export class RightSidebarComponent {
  @Input() modelName: string;
  @Input() relatedFields: IRelatedField[] = [];
  @Input() selectedField: IField;

  @Output() selectRelatedField = new EventEmitter<IRelatedField>();
  @Output() onToggleRightNav = new EventEmitter();
  @Output() searchFields = new EventEmitter<string>();
  @Output() searchRelations = new EventEmitter<string>();

  @Input() rightNavIsOpen: boolean;
  @Output() addReportField = new EventEmitter<IField>();
  @Output() selectField = new EventEmitter<IField>();

  @Input() 
  set fields(value: IField[]) {
    this.fieldDataSource = new MatTableDataSource(value);
  };

    fieldDataSource: MatTableDataSource<IField>;
  
    displayedColumnsField = ['name'];

  constructor() {}

  toggleRightNav() {
    if (this.rightNavIsOpen === true) {
      this.onToggleRightNav.emit();
    }
  }

  onActivate($event) {
    this.selectRelatedField.emit($event);
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim(); 
    filterValue = filterValue.toLowerCase();
    this.fieldDataSource.filter = filterValue;
  }

    getRelatedFields() {
      return this.relatedFields.map(deepCopy);
   }

}

function deepCopy(obj) {
  const copy = { ...obj };
  copy.name = copy.verbose_name;
  copy.id = copy.model_id;
  copy.children = copy.children.map(deepCopy);
  return copy;
}
