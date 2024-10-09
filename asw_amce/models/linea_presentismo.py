# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_linea_presentismo(models.Model):
    _name = "asw.linea_presentismo"
    _inherit = ["mail.thread"]
    _description = "Lineas de presentismo"

    lpr_profesional = fields.Many2one(
        string="Profesional",
        comodel_name="asw.profesionales",
        ondelete="restrict",
    )

    lpr_profesional_concepto = fields.One2many(
        string="Concepto Generado",
        comodel_name="asw.profesional_concepto",
        inverse_name="prc_linea_presentismo",
    )

    lpr_importe = fields.Float(compute="_compute_lpr_importe")

    lpr_presentismo = fields.Many2one(
        string="Presentismo",
        comodel_name="asw.presentismo",
        ondelete="cascade",
    )

    @api.depends("lpr_profesional_concepto")
    def _compute_lpr_importe(self):
        for record in self:
            record.lpr_importe = sum(
                record.lpr_profesional_concepto.mapped("prc_importe")
            )
