# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_diagnos(models.Model):
    _name = "asw.diagnos"
    _description = "Diagnostico"
    _ord = "diagnos_nombre"
    _rec_name = "diagnos_nombre"

    diagnos_nombre = fields.Char(string="Diagnóstico")

    diagnos_codigo = fields.Char(string="Diagnóstico")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "diagnos_nombre" in values and values["diagnos_nombre"] not in [False, ""]:
            cnt = self.env["asw.diagnos"].search_count(
                [("diagnos_nombre", "=", values["diagnos_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_diagnos, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "diagnos_nombre" in values and values["diagnos_nombre"] not in [False, ""]:
            cnt = self.env["asw.diagnos"].search_count(
                [("diagnos_nombre", "=", values["diagnos_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_diagnos, self).write(values)

        return result
