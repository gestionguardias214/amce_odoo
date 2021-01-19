# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo import exceptions

class asw_mla(models.Model):
    _name = 'asw.mla'
    _description = 'Motivo de Llamado'
    _ord = 'mla_nombre'
    _rec_name = 'mla_nombre'

    mla_nombre = fields.Char(
        string = 'Motivo'
    )

    mla_codigo = fields.Integer(
        string = u'Código'
    )

    mla_color = fields.Char(
        string = u'Color'
    )

    active = fields.Boolean(
        string = 'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'mla_codigo' in values and values['mla_codigo'] not in [False, '']:
            cnt = self.env['asw.mla'].search_count([('mla_codigo', '=', values['mla_codigo'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                y vuelva a intentarlo.''')
        else:
            raise exceptions.Warning('No se ha provisto ningun codigo para el registro')

        if 'mla_nombre' in values and values['mla_nombre'] not in [False, '']:
            cnt = self.env['asw.mla'].search_count([('mla_nombre', '=', values['mla_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                y vuelva a intentarlo.''')
        else:
            raise exceptions.Warning('No se ha provisto ningun motivo para el registro')

        result = super(asw_mla, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'mla_codigo' in values:
            if values['mla_codigo'] not in [False, '']:
                cnt = self.env['asw.mla'].search_count([('mla_codigo', '=', values['mla_codigo'])])
                if cnt > 0:
                    raise exceptions.Warning('''Ya existe un registro con el codigo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo.''')
            else:
                raise exceptions.Warning('Por favor ingrese un codigo')

        if 'mla_nombre' in values:
            if values['mla_nombre'] not in [False, '']:
                cnt = self.env['asw.mla'].search_count([('mla_nombre', '=', values['mla_nombre'])])
                if cnt > 0:
                    raise exceptions.Warning('''Ya existe un registro con el motivo provisto. Por favor revise nuevamente
                    y vuelva a intentarlo.''')
            else:
                raise exceptions.Warning('Por favor ingrese un motivo')

        result = super(asw_mla, self).write(values)

        return result