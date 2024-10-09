# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions


class asw_urogen(models.Model):
    _name = "asw.urogen"
    _description = "Urogenital"
    _ord = "urogen_nombre"
    _rec_name = "urogen_nombre"

    urogen_nombre = fields.Char(string="Nombre")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "urogen_nombre" in values and values["urogen_nombre"] not in [False, ""]:
            cnt = self.env["asw.urogen"].search_count(
                [("urogen_nombre", "=", values["urogen_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_urogen, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "urogen_nombre" in values and values["urogen_nombre"] not in [False, ""]:
            cnt = self.env["asw.urogen"].search_count(
                [("urogen_nombre", "=", values["urogen_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_urogen, self).write(values)

        return result
