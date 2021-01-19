# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_usuario_app(models.Model):
    _name = 'asw.usuario_app'
    _description = 'Usuario de la APP'

    app_nombre = fields.Char(
        string=u'Nombre',
    )
    
    app_matricula = fields.Char(
        string=u'Matricula',
    )

    app_mail = fields.Char(
        string=u'Mail',
    )

    app_password = fields.Char(
        string=u'Password',
    )
    