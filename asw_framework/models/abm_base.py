# -*- coding: utf-8 -*-
from openerp import models, fields, api

class asw_abm_base(models.AbstractModel):
    _name = 'asw.abm.base'
    _rec_name = 'name'

    codigo = fields.Char(
        string=u'Código',
        track_visibility='onchange',                
        copy=False,        
        default='',        
    )

    nombre = fields.Char(
        string = 'Nombre'
    )

    descripcion = fields.Char(
        string = 'Descripcion'
    )

    name = fields.Char(
        string = 'Nombre',        
        compute='_compute_name'
    )

    active = fields.Boolean(
        string = 'Esta activo?',
        default = True
    )
    
    @api.depends('codigo', 'descripcion')
    def _compute_name(self):
        for record in self:
            record.name = record.descripcion

    @api.model
    def create(self, values):
        # se asigna automaticamente una descripcion igual al nombre si no se ha provisto de una
        if 'descripcion' in values and values['descripcion'] in ['', False]:
            values['descripcion'] = values['nombre']

        return super(asw_abm_base, self).create(values)
