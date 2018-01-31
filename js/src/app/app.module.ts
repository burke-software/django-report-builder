import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { TreeModule } from 'angular-tree-component';
import { MatSortModule } from '@angular/material/sort';

import {
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatInputModule,
  MatToolbarModule,
  MatSelectModule,
  MatSidenavModule,
  MatTabsModule
} from '@angular/material';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';

import { AppComponent } from './app.component';
import { NewReportComponent } from './new-report/new-report.component';
import { MainComponent } from './main/main.component';
import { LeftSidebarComponent } from './main/left-sidebar/';

import { ApiService } from './api.service';

import { reducers, metaReducers } from './reducers';
import { ReportEffects } from './effects/reports';
import { ConfigEffects } from './effects/config';
import { HeaderComponent } from './header/header.component';
import { TabsComponent } from './main/tabs/tabs.component';
import { OptionsTabComponent } from './main/tabs/options-tab/options-tab.component';
import { CopyReportComponent } from './main/tabs/options-tab/copy-report.component';
import { LastReportComponent } from './main/tabs/options-tab/last-report.component';
import { ReportTabComponent } from './main/tabs/report-tab/report-tab.component';
import { ReportPreviewComponent } from './main/tabs/report-tab/report-preview.component';
import { SavedTimestampComponent } from './main/tabs/report-tab/saved-timestamp.component';
import { RightSidebarComponent } from './main/right-sidebar/right-sidebar.component';
import { RelatedFieldComponent } from './main/right-sidebar/related-field.component';
import { ClickOutsideModule } from 'ng4-click-outside';

const appRoutes: Routes = [
  { path: '', component: MainComponent, data: { title: 'Reports' } },
  {
    path: 'report/add',
    component: NewReportComponent,
    data: { title: 'Add New Report' }
  },
  { path: 'report/:id', component: MainComponent, data: { title: 'Report' } }
];

export const MatModules = [
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatInputModule,
  MatToolbarModule,
  MatSelectModule,
  MatSidenavModule,
  MatTabsModule
];

@NgModule({
  declarations: [
    AppComponent,
    NewReportComponent,
    MainComponent,
    LeftSidebarComponent,
    HeaderComponent,
    TabsComponent,
    OptionsTabComponent,
    CopyReportComponent,
    LastReportComponent,
    ReportTabComponent,
    ReportPreviewComponent,
    SavedTimestampComponent,
    RightSidebarComponent,
    RelatedFieldComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    ClickOutsideModule,
    RouterModule.forRoot(appRoutes),
    StoreModule.forRoot(reducers, { metaReducers }),
    StoreDevtoolsModule.instrument({ maxAge: 25 }),
    EffectsModule.forRoot([ReportEffects, ConfigEffects]),
    HttpClientModule,
    TreeModule,
    MatSortModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    FormsModule,
    ...MatModules
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule {}
