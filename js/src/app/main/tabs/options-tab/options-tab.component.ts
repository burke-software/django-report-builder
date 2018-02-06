import { Component, Output, EventEmitter } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../../reducers';
import {
  getDescriptionInput,
  getIsDistinct,
  getSelectedReportId,
  getLastGeneratedReport,
} from '../../../selectors';
import {
  ChangeReportDescription,
  ToggleReportDistinct,
  DeleteReport,
} from '../../../actions/reports';

@Component({
  selector: 'app-options-tab',
  template: `
  <div class="options-tab">
  <mat-list class="options-content"><form>

    <mat-list-item>
      <mat-form-field>
        <input matInput placeholder="Description" [value]="descriptionInput$ | async" (keyup)="onChange($event.currentTarget.value)" >
      </mat-form-field>
    </mat-list-item>

    <mat-list-item>
    <mat-checkbox matListIcon class="checkbox-icon" [checked]="isChecked$ | async" (change)="onClick($event.checked)"></mat-checkbox>
    <span class="checkbox-label" matLine>Is Distinct (maybe help reduce duplicate rows). Read
      <a
        href="https://docs.djangoproject.com/en/2.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct"
      target="_blank">more
      </a>.
    </span>
    </mat-list-item>

    <mat-list-item (click)="onDelete($event)" class="icon-link" ><mat-icon matListIcon>delete</mat-icon><a matLine href="#" alt="Delete this report">Delete this report</a></mat-list-item>
    
    <app-copy-report *ngIf="copyId$ | async" [id]="copyId$ | async"></app-copy-report>

    <app-last-report *ngIf="lastGeneratedReport$ | async" [report]="lastGeneratedReport$ | async"></app-last-report>
  </form></mat-list>
  </div>
  `,
})
export class OptionsTabComponent {
  descriptionInput$ = this.store.select(getDescriptionInput);
  isChecked$ = this.store.select(getIsDistinct);
  copyId$ = this.store.select(getSelectedReportId);
  lastGeneratedReport$ = this.store.select(getLastGeneratedReport);
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

  constructor(private store: Store<State>) {}
}
