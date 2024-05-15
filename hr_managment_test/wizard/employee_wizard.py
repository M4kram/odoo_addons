from odoo import models, fields
from odoo.exceptions import UserError


class EmployeeWizard(models.TransientModel):
    _name = "employee.wizard"

    first_name = fields.Char("Prénom")
    last_name = fields.Char("Nom")
    department_id = fields.Many2one("department", string="Département")
    salary = fields.Float("Salaire", default="3000")
    number = fields.Integer("Matricule")

    def button_create_employee(self):
        domain = [("number", "=", self.number)]
        employee_found = self.env["employee"].search(domain, limit=1)

        if bool(employee_found):
            # MAJ
            employee_found.update(
                {
                    "first_name": self.first_name or employee_found.first_name,
                    "last_name": self.last_name or employee_found.last_name,
                    "department_id": self.department_id.id or employee_found.department_id.id,
                    "salary": self.salary > employee_found.salary and self.salary or employee_found.salary,
                }
            )
        else:
            new_employee = self.env["employee"].create(
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "department_id": self.department_id.id,
                    "salary": self.salary,
                    "number": self.number,
                }
            )

            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    # success, warning, danger
                    'type': 'success',
                    'message': 'Employee cree avec succes!',
                    'sticky': False,
                }
            }

            employee_action = {
                "name": "Nouveau Employé",
                "type": "ir.actions.act_window",
                "res_model": "employee",
                "view_mode": "tree,form",
                # new = popup, current = chemin encours, main = nouveau chemin
                "target": "main",
                # "res_id": new_employee.id,
                "domain": [("id", "=", new_employee.id)],
                "views": [
                    (self.env.ref("hr_managment_test.employee_tree_view").id, "tree"),
                    (self.env.ref("hr_managment_test.employee_form_view").id, "form"),
                ],
                "context": {
                    "edit": False,
                    "create": False,
                    "delete": False,
                }
            }

            return {
                'type': 'ir.actions.act_multi',
                'actions': [
                    employee_action,
                    notification,
                    # {'type': 'ir.actions.act_window_close'},
                ]
            }
