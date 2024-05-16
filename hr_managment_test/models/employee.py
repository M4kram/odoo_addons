from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Employee(models.Model):
    _name = "employee"
    _rec_name = "first_name"

    first_name = fields.Char("Prénom")
    last_name = fields.Char("Nom", required=True)
    state = fields.Selection([
        ("in", "In"),
        ("out", "Out"),
    ], default="in", string="État")
    department_id = fields.Many2one("department", string="Département")
    salary = fields.Float("Salaire", default="3000")
    number = fields.Integer("Matricule")
    skill_ids = fields.Many2many("skill", string="Compétences")
    # skill_ids_spec = fields.Many2many("skill",
    #                                   relation="employee_skill_rel_spec",
    #                                   column1="employee_id_spec",
    #                                   column2="skill_id_spec"
    # )

    def button_test(self):
        # unlink
        for employee in self:
            if employee.salary < 2000:
                employee.unlink()

        # # filtered
        # to_delete = self.filtered(lambda e: e.salary < 4000 and e.department_id.name == "Finance")
        # to_delete.unlink()

        # # mapped
        # last_names = self.mapped("last_name")
        # print(last_names)

        # department_names = self.mapped("department_id").mapped("name")
        # print(department_names)

        # # sorted
        # print(f"Par défaut: {self}")
        # sorted_by_number = self.sorted(key=lambda e: (e.number, e.salary), reverse=False)
        # print(f"Aprés sorted: {sorted_by_number}")
        return True


    @api.model
    def create(self, vals):
        res = super(Employee, self).create(vals)

        if vals["salary"] < 5000:
            raise UserError("Vous avez un salaire inferieur a 5000")

        return res

    @api.onchange("skill_ids")
    def _onchange_skill_ids(self):
        js_id = self.env["skill"].search([("name", "=", "JavaScript")], limit=1)
        if self.skill_ids:
            if js_id.id in self.skill_ids.ids:
                self.department_id = self.env["department"].search([("name", "=", "Informatique")], limit=1).id

    @api.constrains("number")
    def _constrains_for_number(self):
        number_exist = self.env["employee"].search([("number", "=", self.number), ("id", "!=", self.id)], limit=1)
        if number_exist:
            raise ValidationError("Le matricule que vous avez entrer existe déja.")
