# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_hosp(models.Model):
    _name = "asw.hosp"
    _description = "Hospitales"
    _ord = "hosp_nombre"
    _rec_name = "hosp_nombre"

    hosp_nombre = fields.Char(string="Hospital")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "hosp_nombre" in values and values["hosp_nombre"] not in [False, ""]:
            cnt = self.env["asw.hosp"].search_count(
                [("hosp_nombre", "=", values["hosp_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_hosp, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "hosp_nombre" in values and values["hosp_nombre"] not in [False, ""]:
            cnt = self.env["asw.hosp"].search_count(
                [("hosp_nombre", "=", values["hosp_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_hosp, self).write(values)

        return result
