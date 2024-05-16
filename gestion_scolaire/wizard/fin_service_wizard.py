from odoo import models, fields, api

class FinServiceWizard(models.TransientModel):
    _name = "fin.service.wizard"
    _description = "Assistant de fin de service"

    formateur_id = fields.Many2one("formateur", string="Formateur à remplacer", required=True)
    nouveau_formateur_id = fields.Many2one("formateur", string="Nouveau formateur", required=True)

    
    def button_replace(self):
        formateur_a = self.formateur_id
        formateur_b = self.nouveau_formateur_id

        # Assigner la date de fin de service au formateur A
        formateur_a.date_fin_service = fields.Date.today()

        # Modifier le formateur des classes concernées par le formateur B
        classes_a = formateur_a.classes_ids
        for classe in classes_a:
            classe.formateurs_ids -= formateur_a
            classe.formateurs_ids += formateur_b

        return {'type': 'ir.actions.act_window_close'}
