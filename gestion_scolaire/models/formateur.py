from odoo import models, fields, api
from datetime import datetime

class Formateur(models.Model):
    _name = "formateur"
    _description = "Modèle pour stocker les informations des formateurs"

    nom = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    classes_ids = fields.Many2many("classe", string="Classes")
    date_embauche = fields.Date(string="Date d'embauche", required=True)
    date_fin_service = fields.Date(string="Date de fin de service", compute="_compute_date_fin_service", store=True)
    experience = fields.Integer(string="Expérience (en mois)", compute="_compute_experience", store=True)
    filieres_ids = fields.Many2many("filiere", string="Filières")

    @api.depends('date_embauche')
    def _compute_date_fin_service(self):
        for formateur in self:
            if formateur.date_embauche:
                formateur.date_fin_service = formateur.date_embauche.replace(year=formateur.date_embauche.year + 2)
            else:
                formateur.date_fin_service = False
    
    @api.depends('date_embauche')
    def _compute_experience(self):
        today = datetime.today().date()
        for formateur in self:
            if formateur.date_embauche:
                hire_date = formateur.date_embauche
                formateur.experience = (today.year - hire_date.year) * 12 + today.month - hire_date.month
            else:
                formateur.experience = 0
