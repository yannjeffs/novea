// configuration.model.ts
export interface Configuration {
  id: number;
  reference: string;
  client: number | null;
  modele: number;
  finition: number;
  teinte: number | null;
  habitacle: number | null;
  options: number[];
  prix_total: number;
  mensualite_estimee: number | null;
  statut: 'brouillon' | 'enregistree' | 'convertie';
  created_at: string;
}
