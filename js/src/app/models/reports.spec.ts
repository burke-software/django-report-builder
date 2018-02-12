import { createPositionEntityAdapter } from './reports';

describe('createPositionEntityAdapter', () => {
  interface IPositionThing {
    tempid: number;
    position: number;
  }
  const adapter = createPositionEntityAdapter<IPositionThing>();
  const selectors = adapter.getSelectors();
  const state = adapter.addMany(
    [
      { position: 0, tempid: 0 },
      { position: 1, tempid: 1 },
      { position: 2, tempid: 2 },
      { position: 3, tempid: 3 },
      { position: 4, tempid: 4 },
    ],
    adapter.getInitialState()
  );

  it('removeOne should update all greater positions if one is removed', () => {
    const newState = adapter.removeOne(1, state);
    const expected = [
      { position: 0, tempid: 0 },
      { position: 1, tempid: 2 },
      { position: 2, tempid: 3 },
      { position: 3, tempid: 4 },
    ];
    expected.forEach(obj =>
      expect(selectors.selectAll(newState)).toContain(
        jasmine.objectContaining(obj)
      )
    );
  });

  it('updateOne should shift positions if one is updated', () => {
    const newState = adapter.updateOne(
      { id: 1, changes: { position: 3 } },
      state
    );
    const expected = [
      { position: 0, tempid: 0 },
      { position: 1, tempid: 2 },
      { position: 2, tempid: 3 },
      { position: 3, tempid: 1 },
      { position: 4, tempid: 4 },
    ];
    expected.forEach(obj =>
      expect(selectors.selectAll(newState)).toContain(
        jasmine.objectContaining(obj)
      )
    );
  });
});
