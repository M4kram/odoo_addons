from odoo import models, fields

class Filiere(models.Model):
    _name = "filiere"
    _rec_name = "nom"
    _description = "Modèle pour stocker les informations des filières"

    nom = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code", required=True)
