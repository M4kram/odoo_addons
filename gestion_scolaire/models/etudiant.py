from odoo import fields, models, api
from datetime import datetime


class Etudiant(models.Model):
    _name = "etudiant"
    _rec_name = "prenom"
    _description = "Modèle pour stocker les informations des étudiants"

    nom = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    date_naissance = fields.Date(string="Date de naissance", required=True)
    age = fields.Integer(string="Age")
    classe_id = fields.Many2one("classe", string="Classe")
    inscrit = fields.Boolean(string="Inscrit", default=False)

    @api.onchange('date_naissance')
    def _onchange_date_naissance(self):
        today = datetime.today().date()
        for record in self:
            if record.date_naissance:
                birth_date = record.date_naissance
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0

