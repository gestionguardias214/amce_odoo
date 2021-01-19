# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_psi(models.Model):
    _name = 'asw.psi'
    _description = u'Psiquiátrico'
    _ord = 'psi_nombre'
    _rec_name = 'psi_nombre'

    psi_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'psi_nombre' in values and values['psi_nombre'] not in [False, '']:
            cnt = self.env['asw.psi'].search_count([('psi_nombre', '=', values['psi_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_psi, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'psi_nombre' in values and values['psi_nombre'] not in [False, '']:
            cnt = self.env['asw.psi'].search_count([('psi_nombre', '=', values['psi_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_psi, self).write(values)

        return result
