# -*- coding: utf-8 -*-
from openerp import api, models, fields

class asw_signos(models.Model):
    _name = 'asw.signos'
    _description = 'Signos vitales'
    _ord = ''
    _rec_name = 'signos_hora'

    signos_hora = fields.Char(
        string = 'Hora'
    )

    signos_tas = fields.Char(
        string = 'TAS'
    )

    signos_tad = fields.Char(
        string = 'TAD'
    )

    signos_temp = fields.Char(
        string = 'TEMP'
    )

    signos_fr_res = fields.Char(
        string = 'FR. RES.'
    )

    signos_f_c = fields.Char(
        string = 'F.C.'
    )

    signos_ll_cap = fields.Char(
        string = 'LL. CAP.'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )