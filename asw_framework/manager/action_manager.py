# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from datetime import datetime


class asw_action_manager(models.AbstractModel):
    _name = "asw.action.manager"

    def get_action(self, nombre, modelo, view_type, target):
        return {
            "name": nombre,
            "type": "form",
            "res_model": model,
            "view_type": view_type,
            "view_mode": "form",
            "targe": target,
        }

    def get_action_existente(self, accion):
        return self.env.ref("asw_tpv." + accion)

    def get_action_navega(self, accion, id_navega):
        action_id = self.get_action_existente(accion)
        return {
            "name": action_id.name,
            "type": action_id.type,
            "res_model": action_id.res_model,
            "view_type": action_id.view_type,
            "view_mode": "form",
            "help": action_id.help,
            "res_id": id_navega,
            "targe": "inline",
        }
