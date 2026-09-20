// vehicule.model.ts
export type TypeEnergie = 'essence' | 'diesel' | 'hybride' | 'hybride_rechargeable' | 'electrique';
export type TypeCarrosserie = 'berline' | 'suv' | 'citadine' | 'break' | 'pickup' | 'monospace';

export interface VehiculeListe {
  id: number;
  nom: string;
  slug: string;
  carrosserie: TypeCarrosserie;
  energie: TypeEnergie;
  prix_base: number;
  autonomie_km: number | null;
  consommation_l_100km: number | null;
  puissance_ch: number | null;
  disponible: boolean;
  photo_principale: string | null;
}

export interface Finition {
  id: number;
  modele: number;
  nom: string;
  supplement_prix: number;
  puissance_ch: number | null;
  autonomie_km: number | null;
  equipements_inclus: string;
  ordre: number;
}

export interface Teinte {
  id: number;
  modele: number;
  nom: string;
  code_hex: string;
  supplement_prix: number;
}

export interface Habitacle {
  id: number;
  modele: number;
  nom: string;
  description: string;
  supplement_prix: number;
}

export interface OptionPack {
  id: number;
  nom: string;
  description: string;
  prix: number;
  categorie: 'confort' | 'securite' | 'multimedia' | 'style';
  disponible: boolean;
}

export interface VehiculeDetail extends VehiculeListe {
  description: string;
  capacite_batterie_kwh: number | null;
  temps_recharge_minutes: number | null;
  finitions: Finition[];
  teintes: Teinte[];
  habitacles: Habitacle[];
  medias: { id: number; type_media: string; vue: string; fichier: string; legende: string }[];
  documents: { id: number; type_document: string; langue: string; fichier: string }[];
  options: OptionPack[];
}
