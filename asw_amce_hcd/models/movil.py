# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class asw_movil(models.Model):
    """ ABM de movil

    """

    _name = 'asw.movil'
    _description = u'Movil'
    _rec_name = 'movil_nombre'
    _order = 'movil_nombre'

    movil_nombre = fields.Char(
        string=u'Nombre',
    )

    active = fields.Boolean(
        string=u'Está activo?',
        default=True
    )

    @api.model
    def create(self, values):
        if 'movil_nombre' in values and values['movil_nombre'] not in [False, '']:
            cnt = self.env['asw.movil'].search_count([('movil_nombre', '=', values['movil_nombre'])])
            if cnt > 0:
                raise ValidationError('''El nombre provisto ya existe para otro registro. Por
                favor revise nuevamente y vuelva a intentarlo''')

        result = super(asw_movil, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'movil_nombre' in values and values['movil_nombre'] not in [False, '']:
            cnt = self.env['asw.movil'].search_count([('movil_nombre', '=', values['movil_nombre'])])
            if cnt > 0:
                raise ValidationError('''El nombre provisto ya existe para otro registro. Por
                favor revise nuevamente y vuelva a intentarlo''')

        result = super(asw_movil, self).write(values)

        return result