import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import { StoreModule } from '@ngrx/store';

import { MatModules } from '../app.module';
import { MainComponent } from './main.component';
import { LeftSidebarComponent } from './left-sidebar';

import { reducers } from '../reducers';

describe('MainComponent', () => {
  let component: MainComponent;
  let fixture: ComponentFixture<MainComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        MainComponent,
        LeftSidebarComponent
      ],
      imports: [
        ...MatModules,
        StoreModule.forRoot(reducers),
        NoopAnimationsModule,
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
