# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_medicacion(models.Model):
    _name = "asw.medicacion"
    _description = "Medicacion"
    _ord = "medicacion_nombre"
    _rec_name = "medicacion_nombre"

    medicacion_nombre = fields.Char(string="Medicacion")

    medicacion_codigo = fields.Integer(string="Código")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "medicacion_codigo" in values:
            if values["medicacion_codigo"] not in [False, ""]:
                cnt = self.env["asw.medicacion"].search_count(
                    [("medicacion_codigo", "=", values["medicacion_codigo"])]
                )
                if cnt > 0:
                    raise exceptions.Warning(
                        """Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo."""
                    )
            else:
                raise exceptions.Warning("No se ha ingresado ningun codigo")

        if "medicacion_nombre" in values and values["medicacion_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.medicacion"].search_count(
                [("medicacion_nombre", "=", values["medicacion_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """Ya existe un registro con la medicacion especificada. Por favor revise nuevamente
                y vuelva a intentarlo."""
                )

        result = super(asw_medicacion, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "medicacion_codigo" in values:
            if values["medicacion_codigo"] not in [False, ""]:
                cnt = self.env["asw.medicacion"].search_count(
                    [("medicacion_codigo", "=", values["medicacion_codigo"])]
                )
                if cnt > 0:
                    raise exceptions.Warning(
                        """Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo."""
                    )
            else:
                raise exceptions.Warning("No se ha ingresado ningun codigo")

        if "medicacion_nombre" in values and values["medicacion_nombre"] not in [
            False,
            "",
        ]:
            cnt = self.env["asw.medicacion"].search_count(
                [("medicacion_nombre", "=", values["medicacion_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """Ya existe un registro con la medicacion especificada. Por favor revise nuevamente
                y vuelva a intentarlo."""
                )

        result = super(asw_medicacion, self).write(values)

        return result
