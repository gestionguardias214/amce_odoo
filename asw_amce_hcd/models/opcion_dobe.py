# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_opcion_doble(models.AbstractModel):
    _name = "asw.opcion_doble"

    opcion_doble = fields.Boolean(
        string="Opcion doble",
    )
