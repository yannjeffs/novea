// reseau.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Concession } from '../models/concession.model';

@Injectable({ providedIn: 'root' })
export class ReseauService {
  private readonly baseUrl = `${environment.apiUrl}/concessions`;

  constructor(private http: HttpClient) {}

  listerConcessions(): Observable<{ results: Concession[] }> {
    return this.http.get<{ results: Concession[] }>(`${this.baseUrl}/`);
  }
}
