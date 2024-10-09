# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError


class asw_liquidacion(models.Model):
    _name = "asw.liquidacion"
    _inherit = ["mail.thread"]
    _description = "Liquidacion"
    _order = "id desc"

    liq_profesional = fields.Many2one(
        string="Profesional",
        comodel_name="asw.profesionales",
        ondelete="restrict",
    )

    liq_periodo = fields.Many2one(
        string="Período de liquidación",
        comodel_name="asw.periodo",
        ondelete="restrict",
    )

    liq_fecha = fields.Date(
        string="Fecha de liquidación",
        default=fields.Date.context_today,
    )

    liq_periodo_cerrado = fields.Boolean(
        string="Periodo Cerrado",
        related="liq_periodo.per_cerrado",
    )

    liq_importe = fields.Float(
        string="Importe total liquidado", compute="_compute_importe"
    )

    liq_lineas = fields.One2many(
        string="Lineas de liquidación",
        comodel_name="asw.linea_liquidacion",
        inverse_name="lin_liquidacion",
    )

    name = fields.Char(
        string="Nombre",
        compute="_compute_name",
        store=True,
    )

    liq_tipo = fields.Selection(
        string="Tipo",
        selection=[("normal", "Normal"), ("sac", "SAC")],
        default="normal",
    )

    liq_guardia = fields.One2many(
        string="Guardias",
        comodel_name="asw.guardia",
        inverse_name="gua_liquidacion",
    )

    liq_cant_guardias = fields.Integer(
        string="Cant de guardias", compute="_compute_cant_guardias"
    )

    liq_semestre = fields.Selection(
        string="Semetre",
        selection=[("primero", "Primero"), ("segundo", "Segundo")],
        compute="_compute_semestre",
        store=True,
    )

    liq_sac = fields.Many2one(
        string="Liquidaciones sac",
        comodel_name="asw.calculo_sac",
        ondelete="restrict",
    )

    liq_monto_aplicable_sac = fields.Float(
        string="Monto para calcular SAC",
    )

    name = fields.Char(
        string="Nombre",
        compute="_compute_name",
        store=True,
    )

    liq_grupo = fields.Many2one(
        string="Grupo",
        comodel_name="asw.grupo",
        ondelete="restrict",
        related="liq_profesional.pro_grupo",
        store=True,
    )

    liq_liquidaciones_sac = fields.Many2one(
        string="Liquidacion de SAC",
        comodel_name="asw.liquidacion",
        ondelete="set null",
    )

    liq_liq_sac_ids = fields.One2many(
        string="Liquidaciones",
        comodel_name="asw.liquidacion",
        inverse_name="liq_liquidaciones_sac",
    )

    liq_proc_id = fields.Many2one(
        string="Proceso de Liquidación",
        comodel_name="asw.proceso_liquidacion",
        ondelete="restrict",
    )

    liq_ult_mail = fields.Many2one(
        string="ültimo mail enviado",
        comodel_name="mail.mail",
        ondelete="set null",
    )

    liq_estado_mail = fields.Selection(
        string="Estado del Mail",
        related="liq_ult_mail.state",
        store=True,
    )

    def importe_guardia(self):
        guardias = self.liq_guardia.mapped("gua_importe")
        result = sum(guardias)
        return result

    def importe_concepto(self, concepto):
        lineas = self.liq_lineas.filtered(lambda r: r.lin_concepto.id == concepto.id)
        importe = lineas.mapped("lin_importe")
        suma = sum(importe)
        return suma

    def calcular_monto_sac(self):
        for record in self:
            lineas_aplica = record.liq_lineas.filtered(
                lambda r: r.lin_concepto.con_sac == True
            )

            monto_concepto = sum(lineas_aplica.mapped("lin_importe"))
            monto_guardias = sum(record.liq_guardia.mapped("gua_importe"))
            record.liq_monto_aplicable_sac = monto_concepto + monto_guardias

    @api.depends("liq_guardia")
    def _compute_cant_guardias(self):
        for record in self:
            record.liq_cant_guardias = self.env["asw.guardia"].search_count(
                [("gua_liquidacion", "=", record.id)]
            )

    @api.depends("liq_fecha")
    def _compute_semestre(self):
        for record in self:
            if record.liq_fecha != False:
                mes = int(record.liq_fecha[5:7])
                if mes <= 6:
                    record.liq_semestre = "primero"
                else:
                    record.liq_semestre = "segundo"

    @api.depends("liq_lineas")
    def _compute_importe(self):
        for record in self:
            conceptos = sum(record.liq_lineas.mapped("lin_importe"))
            guardias = sum(record.liq_guardia.mapped("gua_importe"))
            record.liq_importe = round(conceptos + guardias, 2)
            # for i in record.liq_lineas:
            #     record.liq_importe = record.liq_importe+i.lin_importe

    def enviar_mail_masivo(self):

        for record in self:
            record.enviar_mail()

    def enviar_mail(self):
        docargs = {
            "doc_ids": self.id,
            "doc_model": "asw.liquidacion",
            "docs": self,
        }
        body = self.env["report"].render("asw_amce.pdfliquidacion", docargs)
        mail = self.env["mail.mail"].create(
            {
                "subject": "Liquidacion",
                "reply_to": "gestionguardias214@gmail.com",
                "email_to": self.liq_profesional.email,
                "body_html": body,
                "message_type": "email",
                "model": "asw.liquidacion",
                "res_id": self.id,
            }
        )
        mail.send()
        self.liq_ult_mail = mail

    @api.multi
    def invoice_print(self):
        return self.env["report"].get_action(self, "asw_amce.pdfliquidacion")

    @api.depends("liq_profesional", "liq_periodo")
    def _compute_name(self):
        for record in self:
            record.name = record.liq_profesional.name + " - " + record.liq_periodo.name

    @api.multi
    def unlink(self):
        for record in self:
            if record.liq_periodo.get_esta_cerrado(record.liq_grupo):
                raise ValidationError(
                    "No se puede eliminar esta liquidacion ya que el periodo al que pertenece esta cerrado."
                )
            else:
                record.liq_lineas.unlink()
                record.liq_guardia.write({"state": "c"})
                super(asw_liquidacion, record).unlink()

    @api.multi
    def write(self, vals):
        for record in self:
            if record.liq_periodo.get_esta_cerrado(record.liq_grupo):
                raise ValidationError(
                    "No se puede editar esta liquidacion ya que el periodo al que pertenece esta cerrado."
                )

            super(asw_liquidacion, record).write(vals)
        return True
