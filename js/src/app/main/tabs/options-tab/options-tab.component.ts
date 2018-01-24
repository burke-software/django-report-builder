import { Component, Output, EventEmitter } from '@angular/core';
import { Store } from '@ngrx/store';
import { State, getDescriptionInput, getIsDistinct, getSelectedReportId } from '../../../reducers';
import { ChangeReportDescription, ToggleReportDistinct, DeleteReport } from '../../../actions/reports';

@Component({
  selector: 'app-options-tab',
  template: `
  <div><form>
    <div><mat-form-field>
      <input matInput placeholder="Description" [value]="descriptionInput$ | async" (keyup)="onChange($event.currentTarget.value)" >
    </mat-form-field></div>

    <div>
      <mat-checkbox [checked]="isChecked$ | async" (change)="onClick($event.checked)">
        Is Distinct (maybe help reduce duplicate rows) Read&nbsp;
        <a
          href="https://docs.djangoproject.com/en/2.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct"
        target="_blank">more</a>.
      </mat-checkbox>
    </div>
    <div><a (click)="onDelete($event)" href="#" alt="Delete this report">Delete this report</a></div>
    <app-copy-report *ngIf="copyId$ | async" [id]="copyId$ | async"></app-copy-report>
    <div><a>Download existing report generated at</a></div>
  </form></div>
  `
})
export class OptionsTabComponent {
  descriptionInput$ = this.store.select(getDescriptionInput);
  isChecked$ = this.store.select(getIsDistinct);
  copyId$ = this.store.select(getSelectedReportId);
  @Output() changeDescription = new EventEmitter<string>();

  onChange(value: string) {
    this.store.dispatch(new ChangeReportDescription(value));
  }

  onClick(value: boolean) {
    this.store.dispatch(new ToggleReportDistinct(value));
  }

  onDelete(e: MouseEvent) {
    e.preventDefault();
    this.store.dispatch(new DeleteReport());
  }

  constructor(private store: Store<State>) { }
}
