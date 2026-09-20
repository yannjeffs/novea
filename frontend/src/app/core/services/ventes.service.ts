// ventes.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Commande } from '../models/commande.model';

@Injectable({ providedIn: 'root' })
export class VentesService {
  private readonly baseUrl = `${environment.apiUrl}/ventes`;

  constructor(private http: HttpClient) {}

  listerMesCommandes(): Observable<{ results: Commande[] }> {
    return this.http.get<{ results: Commande[] }>(`${this.baseUrl}/commandes/`);
  }

  obtenirCommande(id: number): Observable<Commande> {
    return this.http.get<Commande>(`${this.baseUrl}/commandes/${id}/`);
  }
}
