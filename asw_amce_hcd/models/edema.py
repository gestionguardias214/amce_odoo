# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions

class asw_edema(models.Model):
    _name = 'asw.edema'
    _description = 'Edemas'
    _ord = 'edema_nombre'
    _rec_name = 'edema_nombre'

    edema_nombre = fields.Char(
        string = 'Edemas'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'edema_nombre' in values and values['edema_nombre'] not in [False, '']:
            cnt = self.env['asw.edema'].search_count([('edema_nombre', '=', values['edema_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con ese nombre. Por favor revise nuevamente y vuelva
                a intentarlo''')

        result = super(asw_edema, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'edema_nombre' in values and values['edema_nombre'] not in [False, '']:
            cnt = self.env['asw.edema'].search_count([('edema_nombre', '=', values['edema_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con ese nombre. Por favor revise nuevamente y vuelva
                a intentarlo''')

        result = super(asw_edema, self).write(values)

        return result
