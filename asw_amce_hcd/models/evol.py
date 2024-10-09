# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_evol(models.Model):
    _name = "asw.evol"
    _description = "Evolución"
    _ord = "evol_nombre"
    _rec_name = "evol_nombre"

    evol_nombre = fields.Char(string="Evolución")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "evol_nombre" in values and values["evol_nombre"] not in [False, ""]:
            cnt = self.env["asw.evol"].search_count(
                [("evol_nombre", "=", values["evol_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_evol, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "evol_nombre" in values and values["evol_nombre"] not in [False, ""]:
            cnt = self.env["asw.evol"].search_count(
                [("evol_nombre", "=", values["evol_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_evol, self).create(values)

        return result
