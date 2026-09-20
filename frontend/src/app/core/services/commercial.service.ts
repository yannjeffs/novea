// commercial.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { LeadCreation } from '../models/lead.model';

@Injectable({ providedIn: 'root' })
export class CommercialService {
  private readonly baseUrl = `${environment.apiUrl}/commercial`;

  constructor(private http: HttpClient) {}

  creerLead(lead: LeadCreation): Observable<LeadCreation> {
    return this.http.post<LeadCreation>(`${this.baseUrl}/leads/`, lead);
  }
}
