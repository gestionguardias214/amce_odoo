# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_envio_masivo(models.TransientModel):
    _name = "asw.envio.masivo"

    enl_profesionales = fields.Many2many(
        string="Profesionales",
        comodel_name="asw.profesionales",
        relation="asw_liquidacion_envio_profesionales",
        column1="asw_profesionales_id",
        column2="asw_envio_masivo_id",
    )

    enl_enviado = fields.Boolean(
        string="Enviado",
        default=False,
    )

    enl_liquidaciones = fields.Many2many(
        string="Liquidaciones",
        comodel_name="asw.liquidacion",
        relation="asw_liquidacion_envio_liquidaciones",
        column1="asw_liquidacion_id",
        column2="asw_envio_masivo_id",
    )

    @api.model
    def default_get(self, fields):
        # Agregar codigo de validacion aca
        liq_ids = self.env.context.get("active_ids", [])
        result = super(asw_envio_masivo, self).default_get(fields)
        liquidaciones = self.env["asw.liquidacion"].search([("id", "in", liq_ids)])
        prof = liquidaciones.mapped("liq_profesional")
        result["enl_profesionales"] = [(6, 0, prof.ids)]

        return result

    @api.multi
    def enviar_mail(self):
        liq_ids = self.env.context.get("active_ids", [])
        liquidaciones = self.env["asw.liquidacion"].search([("id", "in", liq_ids)])
        liquidaciones.enviar_mail_masivo()
        self.enl_liquidaciones = [(6, 0, liquidaciones.ids)]
        self.enl_enviado = True
        return {
            "type": "ir.actions.act_window",
            "res_model": "asw.envio.masivo",
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }
