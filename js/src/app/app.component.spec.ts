import { TestBed, async } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { StoreModule } from '@ngrx/store';
import { AppComponent } from './app.component';
import { MatModules } from './app.module';
import { HeaderComponent } from './header/header.component';
import * as fromRoot from './reducers';

describe('AppComponent', () => {
  beforeEach(
    async(() => {
      TestBed.configureTestingModule({
        declarations: [AppComponent, HeaderComponent],
        imports: [
          RouterTestingModule,
          StoreModule.forRoot({
            ...fromRoot.reducers
          }),
          ...MatModules
        ]
      }).compileComponents();
    })
  );

  it(
    'should create the app',
    async(() => {
      const fixture = TestBed.createComponent(AppComponent);
      const app = fixture.debugElement.componentInstance;
      expect(app).toBeTruthy();
    })
  );
});
