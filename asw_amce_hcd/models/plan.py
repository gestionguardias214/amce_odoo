# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions


class asw_plan(models.Model):
    _name = "asw.plan"
    _description = "Plan"
    _ord = "plan_nombre"
    _rec_name = "plan_nombre"

    plan_nombre = fields.Char(string="Nombre")

    plan_codigo = fields.Integer(string="Código")

    active = fields.Boolean(string="Está activo?", default=True)

    @api.model
    def create(self, values):
        if "plan_codigo" in values and values["plan_codigo"] not in [False, ""]:
            cnt = self.env["asw.plan"].search_count(
                [("plan_codigo", "=", values["plan_codigo"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                y vuelva a intentarlo."""
                )
        else:
            raise exceptions.Warning("No se ha provisto ningun codigo para el registro")

        if "plan_nombre" in values and values["plan_nombre"] not in [False, ""]:
            cnt = self.env["asw.plan"].search_count(
                [("plan_nombre", "=", values["plan_nombre"])]
            )
            if cnt > 0:
                raise exceptions.Warning(
                    """Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                y vuelva a intentarlo."""
                )
        else:
            raise exceptions.Warning("No se ha provisto ningun motivo para el registro")

        result = super(asw_plan, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if "plan_codigo" in values:
            if values["plan_codigo"] not in [False, ""]:
                cnt = self.env["asw.plan"].search_count(
                    [("plan_codigo", "=", values["plan_codigo"])]
                )
                if cnt > 0:
                    raise exceptions.Warning(
                        """Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo."""
                    )
            else:
                raise exceptions.Warning("Por favor ingrese un codigo")

        if "plan_nombre" in values:
            if values["plan_nombre"] not in [False, ""]:
                cnt = self.env["asw.plan"].search_count(
                    [("plan_nombre", "=", values["plan_nombre"])]
                )
                if cnt > 0:
                    raise exceptions.Warning(
                        """Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo."""
                    )
            else:
                raise exceptions.Warning("Por favor ingrese un motivo")

        result = super(asw_plan, self).write(values)

        return result
