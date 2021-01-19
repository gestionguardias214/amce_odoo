# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_score_glasgow(models.Model):
    _name = 'asw.historia_score_glasgow'
    _description = 'Historia Score Glasgow'
    
    hora = fields.Char(string='Hora' )
    motora = fields.Char(string='Motora' )
    ocular = fields.Char(string='Ocular' )
    verbal = fields.Char(string='Verbal' )
    total = fields.Char(string='Total' )