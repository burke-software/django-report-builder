import {
  Component,
  Input,
  Output,
  EventEmitter,
  OnChanges,
} from '@angular/core';

@Component({
  selector: 'app-filter-input',
  templateUrl: './filter-input.component.html',
})
export class FilterInputComponent implements OnChanges {
  @Input() value: string;
  @Input() filterType: string;
  @Input() fieldType: string;
  @Output() change = new EventEmitter<any>();
  date?: string;
  time?: string;

  ngOnChanges() {
    if (/Date/.test(this.fieldType)) {
      const [date, time] = this.value.split(' ');
      this.date = date;
      this.time = time;
    }
  }

  getBoolean() {
    return this.value === 'True';
  }

  emitBoolean(value: boolean) {
    this.change.emit(value ? 'True' : 'False');
  }

  onDateChange(date: string) {
    this.date = date;
    this.emitDateTime();
  }

  emitDateTime() {
    let result = this.date;
    if (this.time) {
      result += ' ' + this.time;
    }
    this.change.emit(result);
  }
}
