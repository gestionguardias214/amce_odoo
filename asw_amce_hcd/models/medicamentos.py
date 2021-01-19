# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions

class asw_medicamentos(models.Model):
    _name = 'asw.medicamentos'
    _description = 'Medicamentos'
    _ord = 'medicamentos_nombre'
    _rec_name = 'medicamentos_nombre'

    medicamentos_nombre = fields.Char(
        string = 'Nombre'
    )

    medicamentos_codigo = fields.Integer(
        string = u'Código'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'medicamentos_nombre' in values and values['medicamentos_nombre'] not in [False, '']:
            cnt = self.env['asw.medicamentos'].search_count([('medicamentos_nombre', '=', values['medicamentos_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')
        
        result = super(asw_medicamentos, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'medicamentos_nombre' in values and values['medicamentos_nombre'] not in [False, '']:
            cnt = self.env['asw.medicamentos'].search_count([('medicamentos_nombre', '=', values['medicamentos_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')
        
        result = super(asw_medicamentos, self).write(values)

        return result