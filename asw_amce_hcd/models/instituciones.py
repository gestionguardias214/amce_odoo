# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_institucion(models.Model):
    _name = "asw.institucion"
    _description = "Institución"

    ins_nombre = fields.Char(string="Nombre")

    ins_codigo = fields.Char(string="Código")
