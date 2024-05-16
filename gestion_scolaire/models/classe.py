from odoo import models, fields, api


class Classe(models.Model):
    _name = "classe"
    _rec_name = "code"
    _description = "Modèle pour stocker les informations des classes"

    code = fields.Char(string="Code", required=True)
    formateurs_ids = fields.Many2many("formateur", string="Formateurs")
    etudiants_ids = fields.One2many("etudiant", "classe_id", string="Etudiants")
    filiere_id = fields.Many2one("filiere", string="Filière")
