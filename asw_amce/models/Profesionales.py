# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from datetime import timedelta, date
from odoo.exceptions import ValidationError


class asw_profesionales(models.Model):
    _name = "asw.profesionales"
    _inherit = ["mail.thread"]
    _inherits = {"res.partner": "partner_id"}
    _description = "Profesionales"
    _rec_name = "pro_nombre_mostrar"
    _order = "name"

    _sql_constraints = {
        (
            "codigo_unique",
            "UNIQUE(pro_codigo)",
            "No puede haber dos profesionales con el mismo codigo",
        ),
        # ('cbu_unique', 'UNIQUE(pro_cbu)', 'No puede haber dos profesionales con el mismo cbu'),
    }

    partner_id = fields.Many2one(
        string="Partner Asociado",
        comodel_name="res.partner",
        required=True,
        ondelete="cascade",
    )

    pro_codigo = fields.Char(
        string="Código",
        required=True,
        track_visibility="onchange",
        copy=False,
        default="",
    )

    pro_matricula = fields.Char(
        string="MatrIcula",
    )

    pro_cbu = fields.Char(
        string="CBU",
        track_visibility="onchange",
    )

    pro_email = fields.Char(
        string="Email",
    )

    pro_telefono = fields.Char(
        string="Telefono",
    )

    pro_nombre = fields.Char(
        string="Nombre",
    )

    pro_nombre_mostrar = fields.Char(
        string="Nombre", compute="_compute_name", store="True"
    )

    active = fields.Boolean(
        string="Activo",
        default=True,
        track_visibility="onchange",
    )

    pro_grupo = fields.Many2one(
        string="Grupo",
        comodel_name="asw.grupo",
        ondelete="restrict",
    )

    pro_categoria = fields.Many2many(
        string="Categoria",
        comodel_name="asw.categoria",
        relation="asw_profesional_categoria",
        column1="asw_categoria_id",
        column2="asw_profesionales_id",
    )

    pro_guardia = fields.One2many(
        string="Guardia",
        comodel_name="asw.guardia",
        inverse_name="gua_profesional",
    )

    pro_liquidacion = fields.One2many(
        string="Liquidaciones",
        comodel_name="asw.liquidacion",
        inverse_name="liq_profesional",
    )

    pro_vto_poliza = fields.Date(
        string="Vto poliza de mala praxis",
        default=fields.Date.context_today,
    )

    pro_vto_examenes = fields.Date(
        string="Vto examenes periodicos",
        default=fields.Date.context_today,
    )

    # vto licencia
    pro_vto_licencia = fields.Date(
        string="Vto licencia de conducir",
    )

    prox_venc_lic = fields.Boolean(
        string="Licencia proxima a vencer",
        compute="_compute_venc",
        search="_search_prox_venc_lic",
    )

    pro_concepto = fields.One2many(
        string="Concepto",
        comodel_name="asw.profesional_concepto",
        inverse_name="prc_profesional",
    )

    pro_estado = fields.Selection(
        string="Estado",
        selection=[("disponible", "Disponible"), ("en_guardia", "En Guardia")],
        compute="_compute_pro_estado",
        search="_estado_search",
    )

    # vto examenes
    pro_vto_examenes = fields.Date(
        string="Vto examenes periodicos",
    )

    prox_venc_exa = fields.Boolean(
        string="Examenes proximos a vencer",
        compute="_compute_venc",
        search="_search_prox_venc_exa",
    )

    # vto poliza
    pro_vto_poliza = fields.Date(
        string="Vto poliza de mala praxis",
    )

    prox_venc_pol = fields.Boolean(
        string="Poliza pronta a vencer",
        compute="_compute_venc",
        search="_search_prox_venc_pol",
    )

    pro_fecha_alta = fields.Date(
        string="Fecha de Alta",
    )

    pro_fecha_baja = fields.Date(
        string="Fecha de Baja",
    )

    pro_fecha_ultimo_sac = fields.Date(
        string="Fecha de último SAC",
    )

    def _compute_pro_estado(self):
        for record in self:
            record.pro_estado = "disponible"

    def _estado_search(self, name, args=None, operator="=", limit=100):
        guardias_abiertas = self.env["asw.guardia"].search([("state", "=", "a")])
        profesionales_ocupados = guardias_abiertas.mapped("gua_profesional")
        operador = "not in"
        if name == "!=":
            operador = "in"
        return [("id", operador, profesionales_ocupados.ids)]

    # def _nombre_search(self,name, args=None, operator='=', limit=100):
    #     return ['|', ('pro_codigo', operator , args),('name', operator, args)]

    @api.depends("pro_codigo", "name")
    def _compute_name(self):
        for record in self:
            record.pro_nombre_mostrar = record.pro_codigo + " - " + record.name or ""

    def _compute_venc(self):
        pass

    def _search_prox_venc_lic(self, operator, value):
        filtro = self.obtenerfiltro("pro_vto_licencia")
        return filtro

    def _search_prox_venc_exa(self, operator, value):
        filtro = self.obtenerfiltro("pro_vto_examenes")
        return filtro

    def _search_prox_venc_pol(self, operator, value):
        filtro = self.obtenerfiltro("pro_vto_poliza")
        return filtro

    def obtenerfiltro(self, campo):
        datetimeFormat = "%Y-%m-%d"
        dias = 15
        date_e = (date.today() + timedelta(days=dias)).strftime(datetimeFormat)
        date_e = datetime.datetime.strptime(date_e, datetimeFormat)
        return [(campo, "<=", date_e)]

    # @api.onchange('pro_grupo')
    # def onchange_filtro(self):
    #     result = {}
    #     result['domain'] = []
    #     registros = self.env['asw.categoria'].search([('cat_grupo','ilike',self.pro_grupo.id)])
    #     result['domain'] = {'pro_categoria' : [('id', 'in', registros.ids)]}
    #     return result

    @api.multi
    def unlink(self):
        for record in self:
            if (
                len(record.pro_guardia) > 0
                and len(record.pro_liquidacion) > 0
                and len(record.pro_concepto) > 0
            ):
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas guardias, liquidaciones, y conceptos asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_guardia) > 0 and len(record.pro_liquidacion) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas guardias y liquidaciones asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_guardia) > 0 and len(record.pro_concepto) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas guardias y conceptos asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_liquidacion) > 0 and len(record.pro_concepto) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas liquidaciones, y conceptos asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_guardia) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas guardias asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_liquidacion) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee una o mas liquidaciones asociadas a el. Elimine estas relaciones para borrar el profesional."
                )

            elif len(record.pro_concepto) > 0:
                raise ValidationError(
                    "No se puede eliminar este profesional ya que posee uno o mas conceptos asociados a el. Elimine estas relaciones para borrar el profesional."
                )

            else:
                super(asw_profesionales, record).unlink()

    @api.model
    def default_get(self, vals):
        result = super(asw_profesionales, self).default_get(vals)
        result["pro_codigo"] = self.search([], order="id desc", limit=1).id + 1
        return result
