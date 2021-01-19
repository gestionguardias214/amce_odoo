# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_linea_actualizacion(models.Model):
    _name = 'asw.linea_actualizacion'
    _inherit = ['mail.thread']
    _description = 'Linea de actualizacion'
    
    lia_categoria = fields.Many2one(
        string=u'Categoria',
        comodel_name='asw.categoria',
        ondelete='restrict',
    )
    
    lia_precio_actual = fields.Float(
        string=u'Precio actual',
    )
    
    lia_precio_nuevo = fields.Float(
        string=u'Precio nuevo',
    )
    
    lia_actualizacion = fields.Many2one(
        string=u'Actualizacion',
        comodel_name='asw.actualizacion_precio',
        ondelete='restrict',
    )
    