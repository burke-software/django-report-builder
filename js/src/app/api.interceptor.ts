import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse,
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { _throw } from 'rxjs/observable/throw';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';
import 'rxjs/add/observable/empty';
import 'rxjs/add/operator/retry';

import { MatSnackBar } from '@angular/material';
import { Store } from '@ngrx/store';
import { State } from './reducers';
import { CancelGeneratePreview } from './actions/reports';

@Injectable()
export class NetworkErrorInterceptor implements HttpInterceptor {
  constructor(public snackBar: MatSnackBar, private store: Store<State>) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // Respect base URL tag
    const baseUrl = document.getElementsByTagName('base')[0].href;
    const apiReq = request.clone({ url: `${baseUrl}${request.url}` });

    return next.handle(apiReq).catch((err: HttpErrorResponse) => {
      if (err.status === 0 || err.status === 500) {
        // An error we can't help with happened, one of:
        // 1. Network error
        // 2. Client side JS error
        // 3. Server side 500 error
        this.store.dispatch(new CancelGeneratePreview());
        this.snackBar.open('Sorry, something went wrong!');
        return Observable.empty<HttpEvent<any>>();
      }
      return _throw(err.error);
    });
  }
}
