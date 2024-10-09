# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_usuario_app(models.Model):
    _name = "asw.usuario_app"
    _description = "Usuario de la APP"

    app_nombre = fields.Char(
        string="Nombre",
    )

    app_matricula = fields.Char(
        string="Matricula",
    )

    app_mail = fields.Char(
        string="Mail",
    )

    app_password = fields.Char(
        string="Password",
    )
