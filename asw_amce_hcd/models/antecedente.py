# -*- encoding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_antecedente(models.Model):
    _name = 'asw.antecedente'
    _description = 'Antecedentes'
    _ord = 'antecedente_nombre'
    _rec_name = 'antecedente_nombre'

    antecedente_nombre = fields.Char(
        string = 'Antecedentes'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'antecedente_nombre' in values and values['antecedente_nombre'] not in [False, '']:
            cnt = self.env['asw.antecedente'].search_count([('antecedente_nombre', '=', values['antecedente_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con los antecedentes ingresados. Por
                favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_antecedente, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'antecedente_nombre' in values and values['antecedente_nombre'] not in [False, '']:
            cnt = self.env['asw.antecedente'].search_count([('antecedente_nombre', '=', values['antecedente_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con los antecedentes ingresados. Por favor
                revise nuevamente y vuelva a intentarlo''')

        result = super(asw_antecedente, self).write(values)

        return result