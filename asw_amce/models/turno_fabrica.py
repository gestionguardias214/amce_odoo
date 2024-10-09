# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError


class asw_turno_fabrica(models.Model):
    _name = "asw.turno_fabrica"
    _inherit = ["asw.calcula.periodo"]
    _description = "Turnos fabrica"
    _rec_name = "id"
    _order = "id desc"

    tuf_fabrica = fields.Many2one(
        string="Fabrica",
        comodel_name="asw.fabrica",
        ondelete="restrict",
    )

    tuf_fecha = fields.Date(
        string="Fecha inicio",
        default=fields.Date.context_today,
    )

    tuf_cantdias = fields.Integer(
        string="Cantidad de dias",
    )

    tuf_lineas_turno_fabrica = fields.One2many(
        string="Lineas",
        comodel_name="asw.linea_turno_fabrica",
        inverse_name="ltf_turno_fabrica",
    )

    tuf_estado = fields.Selection(
        string="Estado",
        selection=[("borrador", "Borrador"), ("validado", "Validado")],
        default="borrador",
    )

    tuf_guardia = fields.One2many(
        string="Guardias",
        comodel_name="asw.guardia",
        inverse_name="gua_tuf",
    )

    tuf_prof_con = fields.One2many(
        string="Profesional concepto",
        comodel_name="asw.profesional_concepto",
        inverse_name="prc_tuf",
    )

    tuf_refuerzo = fields.Boolean(
        string="Todas las guardias son de Refuerzo?",
    )

    tuf_proyectos = fields.Many2one(
        string="Nombre del Proyecto", comodel_name="asw.proyectos", ondelete="set null"
    )

    def calcular(self):
        conf = self.env["asw.configuracion"].search([], limit=1)

        for record in self:
            record.tuf_lineas_turno_fabrica.unlink()

            for num_dia in range(record.tuf_cantdias):
                for turno in record.tuf_fabrica.fab_turno:
                    datetimeFormat = "%Y-%m-%d"
                    fecha = datetime.datetime.strptime(record.tuf_fecha, datetimeFormat)

                    nlinea = self.env["asw.linea_turno_fabrica"].create(
                        {
                            "ltf_turno_fabrica": record.id,
                            "ltf_fecha": fecha + timedelta(num_dia),
                            "ltf_turno": turno.id,
                            "ltf_vianda": conf.con_importe_vianda,
                            "ltf_refuerzo": self.tuf_refuerzo,
                        }
                    )
                    nlinea.compute_canthoras()

    def validar(self):
        linas_incompletas = self.tuf_lineas_turno_fabrica.filtered(
            lambda r: r.ltf_categoria.id == False or r.ltf_profesional.id == False
        )
        if len(linas_incompletas) > 0:
            raise ValidationError(
                "Existen linas que no se completaron, primero complete el profesional y la categoria y luego vuelva a intentarlo"
            )

        self.validar_lineas()

        concepto_vianda = self.env["asw.configuracion"].browse(1).con_concepto_vianda
        concepto_viatico = self.env["asw.configuracion"].browse(1).con_concepto_viatico
        for linea in self.tuf_lineas_turno_fabrica:
            linea._al_cambiar_fechas()
            periodo = self.obtenerPeriodo(
                linea.ltf_fecha_fin, linea.ltf_profesional.pro_grupo
            )

            guardia = self.env["asw.guardia"].create(
                {
                    "gua_profesional": linea.ltf_profesional.id,
                    "gua_categoria": linea.ltf_categoria.id,
                    "gua_ingreso": linea.ltf_fecha_inicio,
                    "state": "c",
                    "gua_egreso": linea.ltf_fecha_fin,
                    "gua_canthoras": linea.ltf_canthoras,
                    "gua_importe": linea.ltf_importe,
                    "gua_periodo": periodo.id,
                    "gua_tuf": self.id,
                    "gua_refuerzo": linea.ltf_refuerzo,
                }
            )

            if linea.ltf_vianda != 0.0:

                descripcion_vianda = "Turno Fabrica Nro %s por el concepto %s" % (
                    self.id,
                    concepto_vianda.descripcion,
                )
                self.env["asw.profesional_concepto"].create(
                    {
                        "prc_descripcion": descripcion_vianda,
                        "prc_profesional": linea.ltf_profesional.id,
                        "prc_concepto": concepto_vianda.id,
                        "prc_importe": linea.ltf_vianda,
                        "prc_periodo": periodo.id,
                        "prc_tuf": self.id,
                        "prc_guardia": guardia.id,
                    }
                )

            if linea.ltf_viatico != 0.0:
                descripcion_viatico = "Turno Fabrica Nro %s por el concepto %s" % (
                    self.id,
                    concepto_viatico.descripcion,
                )
                self.env["asw.profesional_concepto"].create(
                    {
                        "prc_descripcion": descripcion_viatico,
                        "prc_profesional": linea.ltf_profesional.id,
                        "prc_concepto": concepto_viatico.id,
                        "prc_importe": linea.ltf_viatico,
                        "prc_periodo": periodo.id,
                        "prc_tuf": self.id,
                        "prc_guardia": guardia.id,
                    }
                )
        self.tuf_estado = "validado"

    def validar_lineas(self):
        fechas = self.tuf_lineas_turno_fabrica.mapped("ltf_fecha")

        lineas = self.env["asw.linea_turno_fabrica"].search(
            [
                ("ltf_fecha", "in", fechas),
                ("id", "not in", self.tuf_lineas_turno_fabrica.ids),
                ("ltf_turno_fabrica.tuf_fabrica", "=", self.tuf_fabrica.id),
                ("ltf_turno_fabrica.tuf_estado", "=", "validado"),
            ]
        )

        if len(lineas) > 0:
            turnos = lineas.mapped("ltf_turno_fabrica")
            raise ValidationError(
                "No se puede validar este Turno de fabrica ya que los turnos %s tienen guardias generadas para los dias seleccionados"
                % (turnos.ids)
            )

    def checkeo(self):
        for record in self:
            for guardia in record.tuf_guardia:
                guardia.checkeo()

            for prc in record.tuf_prof_con:
                prc.unlink()

            for guardia in record.tuf_guardia:
                guardia.unlink()

    def cancelar(self):
        for record in self:
            record.checkeo()
            record.tuf_estado = "borrador"

    @api.multi
    def unlink(self):
        for record in self:
            record.checkeo()
            return super(asw_turno_fabrica, record).unlink()
