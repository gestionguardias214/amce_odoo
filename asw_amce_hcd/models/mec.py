# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions


class asw_mec(models.Model):
    _name = "asw.mec"
    _description = "Mecanismo"
    _ord = "mec_nombre"
    _rec_name = "mec_nombre"

    mec_nombre = fields.Char(string="Nombre")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "mec_nombre" in values and values["mec_nombre"] not in [False, ""]:
            cnt = self.env["asw.mec"].search_count(
                [("mec_nombre", "=", values["mec_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_mec, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "mec_nombre" in values and values["mec_nombre"] not in [False, ""]:
            cnt = self.env["asw.mec"].search_count(
                [("mec_nombre", "=", values["mec_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_mec, self).write(values)

        return result
