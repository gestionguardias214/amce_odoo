# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions

class asw_trauma_tipo(models.Model):
    _name = 'asw.trauma_tipo'
    _description = 'Tipo de trauma'
    _ord = 'trauma_tipo_nombre'
    _rec_name = 'trauma_tipo_nombre'

    trauma_tipo_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if ('trauma_tipo_nombre' in values and 
            values['trauma_tipo_nombre'] not in [False, '']):

            cnt = self.env['asw.trauma_tipo'].search_count([('trauma_tipo_nombre', '=', values['trauma_tipo_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_trauma_tipo, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if ('trauma_tipo_nombre' in values and 
            values['trauma_tipo_nombre'] not in [False, '']):

            cnt = self.env['asw.trauma_tipo'].search_count([('trauma_tipo_nombre', '=', values['trauma_tipo_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_trauma_tipo, self).create(values)

        return result