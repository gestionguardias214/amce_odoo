# -*- coding: utf-8 -*-
from openerp import fields, models, api
from odoo import exceptions


class asw_neuro(models.Model):
    _name = "asw.neuro"
    _description = "Examen neurológico"
    _ord = ""
    _rec_name = "neuro_nombre"

    _inherit = ["asw.opcion_doble"]

    neuro_nombre = fields.Char(string="Nombre")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "neuro_nombre" in values and values["neuro_nombre"] not in [False, ""]:
            cnt = self.env["asw.neuro"].search_count(
                [("neuro_nombre", "=", values["neuro_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_neuro, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "neuro_nombre" in values and values["neuro_nombre"] not in [False, ""]:
            cnt = self.env["asw.neuro"].search_count(
                [("neuro_nombre", "=", values["neuro_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_neuro, self).write(values)

        return result
