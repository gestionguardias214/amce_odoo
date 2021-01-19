# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_cyc(models.Model):
    _name = 'asw.cyc'
    _description = 'Cabeza y Cuello'
    _ord = 'cyc_nombre'
    _rec_name = 'cyc_nombre'

    cyc_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'cyc_nombre' in values and values['cyc_nombre'] not in [False, '']:
            cnt = self.env['asw.cyc'].search_count([('cyc_nombre', '=', values['cyc_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_cyc, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'cyc_nombre' in values and values['cyc_nombre'] not in [False, '']:
            cnt = self.env['asw.cyc'].search_count([('cyc_nombre', '=', values['cyc_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_cyc, self).write(values)

        return result
