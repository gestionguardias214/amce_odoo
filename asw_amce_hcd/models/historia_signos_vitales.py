# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_signos_vitales(models.Model):
    _name = "asw.historia_signos_vitales"
    _description = "Signos Vitales"

    hora = fields.Char(
        string=" Hora",
    )
    tas = fields.Char(
        string="TAS",
    )
    tad = fields.Char(
        string="TAD",
    )
    temperatura = fields.Char(
        string=" Temperatura",
    )
    frres = fields.Char(
        string=" FR. RES",
    )
    fc = fields.Char(
        string=" FC",
    )
    llcap = fields.Char(
        string=" LL. CAP.",
    )
    glisemia = fields.Char(
        string="Glicemia",
    )
    sat_oxigeno = fields.Char(
        string=" Sat. Oxigeno",
    )
