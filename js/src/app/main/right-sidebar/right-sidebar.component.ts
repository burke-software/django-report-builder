import {
  Component,
  Input,
  Output,
  OnChanges,
  EventEmitter,
  ViewChild,
} from '@angular/core';
import { IField, IRelatedField } from '../../models/api';
import { MatTableDataSource } from '@angular/material/table';
import { TreeNode } from '@circlon/angular-tree-component';
import { ITreeNode } from '@circlon/angular-tree-component/lib/defs/api';

@Component({
  selector: 'app-right-sidebar',
  templateUrl: './right-sidebar.component.html',
  styleUrls: ['./right-sidebar.component.scss'],
})
export class RightSidebarComponent implements OnChanges {
  @Input() modelName: string;
  @Input() selectedField: IField;
  @Input() lockOpen: boolean;
  @Output() close = new EventEmitter();

  @Output() selectRelatedField = new EventEmitter<IRelatedField>();
  @Output() expandRelatedField = new EventEmitter<IRelatedField>();
  @Output() searchFields = new EventEmitter<string>();
  @Output() searchRelations = new EventEmitter<string>();

  @Output() addReportField = new EventEmitter<IField>();
  @Output() selectField = new EventEmitter<IField>();
  @Input() relatedFields: IRelatedField[];

  @Input()
  set fields(value: IField[]) {
    this.fieldDataSource = new MatTableDataSource(value);
  }

  @ViewChild('searchFields', { static: true }) searchInput

  fieldDataSource: MatTableDataSource<IField>;
  displayedColumnsField = ['name', 'button'];
  nodes: TreeNode[];

  ngOnChanges() {
    this.nodes = this.getRelatedFields();
  }

  constructor() {}

  onExpand({ node, isExpanded }: { node: ITreeNode; isExpanded: boolean }) {
    if (isExpanded) {
      this.expandRelatedField.emit(node.data);
    }
  }

  onActivate({ node }: { node: ITreeNode }) {
    this.selectRelatedField.emit(node.data);
    this.searchInput.nativeElement.value = ''
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
  copy.hasChildren = true;
  return copy;
}
