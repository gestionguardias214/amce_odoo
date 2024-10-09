# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError


class asw_fabrica(models.Model):
    _name = "asw.fabrica"
    _inherit = ["mail.thread"]
    _description = "Fabrica"
    _sql_constraints = [
        (
            "fab_codigo",
            "UNIQUE(fab_codigo)",
            "Ya se ha ingresado una fabrica con este codigo, por favor elija un codigo diferente",
        ),
    ]

    fab_codigo = fields.Char(
        string="Codigo",
        track_visibility="onchange",
        copy=False,
    )

    fab_descripcion = fields.Char(
        string="Descripcion",
        track_visibility="onchange",
    )

    name = fields.Char(
        string="Nombre",
        compute="_compute_name",
        store=True,
    )

    fab_turno = fields.One2many(
        string="Turnos",
        comodel_name="asw.turno",
        inverse_name="tur_fabrica",
    )

    fab_tuf = fields.One2many(
        string="Turno fabrica",
        comodel_name="asw.turno_fabrica",
        inverse_name="tuf_fabrica",
    )

    @api.depends("fab_codigo", "fab_descripcion")
    def _compute_name(self):
        for record in self:
            record.name = record.fab_codigo + " - " + record.fab_descripcion

    @api.multi
    def unlink(self):
        for record in self:
            if len(record.fab_tuf) > 0:
                raise ValidationError(
                    "No se puede eliminar porque la/s fabrica/s poseen relaciones con algun proceso de turnos fabrica"
                )
            else:
                return super(asw_fabrica, record).unlink()

    @api.model
    def default_get(self, vals):
        result = super(asw_fabrica, self).default_get(vals)
        result["fab_codigo"] = self.search([], order="id desc", limit=1).id + 1
        return result
