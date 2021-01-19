# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions

class asw_des(models.Model):
    _name = 'asw.des'
    _description = 'Desenlace'
    _ord = 'des_nombre'
    _rec_name = 'des_nombre'

    des_nombre = fields.Char(
        string = 'Desenlace'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'des_nombre' in values and values['des_nombre'] not in [False, '']:
            cnt = self.env['asw.des'].search_count([('des_nombre', '=', values['des_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_des, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'des_nombre' in values and values['des_nombre'] not in [False, '']:
            cnt = self.env['asw.des'].search_count([('des_nombre', '=', values['des_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_des, self).write(values)

        return result