# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError


class asw_concepto(models.Model):
    _name = "asw.concepto"
    _inherit = ["mail.thread", "asw.abm.base"]
    _description = "Concepto"
    _sql_constraints = [
        (
            "codigo_unique",
            "UNIQUE(codigo)",
            "Ya se ha ingresado un Concepto con este codigo, por favor ingrese un codigo diferente",
        ),
    ]

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("codigo", "=ilike", name), ("descripcion", operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    con_sac = fields.Boolean(
        string="Incluido en SAC",
    )

    active = fields.Boolean(
        string="Activo",
        default=True,
    )

    con_negativo = fields.Boolean(
        string="Negativo",
    )

    con_concepto = fields.One2many(
        string="Concepto",
        comodel_name="asw.profesional_concepto",
        inverse_name="prc_concepto",
    )

    con_concepto_guardia = fields.Boolean(
        string="Concepto de Guardia",
    )

    con_guardia = fields.Many2many(
        string="Guardias",
        comodel_name="asw.guardia",
        relation="asw_guardia_concepto",
        column1="guardia_id",
        column2="concepto_id",
    )

    @api.multi
    def unlink(self):
        for record in self:
            if (
                len(record.con_concepto) > 0
                and len(
                    self.env["asw.linea_liquidacion"].search(
                        [("lin_concepto", "=", record.id)]
                    )
                )
                > 0
            ):
                raise ValidationError(
                    "No se puede eliminar este concepto ya que posee uno o mas profesionales y liquidaciones asociados a el. Elimine estas relaciones para borrar el concepto."
                )

            elif len(record.con_concepto) > 0:
                raise ValidationError(
                    "No se puede eliminar este concepto ya que posee uno o mas profesionales asociados a el. Elimine estas relaciones para borrar el concepto."
                )

            elif (
                len(self.env["asw.linea_liquidacion"].search([("id", "=", record.id)]))
                > 0
            ):
                raise ValidationError(
                    "No se puede eliminar este concepto ya que posee una o mas liquidaciones asociadas a el. Elimine estas relaciones para borrar el concepto."
                )

            else:
                super(asw_concepto, record).unlink()

    @api.model
    def default_get(self, vals):
        result = super(asw_concepto, self).default_get(vals)
        result["codigo"] = self.search([], order="id desc", limit=1).id + 1
        return result
