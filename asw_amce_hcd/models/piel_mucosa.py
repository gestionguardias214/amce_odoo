# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_piel_mucosa(models.Model):
    _name = 'asw.piel_mucosa'
    _description = "Piel y Mucosa"
    _ord = 'piel_mucosa_nombre'
    _rec_name = 'piel_mucosa_nombre'

    piel_mucosa_nombre = fields.Char(
        string = 'Piel y mucosa'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'piel_mucosa_nombre' in values and values['piel_mucosa_nombre'] not in [False, '']:
            cnt = self.env['asw.piel_mucosa'].search_count([('piel_mucosa_nombre', '=', values['piel_mucosa_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro para el nombre provisto. Por favor
                revise nuevamente y vuelva a intentarlo''')

        result = super(asw_piel_mucosa, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'piel_mucosa_nombre' in values and values['piel_mucosa_nombre'] not in [False, '']:
            cnt = self.env['asw.piel_mucosa'].search_count([('piel_mucosa_nombre', '=', values['piel_mucosa_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro para el nombre provisto. Por favor
                revise nuevamente y vuelva a intentarlo''')

        result = super(asw_piel_mucosa, self).write(values)

        return result