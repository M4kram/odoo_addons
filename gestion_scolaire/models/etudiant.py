from odoo import fields, models, api
from datetime import datetime


class Etudiant(models.Model):
    _name = "etudiant"
    _description = "Modèle pour stocker les informations des étudiants"

    # nom_complet = fields.Char(string="Nom complet", compute="_compute_nom_complet")
    nom = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    date_naissance = fields.Date(string="Date de naissance", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True, group_operator="avg")
    classe_id = fields.Many2one("classe", string="Classe")
    inscrit = fields.Boolean(string="Inscrit", default=False)

    @api.onchange("classe_id")
    def _onchange_classe_id(self):
        if self.classe_id:
            self.inscrit = True
        else:
            self.inscrit = False

    def name_get(self):
        return [(etudiant.id, f"{etudiant.nom} {etudiant.prenom}") for etudiant in self]
        # result = []
        # for etudiant in self:
        #     nom_complet = f"{etudiant.nom} {etudiant.prenom}"
        #     result.append((etudiant.id, nom_complet))
        # return result

    # @api.depends("nom", "prenom")
    # def _compute_nom_complet(self):
    #     for record in self:
    #         record.nom_complet = f"{record.nom} {record.prenom}"

    @api.depends("date_naissance")
    def _compute_age(self):
        today = datetime.today().date()
        for record in self:
            if record.date_naissance:
                birth_date = record.date_naissance
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0
