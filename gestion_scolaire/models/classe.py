from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Classe(models.Model):
    _name = "classe"
    _rec_name = "code"
    _description = "Modèle pour stocker les informations des classes"
    _sql_constraints = [
        ("code_unique", "UNIQUE(code)", "Le code de la classe doit être unique.")
    ]

    nom = fields.Char(string="Nom", compute="_compute_name")
    code = fields.Char(string="Code", required=True)
    etudiants_ids = fields.One2many("etudiant", "classe_id", string="Etudiants")
    formateurs_ids = fields.Many2many("formateur", string="Formateurs")
    filiere_id = fields.Many2one("filiere", string="Filière")

    @api.depends("code", "filiere_id")
    def _compute_name(self):
        for classe in self:
            nom = ""
            if classe.filiere_id:
                nom += classe.filiere_id.code
            if classe.code:
                nom += classe.code
            classe.nom = nom
