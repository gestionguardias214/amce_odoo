# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta


class asw_inicio_guardia(models.TransientModel):
    _name = "asw.inicio_guardia"
    _description = "inicio_guardia"

    proc_profesional = fields.Many2one(
        string="Profesional",
        comodel_name="asw.profesionales",
        ondelete="restrict",
    )

    proc_categoria = fields.Many2one(
        string="Categoria", comodel_name="asw.categoria", ondelete="set null"
    )

    proc_precio_categoria = fields.Float(
        string="Precio categoria", compute="_compute_precioxhora"
    )

    proc_fechahora = fields.Datetime(
        string="Fecha y hora",
        default=fields.Datetime.now,
    )

    proc_observaciones = fields.Text(
        string="Observaciones",
    )

    proc_tolerancia = fields.Integer(
        string="Minutos de Tolerancia",
    )

    proc_profesional_concepto = fields.Many2many(
        string="Profesional concepto",
        comodel_name="asw.conceptos.aux",
        relation="asw_amce_inicio_guardia_conceptos_aux",
        column1="asw_conceptos_aux_id",
        column2="asw_inicio_guardia_id",
    )

    @api.model
    def create(self, vals):
        # Agregar codigo de validacion aca
        result = super(asw_inicio_guardia, self).create(vals)
        return result

    @api.model
    def default_get(self, vals):
        result = super(asw_inicio_guardia, self).default_get(vals)
        tolerancia = (
            self.env["asw.configuracion"].search([], limit=1).con_minutos_tolerancia
            or 0
        )
        result["proc_tolerancia"] = tolerancia

        actual = datetime.now()
        minutos = actual.minute
        resta = 0
        if minutos <= tolerancia:
            resta = minutos
        fecha_propone = actual - timedelta(minutes=resta)
        formato = "%Y-%m-%d %H:%M:%S"

        result["proc_fechahora"] = fecha_propone.strftime(formato)

        # conceptos = self.env['asw.concepto'].search([( 'con_concepto_guardia' , '=' , True )]).ids
        # lista_con = []
        # for con in conceptos:
        #     prc = self.proc_profesional_concepto.create(({
        #         'aux_concepto': con,
        #     }))
        #     lista_con.append(prc.id)
        # result['proc_profesional_concepto'] = [(6,0, lista_con)]

        return result

    @api.onchange("proc_profesional")
    def _compute_cat(self):
        if self.proc_profesional.id != False:
            result = {}
            result["domain"] = []
            ids = self.proc_profesional.pro_categoria.ids
            result["domain"] = {"proc_categoria": [("id", "in", ids)]}

            return result
        else:
            result = {}
            result["domain"] = []
            return result

    def crear_registro(self):
        for record in self:
            guardia = self.env["asw.guardia"].create(
                {
                    "gua_profesional": record.proc_profesional.id,
                    "gua_categoria": record.proc_categoria.id,
                    "state": "a",
                    "gua_ingreso": record.proc_fechahora,
                    "gua_observaciones": record.proc_observaciones,
                }
            )

            for id in record.proc_profesional_concepto.ids:
                prof_con = self.env["asw.profesional_concepto"].browse(id)

                prof_con.write(
                    {
                        "prc_profesional": record.proc_profesional.id,
                        "prc_guardia": guardia.id,
                        "prc_descripcion": "%s - %s %s"
                        % (
                            prof_con.prc_concepto.name,
                            guardia.id,
                            record.proc_fechahora,
                        ),
                    }
                )

    @api.depends("proc_categoria")
    def _compute_precioxhora(self):
        for record in self:
            record.proc_precio_categoria = record.proc_categoria._compute_buscar_precio(
                record.proc_fechahora
            )
