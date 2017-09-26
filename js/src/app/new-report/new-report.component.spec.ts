import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewReportComponent } from './new-report.component';

describe('NewReportComponent', () => {
  let component: NewReportComponent;
  let fixture: ComponentFixture<NewReportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewReportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
