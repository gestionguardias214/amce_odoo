# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class asw_cobertura(models.Model):
    _name = 'asw.cobertura'
    _description = u'Cobertura medica'

    _rec_name = 'cob_nombre'
    _order = 'cob_nombre ASC'

    cob_nombre = fields.Char(
        string = 'Nombre'
    )

    cob_plan_obligatorio = fields.Boolean(
        string = 'Plan obligatorio'
    )

    cob_nro_socio_obligatorio = fields.Boolean(
        string = 'Nro socio obligatorio'
    )

    cob_dni_obligatorio = fields.Boolean(
        string = 'DNI obligatorio'
    )

    cob_nombre_paciente_obligatorio = fields.Boolean(
        string = 'Nombre paciente obligatorio'
    )

    cob_apellido_paciente_obligatorio = fields.Boolean(
        string = 'Apellido paciente obligatorio'
    )
