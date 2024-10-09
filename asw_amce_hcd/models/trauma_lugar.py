# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_trauma_lugar(models.Model):
    _name = "asw.trauma_lugar"
    _description = "Lugar del trauma"
    _ord = "trauma_lugar_nombre"
    _rec_name = "trauma_lugar_nombre"

    trauma_lugar_nombre = fields.Char(string="Nombre")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "trauma_lugar_nombre" in values and values["trauma_lugar_nombre"] not in [
            False,
            "",
        ]:

            cnt = self.env["asw.trauma_lugar"].search_count(
                [("trauma_lugar_nombre", "=", values["trauma_lugar_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_trauma_lugar, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "trauma_lugar_nombre" in values and values["trauma_lugar_nombre"] not in [
            False,
            "",
        ]:

            cnt = self.env["asw.trauma_lugar"].search_count(
                [("trauma_lugar_nombre", "=", values["trauma_lugar_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_trauma_lugar, self).create(values)

        return result
