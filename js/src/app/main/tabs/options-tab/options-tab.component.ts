import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getDescriptionInput } from '../../../reducers';
import { ChangeReportDescription } from '../../../actions/reports';

@Component({
  selector: 'app-options-tab',
  template: `
  <div><form>
    <div><mat-form-field>
      <input matInput placeholder="Description" [value]="descriptionInput$ | async" (keyup)="onChange($event.currentTarget.value)" >
    </mat-form-field></div>

    <div><mat-checkbox>Is Distinct</mat-checkbox></div>
    <div><a>Copy this report</a></div>
    <div><a>Delete this report</a></div>
    <div><a>Download existing report generated at</a></div>
  </form></div>
  `
})
export class OptionsTabComponent {
  descriptionInput$ = this.store.select(getDescriptionInput);
  @Output() changeDescription = new EventEmitter<string>();

  onChange(value: string) {
    this.store.dispatch(new ChangeReportDescription(value));
  }

  constructor(private store: Store<State>) { }
}
