# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from datetime import timedelta, date


class asw_turno(models.Model):
    _name = "asw.turno"
    _inherit = ["mail.thread"]
    _description = "Turnos"

    tur_inicio = fields.Float(
        string="Inicio",
    )

    tur_fin = fields.Float(
        string="Fin",
    )

    tur_fabrica = fields.Many2one(
        string="Fabrica",
        comodel_name="asw.fabrica",
        ondelete="restrict",
    )

    tur_canthoras = fields.Integer(
        string="Cantidad de horas", compute="_compute_canthoras"
    )

    name = fields.Char(string="Nombre", compute="_compute_name")

    @api.depends("tur_inicio", "tur_fin")
    def _compute_name(self):
        for record in self:
            if len(record.tur_fabrica) > 0:
                record.name = str(record.tur_inicio) + " - " + str(record.tur_fin)

    @api.depends("tur_inicio", "tur_fin")
    def _compute_canthoras(self):
        for record in self:
            datetimeFormat = "%Y-%m-%d"
            newdatetimeFormat = "%Y-%m-%d %H:%M:%S"

            inicio = date.today()
            inicio = inicio.strftime(datetimeFormat)
            inicio = inicio + " 00:00:00"
            inicio = datetime.datetime.strptime(inicio, newdatetimeFormat)
            inicio = inicio + timedelta(hours=record.tur_inicio)

            fin = date.today()
            fin = fin.strftime(datetimeFormat)
            fin = fin + " 00:00:00"
            fin = datetime.datetime.strptime(fin, newdatetimeFormat)
            fin = fin + timedelta(hours=record.tur_fin)

            if record.tur_inicio > record.tur_fin:
                fin = fin + timedelta(days=1)

            record.tur_canthoras = (fin - inicio).seconds / 60 / 60
