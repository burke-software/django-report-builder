import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { FormsModule } from '@angular/forms';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { of } from 'rxjs';

import { MatModules } from '../app.module';
import { ApiService } from '../api.service';
import { NewReportComponent } from './new-report.component';

class FakeApiService {
  getRootModels() {
    const contentTypes = [
      { pk: 1, name: 'log entry' },
      { pk: 2, name: 'permission' },
    ];
    return of(contentTypes);
  }
}

xdescribe('NewReportComponent', () => {
  let component: NewReportComponent;
  let fixture: ComponentFixture<NewReportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NewReportComponent],
      imports: [
        ...MatModules,
        RouterTestingModule,
        FormsModule,
        NoopAnimationsModule,
      ],
      providers: [{ provide: ApiService, useClass: FakeApiService }],
    }).compileComponents();
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
