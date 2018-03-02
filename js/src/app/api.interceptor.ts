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

@Injectable()
export class NetworkErrorInterceptor implements HttpInterceptor {
  constructor(public snackBar: MatSnackBar) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).catch((err: HttpErrorResponse) => {
      if (err.status === 0) {
        // Client-side or network error happened
        this.snackBar.open('Sorry, something went wrong!');
        return Observable.empty<HttpEvent<any>>();
      }
      return _throw(err.error);
    });
  }
}
