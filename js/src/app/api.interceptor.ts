import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse,
} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Store } from '@ngrx/store';
import { Observable, throwError, EMPTY } from 'rxjs';
import { catchError } from 'rxjs/operators';

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

    return next.handle(apiReq).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 0 || err.status === 500) {
          // An error we can't help with happened, one of:
          // 1. Network error
          // 2. Client side JS error
          // 3. Server side 500 error
          this.store.dispatch(new CancelGeneratePreview());
          this.snackBar.open('Sorry, something went wrong!', '', {
            duration: 5000,
          });
          return EMPTY;
        }
        return throwError(err.error);
      })
    );
  }
}
