# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions

class asw_quem(models.Model):
    _name = 'asw.quem'
    _description = 'Quemadura'
    _ord = 'quem_nombre'
    _rec_name = 'quem_nombre'

    quem_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'quem_nombre' in values and values['quem_nombre'] not in [False, '']:
            cnt = self.env['asw.quem'].search_count([('quem_nombre', '=', values['quem_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro modulo.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_quem, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'quem_nombre' in values and values['quem_nombre'] not in [False, '']:
            cnt = self.env['asw.quem'].search_count([('quem_nombre', '=', values['quem_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro modulo.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_quem, self).write(values)

        return result