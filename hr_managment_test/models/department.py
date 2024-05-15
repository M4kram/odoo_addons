from odoo import fields, models, api


class Department(models.Model):
    _name = "department"

    name = fields.Char("Nom")
    employee_ids = fields.One2many("employee", "department_id", string="Employés")
    employees_count = fields.Integer("Nombre des employés", compute="_compute_employees_count")

    @api.depends("employee_ids")
    def _compute_employees_count(self):
        for department in self:
            department.employees_count = len(department.employee_ids)
