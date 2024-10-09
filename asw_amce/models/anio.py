# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class asw_anio(models.Model):
    _name = "asw.anio"
    _inherit = ["mail.thread"]
    _description = "Anio"
    _rec_name = "ani_numero"
    _order = "ani_numero desc"
    _sql_constraints = [
        (
            "ani_numero_unique",
            "UNIQUE(ani_numero)",
            "No puede crearse dos años iguales, por favor revise el año ingresado",
        ),
    ]

    ani_numero = fields.Integer(
        string="Año",
        default=2018,
    )

    ani_inicio = fields.Date(
        string="Fecha de Inicio",
        default=fields.Date.context_today,
        compute="cambiar_inicio",
    )

    ani_fin = fields.Date(
        string="Fecha de Fin",
        default=fields.Date.context_today,
        compute="cambiar_fin",
    )

    ani_periodo = fields.One2many(
        string="Periodos",
        comodel_name="asw.periodo",
        inverse_name="per_anio",
    )

    state = fields.Selection(
        string="state",
        selection=[("borrador", "Borrador"), ("procesado", "Procesado")],
        default="borrador",
    )

    @api.depends("ani_numero")
    def cambiar_inicio(self):
        for record in self:
            if record.ani_numero > 2000:
                string = str(record.ani_numero)
                string += "-01-01"
                record.ani_inicio = string

    @api.depends("ani_numero")
    def cambiar_fin(self):
        for record in self:
            if record.ani_numero > 2000:
                string = str(record.ani_numero)
                string += "-12-31"
                record.ani_fin = string

    def nombremes(self, num):
        switcher = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        return switcher.get(num, "Invalid month")

    def generar_periodos(self):
        for record in self:
            if len(record.ani_periodo) != 0:
                record.ani_periodo.unlink()

            for i in range(12):
                mes = i + 1
                codigo = str(mes)
                codigo += "/"
                codigo += str(record.ani_numero)

                descripcion = self.nombremes(mes)

                desde = str(record.ani_numero)
                desde += "-"
                if mes < 10:
                    desde += "0"
                desde += str(mes)
                desde += "-"
                desde += "01"

                if mes == 12:
                    hasta = str(record.ani_numero + 1)
                    hasta += "-"
                    hasta += "01"
                    hasta += "-"
                    hasta += "01"
                else:
                    hasta = str(record.ani_numero)
                    hasta += "-"
                    if mes < 9:
                        hasta += "0"
                    hasta += str(mes + 1)
                    hasta += "-"
                    hasta += "01"
                hasta = datetime.strptime(hasta, "%Y-%m-%d") - timedelta(days=1)

                self.env["asw.periodo"].create(
                    {
                        "per_anio": record.id,
                        "per_codigo": codigo,
                        "per_descripcion": descripcion,
                        "per_desde": desde,
                        "per_hasta": hasta,
                    }
                )

            record.state = "procesado"

    @api.multi
    def unlink(self):
        for record in self:
            periodos = record.ani_periodo.mapped("per_cerrado")
            if any(periodos):
                raise ValidationError(
                    "El año no puede eliminarse ya que posee periodos cerrados"
                )

            for per in record.ani_periodo:
                per.checkeo()
            record.ani_periodo.unlink()
            super(asw_anio, record).unlink()
