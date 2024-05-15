from odoo import models, fields


class Skill(models.Model):
    _name = "skill"

    name = fields.Char("Compétence")
    employee_ids = fields.Many2many("employee", string="Employés")
