# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_zona(models.Model):
    _name = "asw.zona"
    _inherit = ["mail.thread", "asw.abm.base"]
    _description = "Zona"
    _sql_constraints = [
        (
            "codigo_unique",
            "UNIQUE(codigo)",
            "Ya se ha ingresado un Zona con este codigo, por favor ingrese un codigo diferente",
        ),
    ]

    zon_loc_id = fields.Many2one(
        string="Localidad",
        comodel_name="asw.localidad",
        ondelete="set null",
    )

    @api.depends("descripcion")
    def _compute_name(self):
        for record in self:
            record.name = record.descripcion
