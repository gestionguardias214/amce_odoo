# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_provincia(models.Model):
    _name = "asw.provincia"
    _inherit = ["mail.thread", "asw.abm.base"]
    _description = "Provincia"
    _sql_constraints = [
        (
            "codigo_unique",
            "UNIQUE(codigo)",
            "Ya se ha ingresado un Provincia con este codigo, por favor ingrese un codigo diferente",
        ),
    ]
    _rec_name = "descripcion"

    codigo = fields.Char(
        default="",
    )

    pro_localidad = fields.One2many(
        string="Localidades",
        comodel_name="asw.localidad",
        inverse_name="loc_provincia",
    )

    @api.depends("descripcion")
    def _compute_name(self):
        for record in self:
            record.name = record.descripcion

    @api.multi
    def unlink(self):
        for record in self:
            if len(record.pro_localidad) > 0:
                raise exceptions.ValidationError(
                    "No se puede eliminar una Provincia con Localidades relacionadas, por favor eliminelas y vuelva a intentarlo"
                )

            super(asw_provincia, record).unlink()
