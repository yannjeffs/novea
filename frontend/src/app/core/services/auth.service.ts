// auth.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Utilisateur } from '../models/utilisateur.model';

interface TokenPair {
  access: string;
  refresh: string;
}

const ACCESS_KEY = 'novea_access_token';
const REFRESH_KEY = 'novea_refresh_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly baseUrl = environment.apiUrl;
  utilisateurConnecte = signal<Utilisateur | null>(null);

  constructor(private http: HttpClient) {}

  get accessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
  }

  get estConnecte(): boolean {
    return !!this.accessToken;
  }

  connexion(username: string, password: string): Observable<TokenPair> {
    return this.http.post<TokenPair>(`${this.baseUrl}/auth/token/`, { username, password }).pipe(
      tap((tokens) => {
        localStorage.setItem(ACCESS_KEY, tokens.access);
        localStorage.setItem(REFRESH_KEY, tokens.refresh);
      })
    );
  }

  rafraichirToken(): Observable<{ access: string }> {
    const refresh = localStorage.getItem(REFRESH_KEY);
    return this.http
      .post<{ access: string }>(`${this.baseUrl}/auth/token/refresh/`, { refresh })
      .pipe(tap((res) => localStorage.setItem(ACCESS_KEY, res.access)));
  }

  deconnexion(): void {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    this.utilisateurConnecte.set(null);
  }

  chargerProfil(): Observable<Utilisateur> {
    return this.http
      .get<Utilisateur>(`${this.baseUrl}/accounts/moi/`)
      .pipe(tap((user) => this.utilisateurConnecte.set(user)));
  }
}
