from odoo import models, fields, api
from datetime import datetime


class Formateur(models.Model):
    _name = "formateur"
    _rec_name = "nom_complet"
    _description = "Modèle pour stocker les informations des formateurs"

    nom_complet = fields.Char(string="Nom complet", compute="_compute_nom_complet", store=True)
    nom = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    classes_ids = fields.Many2many("classe", string="Classes")
    date_embauche = fields.Date(string="Date d'embauche", required=True)
    # date_fin_service = fields.Date(string="Date de fin de service", compute="_compute_date_fin_service", store=True)
    date_fin_service = fields.Date(string="Date de fin de service")
    experience = fields.Integer(string="Expérience (en mois)", compute="_compute_experience", store=True)
    filieres_ids = fields.Many2many("filiere", string="Filières")

    @api.depends("nom", "prenom")
    def _compute_nom_complet(self):
        for formateur in self:
            formateur.nom_complet = f"{formateur.nom} {formateur.prenom}"

    # @api.depends("date_embauche")
    # def _compute_date_fin_service(self):
    #     for formateur in self:
    #         if formateur.date_embauche:
    #             formateur.date_fin_service = formateur.date_embauche.replace(year=formateur.date_embauche.year + 2)
    #         else:
    #             formateur.date_fin_service = False
    
    @api.depends("date_embauche", "date_fin_service")
    def _compute_experience(self):
        today = datetime.today().date()
        for formateur in self:
            if formateur.date_embauche:
                hire_date = formateur.date_embauche
                formateur.experience = (today.year - hire_date.year) * 12 + today.month - hire_date.month
            elif formateur.date_embauche and formateur.date_fin_service:
                hire_date = formateur.date_embauche
                end_date = formateur.date_fin_service
                formateur.experience = (end_date.year - hire_date.year) * 12 + end_date.month - hire_date.month
            else:
                formateur.experience = 0
