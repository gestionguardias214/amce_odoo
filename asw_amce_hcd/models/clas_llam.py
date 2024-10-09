# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_clas_llam(models.Model):
    _name = "asw.clas_llam"
    _description = "Clasificacion de la Llamada"
    _ord = "clas_llam_nombre"
    _rec_name = "clas_llam_nombre"

    clas_llam_nombre = fields.Char(string="Clasificación Llamada")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "clas_llam_nombre" in values and values["clas_llam_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.clas_llam"].search_count(
                [("clas_llam_nombre", "=", values["clas_llam_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_clas_llam, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "clas_llam_nombre" in values and values["clas_llam_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.clas_llam"].search_count(
                [("clas_llam_nombre", "=", values["clas_llam_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_clas_llam, self).write(values)

        return result
