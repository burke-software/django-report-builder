import {
  IReport,
  IReportDetailed,
  INestedRelatedField,
  IField,
  IReportPreview,
  IDisplayField,
  IFilter,
} from './api';
import {
  createEntityAdapter,
  EntityAdapter,
  EntityState,
  Update,
} from '@ngrx/entity';

export interface State {
  reports: IReport[];
  selectedReport: IReportDetailed | null;
  relatedFields: INestedRelatedField[];
  fields: IField[];
  title: string;
  titleInput: string;
  descriptionInput: string;
  isDistinct: boolean;
  reportPreview?: IReportPreview;
  reportSaved?: Date;
  rightNavIsOpen: boolean;
  activeTab: number;
  displayFields: EntityState<IDisplayField>;
  filters: EntityState<IFilter>;
  selectedField?: IField;
  nextRelatedFieldId: number;
  generatingReport: boolean;
  editedSinceLastSave: boolean;
  errors?: string[];
}

interface IHasPosition {
  position: number;
}

export function createPositionEntityAdapter<
  T extends IHasPosition
>(): EntityAdapter<T> {
  const adapter = createEntityAdapter<T>({
    sortComparer: (x, y) => x.position - y.position,
    selectId: x => x.position,
  });

  const selectors = adapter.getSelectors();

  const result = {
    ...adapter,
  };

  result.removeOne = (removedPos, state: EntityState<T>) => {
    state = adapter.removeOne(removedPos, state);
    return adapter.updateMany(
      selectors.selectAll(state).reduce(
        (updatelist, entity) => {
          if (entity.position > removedPos) {
            updatelist.push({
              id: entity.position,
              changes: {
                position: entity.position - 1,
              },
            } as Update<T>);
          }
          return updatelist;
        },
        [] as Update<T>[]
      ),
      state
    );
  };

  result.removeMany = (removedPositions, state) =>
    removedPositions.reduce((s, pos) => result.removeOne(pos, s), state);

  const getPositionUpdates = (
    oldPosition: number,
    newPosition: number,
    state: EntityState<T>
  ): Update<T>[] => {
    const changedPositions = inclusiveRange(oldPosition, newPosition);
    const isIncrease = oldPosition < newPosition;
    return selectors.selectAll(state).reduce((col, entity) => {
      if (changedPositions.includes(entity.position)) {
        const update: Update<T> = {
          id: entity.position,
          changes: {},
        };
        if (entity.position === oldPosition) {
          update.changes.position = newPosition;
        } else if (isIncrease) {
          update.changes.position = entity.position - 1;
        } else {
          update.changes.position = entity.position + 1;
        }
        return [...col, update];
      } else {
        return col;
      }
    }, []);
  };

  result.updateOne = (update, state) => {
    if ('position' in update.changes) {
      const updates = getPositionUpdates(
        update.id as number,
        update.changes.position,
        state
      );
      if (Object.keys(update.changes).length === 1) {
        return adapter.updateMany(updates, state);
      }
      update = {
        ...update,
        changes: Object.assign({}, update.changes),
      };
      delete update.changes.position;
      return adapter.updateMany([update, ...updates], state);
    } else {
      return adapter.updateOne(update, state);
    }
  };

  result.updateMany = (updates, state) =>
    updates.reduce((s, update) => result.updateOne(update, s), state);

  return result;
}

export const displayFieldAdapter: EntityAdapter<
  IDisplayField
> = createPositionEntityAdapter<IDisplayField>();

export const filterAdapter: EntityAdapter<
  IFilter
> = createPositionEntityAdapter();

function inclusiveRange(begin, end) {
  const result = [];
  for (let i = Math.min(begin, end); i <= Math.max(begin, end); i++) {
    result.push(i);
  }
  return result;
}
