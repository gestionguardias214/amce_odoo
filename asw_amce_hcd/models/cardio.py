# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_cardio(models.Model):
    _name = 'asw.cardio'
    _description = 'Aparato Cardiovascular'
    _ord = 'cardio_nombre'
    _rec_name = 'cardio_nombre'

    cardio_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo?',
        default = True
    )

    @api.model
    def create(self, values):
        if 'cardio_nombre' in values and values['cardio_nombre'] not in [False, '']:
            cnt = self.env['asw.cardio'].search_count([('cardio_nombre', '=', values['cardio_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_cardio, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'cardio_nombre' in values and values['cardio_nombre'] not in [False, '']:
            cnt = self.env['asw.cardio'].search_count([('cardio_nombre', '=', values['cardio_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_cardio, self).write(values)

        return result