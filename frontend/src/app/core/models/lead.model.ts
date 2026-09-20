// lead.model.ts
export interface LeadCreation {
  nom_contact: string;
  email_contact: string;
  telephone_contact: string;
  source: 'site_web' | 'telephone' | 'whatsapp' | 'showroom' | 'salon';
  energie_interet?: string;
  configuration?: number;
  concession?: number;
  notes?: string;
}
