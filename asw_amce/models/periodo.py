from openerp import models, fields, api
from odoo.exceptions import ValidationError


class asw_periodo(models.Model):
    _name = "asw.periodo"
    _inherit = ["mail.thread"]
    _description = "Periodos"
    _sql_constraints = [
        (
            "codigo_unique",
            "UNIQUE(per_codigo)",
            "El codigo ya esta usado en otro campo, por favor elija un codigo diferente",
        ),
    ]
    _order = "per_desde desc"

    per_codigo = fields.Char(
        string="Codigo",
        track_visibility="onchange",
    )

    per_descripcion = fields.Char(
        string="Descripcion",
        track_visibility="onchange",
    )

    per_cerrado = fields.Boolean(
        string="Cerrado",
        track_visibility="onchange",
    )

    per_desde = fields.Date(
        string="Fecha desde",
        default=fields.Date.context_today,
    )

    per_hasta = fields.Date(
        string="Fecha hasta",
        default=fields.Date.context_today,
    )

    name = fields.Char(
        string="Nombre",
        compute="_compute_name",
        store=True,
    )

    per_liquidacion = fields.One2many(
        string="Liquidaciones",
        comodel_name="asw.liquidacion",
        inverse_name="liq_periodo",
    )

    per_anio = fields.Many2one(
        string="Anio",
        comodel_name="asw.anio",
        ondelete="restrict",
    )

    per_desde = fields.Date(
        string="Fecha desde",
        default=fields.Date.context_today,
    )

    per_hasta = fields.Date(
        string="Fecha hasta",
        default=fields.Date.context_today,
    )

    per_guardia = fields.One2many(
        string="Guardias",
        comodel_name="asw.guardia",
        inverse_name="gua_periodo",
    )

    per_gru_ids = fields.Many2many(
        string="Grupos",
        comodel_name="asw.grupo",
        relation="asw_amce_periodo_grupo",
        column1="asw_grupo_id",
        column2="asw_periodo_id",
    )

    @api.depends("per_codigo", "per_descripcion")
    def _compute_name(self):
        for record in self:
            record.name = record.per_codigo + " - " + record.per_descripcion

    def checkeo(self):
        if len(self.env["asw.calculo_sac"].search([("sac_periodo", "=", self.id)])) > 0:
            raise ValidationError(
                "No se puede eliminar este periodo ya que posee uno o mas calculos de SAC relacionados. Elimine estas relaciones para borrar el periodo."
            )

        elif len(self.per_guardia) > 0:
            raise ValidationError(
                "No se puede eliminar este periodo ya que posee una o mas guardias asociadas a el. Elimine estas relaciones para borrar el periodo."
            )

        elif len(self.per_liquidacion) > 0:
            raise ValidationError(
                "No se puede eliminar este periodo ya que posee una o mas liquidaciones asociadas a el. Elimine estas relaciones para borrar el periodo."
            )

        else:
            return True

    @api.multi
    def unlink(self):
        for record in self:
            record.checkeo()
            super(asw_periodo, record).unlink()

    @api.model
    def default_get(self, vals):
        result = super(asw_periodo, self).default_get(vals)
        result["per_codigo"] = self.search([], order="id desc", limit=1).id + 1
        return result

    def get_esta_cerrado(self, grupos):

        grp_ids = self.per_gru_ids.mapped("id")
        list_grupo = set(grupos.ids)
        list_propios = set(grp_ids)

        inter = list_grupo.intersection(list_propios)
        return self.per_cerrado and len(inter) > 0
