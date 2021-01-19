# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo import exceptions

class asw_mco(models.Model):
    _name = 'asw.mco'
    _description = 'Motivo de Consulta'
    _ord = 'mco_nombre'
    _rec_name = 'mco_nombre'

    mco_nombre = fields.Char(
        string = 'Motivo'
    )

    mco_codigo = fields.Integer(
        string = u'Código'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'mco_codigo' in values and values['mco_codigo'] not in [False, '']:
            cnt = self.env['asw.mco'].search_count([('mco_codigo', '=', values['mco_codigo'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                y vuelva a intentarlo.''')
        else:
            raise exceptions.Warning('No se ha provisto ningun codigo para el registro')

        if 'mco_nombre' in values and values['mco_nombre'] not in [False, '']:
            cnt = self.env['asw.mco'].search_count([('mco_nombre', '=', values['mco_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                y vuelva a intentarlo.''')
        else:
            raise exceptions.Warning('No se ha provisto ningun motivo para el registro')

        result = super(asw_mco, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'mco_codigo' in values:
            if values['mco_codigo'] not in [False, '']:
                cnt = self.env['asw.mco'].search_count([('mco_codigo', '=', values['mco_codigo'])])
                if cnt > 0:
                    raise exceptions.Warning('''Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo.''')
            else:
                raise exceptions.Warning('Por favor ingrese un codigo')

        if 'mco_nombre' in values:
            if values['mco_nombre'] not in [False, '']:
                cnt = self.env['asw.mco'].search_count([('mco_nombre', '=', values['mco_nombre'])])
                if cnt > 0:
                    raise exceptions.Warning('''Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo.''')
            else:
                raise exceptions.Warning('Por favor ingrese un motivo')

        result = super(asw_mco, self).write(values)

        return result