# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_linea_liquidacion(models.Model):
    _name = "asw.linea_liquidacion"
    _inherit = ["mail.thread"]
    _description = "Linea de liquidacion"

    lin_concepto = fields.Many2one(
        string="Concepto",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    lin_importe = fields.Float(
        string="Importe",
    )

    lin_descripcion = fields.Char(
        string="Descripción",
    )

    lin_concepto_en_sac = fields.Boolean(
        string="Concepto incluiido en SAC",
        related="lin_concepto.con_sac",
    )

    lin_liquidacion = fields.Many2one(
        string="Liquidación",
        comodel_name="asw.liquidacion",
        ondelete="cascade",
    )
