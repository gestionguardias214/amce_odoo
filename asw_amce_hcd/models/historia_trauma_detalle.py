# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_trauma_detalle(models.Model):
    _name = 'asw.historia_trauma_detalle'
    _description = 'Detalle del Trauma'
    
    lugar = fields.Char(string='Lugar' )
    detalle = fields.Char(string='Detalle' )    