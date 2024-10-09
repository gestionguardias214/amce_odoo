# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_profesional(models.Model):
    _inherit = "asw.profesionales"

    pro_password = fields.Char(string="Contraseña", default="", required=True)
