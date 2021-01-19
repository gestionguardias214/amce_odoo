# -*- coding: utf-8 -*-
from openerp import api, models, fields

class asw_score(models.Model):
    _name = 'asw.score'
    _description = 'Score de Glasgow'
    _ord = 'score_hora'
    _rec_name = 'score_total'

    score_hora = fields.Char(
        string = 'Hora'
    )

    score_o = fields.Char(
        string = 'O'
    )

    score_m = fields.Char(
        string = 'M'
    )

    score_v = fields.Char(
        string = 'V'
    )

    score_total = fields.Char(
        string = 'Total'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )