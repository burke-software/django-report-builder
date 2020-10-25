import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {
  HttpClientModule,
  HttpClientXsrfModule,
  HTTP_INTERCEPTORS,
} from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { TreeModule } from '@circlon/angular-tree-component';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { LayoutModule } from '@angular/cdk/layout';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import {
  StoreRouterConnectingModule,
  RouterStateSerializer, DefaultRouterStateSerializer,
} from '@ngrx/router-store';

import { AppComponent } from './app.component';
import { NewReportComponent } from './new-report/new-report.component';
import { HomeComponent } from './home/home.component';
import { MainComponent } from './main/main.component';

import { ApiService } from './api.service';

import { reducers, metaReducers, CustomSerializer } from './reducers';
import { ReportEffects } from './effects/reports';
import { ConfigEffects } from './effects/config';
import { RouterEffects } from './effects/router';
import { HeaderComponent } from './header/header.component';
import { ConfirmModalComponent } from './confirm/confirm-modal.component';
import { TabsComponent } from './main/tabs/tabs.component';
import { OptionsTabComponent } from './main/tabs/options-tab/options-tab.component';
import { ReportTabComponent } from './main/tabs/report-tab/report-tab.component';
import { ReportPreviewComponent } from './main/tabs/report-tab/report-preview.component';
import { SavedTimestampComponent } from './main/tabs/report-tab/saved-timestamp.component';
import { LastReportComponent } from './main/tabs/report-tab/last-report.component';
import { DisplayTabComponent } from './main/tabs/display-tab/display-tab.component';
import { DisplayTabRowComponent } from './main/tabs/display-tab/display-tab-row.component';
import { FilterTabComponent } from './main/tabs/filter-tab/filter-tab.component';
import { FilterTabRowComponent } from './main/tabs/filter-tab/filter-tab-row.component';
import { RightSidebarComponent } from './main/right-sidebar/right-sidebar.component';
import { FieldComponent } from './main/right-sidebar/field.component';
import { ClickOutsideModule } from 'ng4-click-outside';
import { PendingChangesGuard } from './generic.guard';
import { ErrorComponent } from './error/error.component';
import { NetworkErrorInterceptor } from './api.interceptor';
import { FilterInputComponent } from './main/tabs/filter-tab/filter-input.component';

const appRoutes: Routes = [
  { path: '', component: HomeComponent, data: { title: 'Reports' } },
  {
    path: 'report/add',
    component: NewReportComponent,
    data: { title: 'Add New Report' },
  },
  {
    path: 'report/:id',
    component: MainComponent,
    data: { title: 'Report' },
    canDeactivate: [PendingChangesGuard],
  },
];

export const MatModules = [
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatDatepickerModule,
  MatDialogModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatMomentDateModule,
  MatProgressBarModule,
  MatSelectModule,
  MatSidenavModule,
  MatSnackBarModule,
  MatSortModule,
  MatToolbarModule,
  MatTooltipModule,
  MatTabsModule,
  MatTableModule,
  LayoutModule,
];

@NgModule({
  declarations: [
    AppComponent,
    NewReportComponent,
    HomeComponent,
    MainComponent,
    HeaderComponent,
    ConfirmModalComponent,
    TabsComponent,
    OptionsTabComponent,
    LastReportComponent,
    ReportTabComponent,
    ReportPreviewComponent,
    SavedTimestampComponent,
    DisplayTabComponent,
    DisplayTabRowComponent,
    FilterTabComponent,
    FilterTabRowComponent,
    FilterInputComponent,
    RightSidebarComponent,
    FieldComponent,
    ErrorComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    ClickOutsideModule,
    StoreModule.forRoot(reducers, { metaReducers }),
    RouterModule.forRoot(appRoutes),
    StoreRouterConnectingModule.forRoot({ serializer: DefaultRouterStateSerializer,
      stateKey: 'router',
    }),
    StoreDevtoolsModule.instrument({ maxAge: 25 }),
    EffectsModule.forRoot([ReportEffects, ConfigEffects, RouterEffects]),
    HttpClientModule,
    TreeModule,
    MatSortModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken',
    }),
    FormsModule,
    ...MatModules,
  ],
  providers: [
    ApiService,
    { provide: RouterStateSerializer, useClass: CustomSerializer },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: NetworkErrorInterceptor,
      multi: true,
    },
    PendingChangesGuard,
  ],
  bootstrap: [AppComponent],
  entryComponents: [ConfirmModalComponent],
})
export class AppModule {}
