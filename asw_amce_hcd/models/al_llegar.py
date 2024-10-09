# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_al_llegar(models.Model):
    _name = "asw.al_llegar"
    _description = "Al llegar al domicilio"
    _ord = "al_llegar_nombre"
    _rec_name = "al_llegar_nombre"

    al_llegar_nombre = fields.Char(string="Al llegar")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "al_llegar_nombre" in values and values["al_llegar_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.al_llegar"].search_count(
                [("al_llegar_nombre", "=", values["al_llegar_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_al_llegar, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "al_llegar_nombre" in values and values["al_llegar_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.al_llegar"].search_count(
                [("al_llegar_nombre", "=", values["al_llegar_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo."""
                )

        result = super(asw_al_llegar, self).write(values)

        return result
