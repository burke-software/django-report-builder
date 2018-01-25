import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatModules } from '../../app.module';
import { RightSidebarComponent } from './right-sidebar.component';
import { RelatedFieldComponent } from './related-field.component';

describe('RightSidebarComponent', () => {
  let component: RightSidebarComponent;
  let fixture: ComponentFixture<RightSidebarComponent>;

  beforeEach(
    async(() => {
      TestBed.configureTestingModule({
        declarations: [RightSidebarComponent, RelatedFieldComponent],
        imports: [...MatModules, NoopAnimationsModule]
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(RightSidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
