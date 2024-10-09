# -*- coding: utf-8 -*-
from openerp import api, fields, models


class asw_trauma(models.Model):
    _name = "asw.trauma"
    _description = "Trauma"
    _ord = "trauma_tipo_id"
    _rec_name = "trauma_tipo_id"

    trauma_lugar_id = fields.Many2one(
        string="Lugar", comodel_name="asw.trauma_lugar", ondelete="set null"
    )

    trauma_tipo_id = fields.Many2one(
        string="Tipo", comodel_name="asw.trauma_tipo", ondelete="set null"
    )

    active = fields.Boolean(string="Está activo?", default=True)
