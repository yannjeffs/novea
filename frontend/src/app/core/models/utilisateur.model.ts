// utilisateur.model.ts
export type RoleUtilisateur =
  | 'client_particulier'
  | 'client_entreprise'
  | 'conseiller'
  | 'chef_ventes'
  | 'responsable_stock'
  | 'direction'
  | 'admin_catalogue';

export interface Utilisateur {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  telephone: string | null;
  role: RoleUtilisateur;
  langue_preferee: 'fr' | 'en';
  concession: number | null;
  raison_sociale: string;
}
