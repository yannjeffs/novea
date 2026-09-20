// catalogue.service.ts
import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { OptionPack, VehiculeDetail, VehiculeListe } from '../models/vehicule.model';

interface Paginee<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class CatalogueService {
  private readonly baseUrl = `${environment.apiUrl}/vehicules`;

  constructor(private http: HttpClient) {}

  listerVehicules(filtres?: {
    energie?: string;
    carrosserie?: string;
    ordering?: string;
  }): Observable<Paginee<VehiculeListe>> {
    let params = new HttpParams();
    if (filtres?.energie) params = params.set('energie', filtres.energie);
    if (filtres?.carrosserie) params = params.set('carrosserie', filtres.carrosserie);
    if (filtres?.ordering) params = params.set('ordering', filtres.ordering);

    return this.http.get<Paginee<VehiculeListe>>(`${this.baseUrl}/`, { params });
  }

  obtenirVehicule(slug: string): Observable<VehiculeDetail> {
    return this.http.get<VehiculeDetail>(`${this.baseUrl}/${slug}/`);
  }

  listerOptions(categorie?: string): Observable<Paginee<OptionPack>> {
    let params = new HttpParams();
    if (categorie) params = params.set('categorie', categorie);
    return this.http.get<Paginee<OptionPack>>(`${environment.apiUrl}/options/`, { params });
  }
}
