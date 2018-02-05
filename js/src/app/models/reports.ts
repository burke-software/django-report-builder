import {
  IReport,
  IReportDetailed,
  INestedRelatedField,
  IField,
  IReportPreview,
  IDisplayField,
  IFilter,
} from './api';
import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: INestedRelatedField[];
  fields: IField[];
  title: string;
  descriptionInput: string;
  isDistinct: boolean;
  reportPreview?: IReportPreview;
  reportSaved?: Date;
  leftNavIsOpen: boolean;
  rightNavIsOpen: boolean;
  activeTab: number;
  displayFields: EntityState<IDisplayField>;
  filters: EntityState<IFilter>;
  selectedField?: IField;
  nextRelatedFieldId: number;
}

export const displayFieldAdapter: EntityAdapter<
  IDisplayField
> = createEntityAdapter<IDisplayField>({
  sortComparer: (x, y) => x.position - y.position,
  selectId: x => x.position,
});

export const filterAdapter: EntityAdapter<IFilter> = createEntityAdapter({
  sortComparer: (x, y) => x.position - y.position,
  selectId: x => x.position,
});
