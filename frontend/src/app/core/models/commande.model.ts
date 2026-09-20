// commande.model.ts
export interface Paiement {
  id: number;
  reference: string;
  commande: number;
  canal: 'momo' | 'orange_money' | 'virement' | 'carte' | 'especes';
  montant: number;
  statut: 'en_attente' | 'valide' | 'echoue' | 'rembourse';
  reference_externe: string;
}

export interface Commande {
  id: number;
  reference: string;
  client: number;
  configuration: number;
  concession: number;
  montant_total: number;
  acompte_montant: number;
  financement_type: 'comptant' | 'credit' | 'loa';
  etape: string;
  date_prevue_livraison: string | null;
  paiements: Paiement[];
}
