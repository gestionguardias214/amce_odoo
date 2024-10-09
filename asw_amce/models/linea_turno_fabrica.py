# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from datetime import datetime, date, time, timedelta


class asw_linea_turno_fabrica(models.Model):
    _name = "asw.linea_turno_fabrica"
    _inherit = ["mail.thread"]
    _description = "Lineas tuf"

    ltf_turno_fabrica = fields.Many2one(
        string="Turno fabrica",
        comodel_name="asw.turno_fabrica",
        ondelete="restrict",
    )

    ltf_fecha = fields.Date(
        string="Fecha",
        default=fields.Date.context_today,
    )

    ltf_turno = fields.Many2one(
        string="Turno",
        comodel_name="asw.turno",
        ondelete="restrict",
    )

    ltf_fecha_fin = fields.Datetime(
        string="Fecha de Fin", compute="_compute_ltf_fecha_inicio", store=True
    )

    ltf_fecha_inicio = fields.Datetime(
        string="Fecha de Inicio", compute="_compute_ltf_fecha_inicio", store=True
    )

    ltf_profesional = fields.Many2one(
        string="Profesional",
        comodel_name="asw.profesionales",
        ondelete="restrict",
    )

    ltf_categoria = fields.Many2one(
        string="Categoria",
        comodel_name="asw.categoria",
        ondelete="restrict",
        domain="[('cat_es_fabrica', '=', True)]",
    )

    ltf_canthoras = fields.Float(
        string="Cantidad de horas",
        compute="_al_cambiar_fechas",
    )

    ltf_precio = fields.Float(
        string="Precio",
        compute="_compute_precio",
    )

    ltf_importe = fields.Float(string="Importe", compute="_compute_importe")

    ltf_viatico = fields.Float(
        string="Viatico",
    )

    ltf_vianda = fields.Float(
        string="Vianda",
    )

    ltf_total = fields.Float(string="Total", compute="_compute_total")

    ltf_refuerzo = fields.Boolean(
        string="Es Refuerzo?",
    )

    @api.depends("ltf_turno", "ltf_fecha")
    def _compute_ltf_fecha_inicio(self):
        for record in self:
            fecha_inicio = datetime.strptime(record.ltf_fecha, "%Y-%m-%d")
            hora_inicio = record.ltf_turno
            horas = int(record.ltf_turno.tur_inicio) - 4.5
            minutos = (record.ltf_turno.tur_inicio - horas) * 100
            fecha_inicio = (
                fecha_inicio + timedelta(hours=horas) + timedelta(minutes=minutos)
            )
            fecha_fin = fecha_inicio + timedelta(
                hours=int(record.ltf_turno.tur_canthoras)
            )

            record.ltf_fecha_inicio = fecha_inicio
            record.ltf_fecha_fin = fecha_fin

    @api.onchange("ltf_categoria")
    def _compute_precio(self):
        for record in self:
            precio = record.ltf_categoria._compute_buscar_precio(record.ltf_fecha)
            record.ltf_precio = precio

    @api.onchange("ltf_profesional")
    def _compute_cat(self):
        for record in self:
            if record.ltf_profesional.id != False:
                result = {}
                result["domain"] = []
                ids = record.ltf_profesional.pro_categoria.ids
                result["domain"] = {
                    "ltf_categoria": [("id", "in", ids), ("cat_es_fabrica", "=", True)]
                }

                return result
            else:
                result = {}
                result["domain"] = []
                return result

    @api.onchange("ltf_fecha_inicio", "ltf_fecha_fin")
    def _al_cambiar_fechas(self):
        for record in self:
            inicio = fields.Datetime.from_string(record.ltf_fecha_inicio)
            fin = fields.Datetime.from_string(record.ltf_fecha_fin)
            diferencia = fin - inicio
            if diferencia.total_seconds() <= 0:
                raise exceptions.ValidationError(
                    "La cantidad de horas entre la fecha de inicio y fin no puede ser inferior o igual a cero, por favor revise las fechas"
                )

            record.ltf_canthoras = round(float(diferencia.total_seconds() / 3600), 2)
            # record.ltf_fecha = inicio
            record._compute_importe()
            record._compute_total()

    def compute_canthoras(self):
        for record in self:
            record.ltf_canthoras = record.ltf_turno.tur_canthoras

    @api.depends("ltf_canthoras", "ltf_precio")
    def _compute_importe(self):
        for record in self:
            record.ltf_importe = record.ltf_canthoras * record.ltf_precio

    @api.depends("ltf_importe", "ltf_viatico", "ltf_vianda")
    def _compute_total(self):
        for record in self:
            record.ltf_total = (
                record.ltf_importe + record.ltf_viatico + record.ltf_vianda
            )
