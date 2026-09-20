// configurateur.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Configuration } from '../models/configuration.model';

@Injectable({ providedIn: 'root' })
export class ConfigurateurService {
  private readonly baseUrl = `${environment.apiUrl}/configurateur/configurations`;

  constructor(private http: HttpClient) {}

  creer(config: Partial<Configuration>): Observable<Configuration> {
    return this.http.post<Configuration>(`${this.baseUrl}/`, config);
  }

  mettreAJour(id: number, config: Partial<Configuration>): Observable<Configuration> {
    return this.http.patch<Configuration>(`${this.baseUrl}/${id}/`, config);
  }

  obtenir(id: number): Observable<Configuration> {
    return this.http.get<Configuration>(`${this.baseUrl}/${id}/`);
  }

  listerMesConfigurations(): Observable<{ results: Configuration[] }> {
    return this.http.get<{ results: Configuration[] }>(`${this.baseUrl}/`);
  }
}
