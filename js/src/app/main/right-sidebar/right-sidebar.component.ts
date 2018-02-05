import {
  Component,
  Input,
  Output,
  OnChanges,
  EventEmitter,
} from '@angular/core';
import { IField, IRelatedField } from '../../models/api';
import { MatTableDataSource } from '@angular/material';
import { TreeNode } from 'angular-tree-component';

@Component({
  selector: 'app-right-sidebar',
  templateUrl: './right-sidebar.component.html',
  styleUrls: ['./right-sidebar.component.scss'],
})
export class RightSidebarComponent implements OnChanges {
  @Input() modelName: string;
  @Input() selectedField: IField;

  @Output() selectRelatedField = new EventEmitter<IRelatedField>();
  @Output() onToggleRightNav = new EventEmitter();
  @Output() searchFields = new EventEmitter<string>();
  @Output() searchRelations = new EventEmitter<string>();

  @Input() rightNavIsOpen: boolean;
  @Output() addReportField = new EventEmitter<IField>();
  @Output() selectField = new EventEmitter<IField>();
  @Input() relatedFields: IRelatedField[];

  @Input()
  set fields(value: IField[]) {
    this.fieldDataSource = new MatTableDataSource(value);
  }

  fieldDataSource: MatTableDataSource<IField>;
  displayedColumnsField = ['name', 'button'];
  nodes: TreeNode[];

  ngOnChanges() {
    this.nodes = this.getRelatedFields();
  }

  constructor() {}

  toggleRightNav() {
    if (this.rightNavIsOpen === true) {
      this.onToggleRightNav.emit();
    }
  }

  onActivate($event) {
    this.selectRelatedField.emit($event);
  }

  filterTree(text, tree) {
    tree.treeModel.filterNodes(node => {
      return node.data.verbose_name.startsWith(text);
    });
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
  copy.children = copy.children.map(deepCopy);
  return copy;
}
