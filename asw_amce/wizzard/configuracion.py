# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_configuracion(models.Model):
    _name = "asw.configuracion"
    _inherit = ["mail.thread"]
    _description = "Configuracion"

    con_concepto = fields.Many2one(
        string="Concepto Presentismo",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    con_concepto_sac = fields.Many2one(
        string="Concepto de SAC",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    con_minutos_tolerancia = fields.Integer(string="Minutos de Tolerancia", default=15)

    con_concepto_guardia = fields.Many2one(
        string="Concepto de Guardia",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    con_concepto_vianda = fields.Many2one(
        string="Concepto de Vianda",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    con_concepto_viatico = fields.Many2one(
        string="Concepto de Viatico",
        comodel_name="asw.concepto",
        ondelete="restrict",
    )

    con_importe_vianda = fields.Float(
        string="Importe de Viandas",
    )

    def guardar(self):
        if len(self.env["asw.configuracion"].search([("id", "=", 1)])) == 0:
            self.env["asw.configuracion"].create({})

        self.env["asw.configuracion"].browse(1).write(
            {
                "con_concepto": self.con_concepto.id,
                "con_concepto_sac": self.con_concepto_sac.id,
                "con_minutos_tolerancia": self.con_minutos_tolerancia,
                "con_concepto_guardia": self.con_concepto_guardia.id,
                "con_concepto_vianda": self.con_concepto_vianda.id,
                "con_concepto_viatico": self.con_concepto_viatico.id,
                "con_importe_vianda": self.con_importe_vianda,
            }
        )

    @api.model
    def default_get(self, vals):
        result = super(asw_configuracion, self).default_get(vals)
        conf_guardada = self.search([], limit=1)

        result["con_concepto"] = conf_guardada.con_concepto.id or False
        result["con_concepto_sac"] = conf_guardada.con_concepto_sac.id or False
        result["con_minutos_tolerancia"] = conf_guardada.con_minutos_tolerancia or 0
        result["con_concepto_guardia"] = conf_guardada.con_concepto_guardia.id or False
        result["con_concepto_vianda"] = conf_guardada.con_concepto_vianda.id or False
        result["con_concepto_viatico"] = conf_guardada.con_concepto_viatico.id or False
        result["con_importe_vianda"] = conf_guardada.con_importe_vianda or 0

        return result
