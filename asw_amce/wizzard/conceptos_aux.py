# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_conceptos_aux(models.TransientModel):
    _name = 'asw.conceptos.aux'    
    _description = 'Modelo auxiliar de conceptos profesionales'
    
    aux_concepto = fields.Many2one(
        string=u'Concepto',
        comodel_name='asw.concepto',
        ondelete='restrict',
    )
    
    aux_importe = fields.Float(
        string=u'Importe',        
        default=0,        
    )
    
    