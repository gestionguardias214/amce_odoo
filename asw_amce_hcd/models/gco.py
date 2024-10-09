# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions


class asw_gco(models.Model):
    _name = "asw.gco"
    _description = "Ginecobstetrico"
    _ord = "gco_nombre"
    _rec_name = "gco_nombre"

    gco_nombre = fields.Char(string="Nombre")

    active = fields.Boolean(string="Está activo", default=True)

    @api.model
    def create(self, values):
        if "gco_nombre" in values and values["gco_nombre"] not in [False, ""]:
            cnt = self.env["asw.gco"].search_count(
                [("gco_nombre", "=", values["gco_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_gco, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "gco_nombre" in values and values["gco_nombre"] not in [False, ""]:
            cnt = self.env["asw.gco"].search_count(
                [("gco_nombre", "=", values["gco_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_gco, self).write(values)

        return result
