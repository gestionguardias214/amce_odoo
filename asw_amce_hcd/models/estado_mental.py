# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_neuro_estado_mental(models.Model):
    _name = "asw.neuro_estado_mental"
    _inherit = ["asw.abm.base"]
    _description = "Estado mental"
