import {
  Component,
  Input,
  Output,
  EventEmitter,
  OnChanges,
} from '@angular/core';

// Delete when you switch to a real datetime picker
interface IDateTimeOption {
  display: string;
  value: string;
}

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
  timeOpts: IDateTimeOption[];

  constructor() {
    // this code is ugly and Dog willing can be deleted when Angular Material adds a datetime input
    // until that day I will describe what it does in comments because it's real imperative
    const timeOpts = [];
    for (let x = 0; x < 24; x += 0.5) {
      // go through numbers from 0.0 to 23.5
      const hour = Math.floor(x); // ignore the decimal to get the hour
      const displayHour = hour % 12 === 0 ? '12' : String(hour % 12); // display 12-hour clock times
      const valueHour = hour < 10 ? '0' + hour : String(hour); // use two digit 24-hour clock times for the value
      const ampm = hour < 12 ? 'AM' : 'PM'; // before noon display AM, after PM
      const minutes = x === Math.floor(x) ? '00' : '30'; // 0.0 = on the hour, 0.5 = on the half hour

      timeOpts.push({
        display: `${displayHour}:${minutes} ${ampm}`,
        value: `${valueHour}:${minutes}`,
      } as IDateTimeOption);
    }
    this.timeOpts = timeOpts;
  }

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

  onTimeChange(time) {
    this.time = time;
    this.emitDateTime();
  }

  emitDateTime() {
    let result = this.date;
    if (this.fieldType === 'DateTimeField') {
      result += ' ' + (this.time || '00:00');
    }
    this.change.emit(result);
  }
}
