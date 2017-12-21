import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import {
  MatButtonModule,
  MatCheckboxModule,
  MatInputModule,
  MatToolbarModule,
  MatSelectModule,
  MatSidenavModule,
  MatTabsModule,
} from '@angular/material';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';

import { environment } from '../environments/environment';

import { AppComponent } from './app.component';
import { NewReportComponent } from './new-report/new-report.component';
import { MainComponent } from './main/main.component';
import { LeftSidebarComponent } from './main/left-sidebar/';

import { ApiService } from './api.service';

import { reducers, metaReducers } from './reducers';
import { ReportEffects } from './effects/reports';
import { HeaderComponent } from './header/header.component';
import { TabsComponent } from './main/tabs/tabs.component';
import { RightSidebarComponent } from './main/right-sidebar/right-sidebar.component';
import { RelatedFieldComponent } from './main/right-sidebar/related-field.component';

const appRoutes: Routes = [
  { path: '', component: MainComponent, data: {title: 'Reports'}},
  { path: 'report/add', component: NewReportComponent, data: {title: 'Add New Report'} },
  { path: 'report/:id', component: MainComponent, data: {title: 'Report'}},
];

export const MatModules = [
  MatButtonModule,
  MatCheckboxModule,
  MatInputModule,
  MatToolbarModule,
  MatSelectModule,
  MatSidenavModule,
  MatTabsModule,
];

@NgModule({
  declarations: [
    AppComponent,
    NewReportComponent,
    MainComponent,
    LeftSidebarComponent,
    HeaderComponent,
    TabsComponent,
    RightSidebarComponent,
    RelatedFieldComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    StoreModule.forRoot(reducers, { metaReducers }),
    !environment.production ? StoreDevtoolsModule.instrument() : [],
    EffectsModule.forRoot([ReportEffects]),
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
    FormsModule,
    ...MatModules,
  ],
  providers: [
    ApiService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
