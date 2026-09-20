// concession.model.ts
export interface Concession {
  id: number;
  nom: string;
  ville: string;
  adresse: string;
  telephone: string;
  email: string;
  capacite_essai_quotidienne: number;
  horaires: string;
  actif: boolean;
}
