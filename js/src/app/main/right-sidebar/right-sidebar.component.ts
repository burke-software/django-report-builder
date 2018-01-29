import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IField, IRelatedField } from '../../api.interfaces';
import { TREE_ACTIONS, ITreeOptions } from 'angular-tree-component';


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
      },
    ];
    options: ITreeOptions = {
      isExpandedField: 'expanded',
      hasChildrenField: 'nodes',
      actionMapping: {
        mouse: {
          dblClick: (tree, node, $event) => {
            if (node.hasChildren) { 
              TREE_ACTIONS.TOGGLE_EXPANDED(tree, node, $event); 
            }
          }
        },
      },
    };

    handler($event) {
      this.selectRelatedField.emit($event);
    }
    
    getRelatedFields() {
       return this.relatedFields
      .map(deepCopy);
    }

}

 function deepCopy(obj) {
   const copy = {...obj};
   copy.name = copy.verbose_name;
   copy.id = copy.model_id;
   copy.children = copy.children.map(deepCopy);
   return copy;
 }
