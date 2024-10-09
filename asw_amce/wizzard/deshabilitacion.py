# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_deshabilitacion(models.TransientModel):
    _name = "asw.deshabilitacion"

    def deshabilitar(self):
        context = self.env.context
        prof_ids = context.get("active_ids", [])
        profs = self.env["asw.profesionales"].search([("id", "in", prof_ids)])
        profs.write({"active": False})
