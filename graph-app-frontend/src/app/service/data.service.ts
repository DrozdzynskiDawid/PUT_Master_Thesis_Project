import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private http = inject(HttpClient);
  textFromDataset = signal<string>('');
  hypergraphJsonData = signal<any>(null);

  sendPostRequestJson<T>(url: string, body: any): Observable<T> {
    return this.http.post<T>(url, body);
  }

  sendPostRequestBlob(url: string, body: any): Observable<Blob> {
    return this.http.post(url, body, { responseType: 'blob' });
  }

  sendGetRequest<T>(url: string): Observable<T> {
    return this.http.get<T>(url);
  }
}