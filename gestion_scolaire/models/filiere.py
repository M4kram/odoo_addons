from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Filiere(models.Model):
    _name = "filiere"
    _rec_name = "nom"
    _description = "Modèle pour stocker les informations des filières"

    nom = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code", required=True)
    
    @api.constrains("code")
    def _check_unique_code(self):
        for filiere in self:
            if self.search_count([("code", "=", filiere.code), ("id", "!=", filiere.id)]) > 0:
                raise ValidationError("Le code de la filière doit être unique.")
