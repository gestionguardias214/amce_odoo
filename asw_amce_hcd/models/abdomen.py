# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_abdomen(models.Model):
    _name = 'asw.abdomen'
    _description = 'Abdomen'
    _ord = 'abdomen_nombre'
    _rec_name = 'abdomen_nombre'

    abdomen_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'abdomen_nombre' in values and values['abdomen_nombre'] not in [False, '']:
            cnt = self.env['asw.abdomen'].search_count([('abdomen_nombre', '=', values['abdomen_nombre'])]) 
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor intente nuevamente y vuelva a intentarlo.''')

        result = super(asw_abdomen, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'abdomen_nombre' in values and values['abdomen_nombre'] not in [False, '']:
            cnt = self.env['asw.abdomen'].search_count([('abdomen_nombre', '=', values['abdomen_nombre'])]) 
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor intente nuevamente y vuelva a intentarlo.''')

        result = super(asw_abdomen, self).write(values)

        return result