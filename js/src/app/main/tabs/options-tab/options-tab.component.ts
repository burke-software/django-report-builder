import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { State } from '../../../reducers';
import { getDescriptionInput, getIsDistinct } from '../../../selectors';
import {
  ChangeReportDescription,
  ToggleReportDistinct,
  DeleteReport,
  CopyReport,
} from '../../../actions/reports';
import { MatDialog } from '@angular/material/dialog';
import { IReportDetailed } from '../../../models/api';
import {
  ConfirmModalComponent,
  IConfirmModalData,
} from '../../../confirm/confirm-modal.component';

@Component({
  selector: 'app-options-tab',
  templateUrl: './options-tab.component.html',
})
export class OptionsTabComponent {
  constructor(private store: Store<State>, public dialog: MatDialog) {}

  descriptionInput$ = this.store.select(getDescriptionInput);
  isChecked$ = this.store.select(getIsDistinct);
  @Input() report: IReportDetailed;

  onChange(value: string) {
    this.store.dispatch(new ChangeReportDescription(value));
  }

  onClick(value: boolean) {
    this.store.dispatch(new ToggleReportDistinct(value));
  }

  onDelete(e: MouseEvent) {
    e.preventDefault();

    const dialogRef = this.dialog.open(ConfirmModalComponent, {
      data: {
        title: `Are you sure you want to delete ${this.report.name}`,
        subtitle: 'You will not be able to undo this action.',
        confirmText: 'Delete',
      } as IConfirmModalData,
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.store.dispatch(new DeleteReport(this.report.id));
      }
    });
  }

  copyReport(e: MouseEvent) {
    e.preventDefault();
    this.store.dispatch(new CopyReport(this.report.id));
  }
}
