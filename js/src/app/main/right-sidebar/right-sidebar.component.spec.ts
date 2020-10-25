import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatModules } from '../../app.module';
import { RightSidebarComponent } from './right-sidebar.component';
import { ClickOutsideModule } from 'ng4-click-outside';
import { TreeModule } from '@circlon/angular-tree-component';

describe('RightSidebarComponent', () => {
  let component: RightSidebarComponent;
  let fixture: ComponentFixture<RightSidebarComponent>;

  beforeEach(
    async(() => {
      TestBed.configureTestingModule({
        declarations: [RightSidebarComponent],
        imports: [
          ...MatModules,
          NoopAnimationsModule,
          ClickOutsideModule,
          TreeModule,
        ],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(RightSidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  xit('should create', () => {
    expect(component).toBeTruthy();
  });
});
