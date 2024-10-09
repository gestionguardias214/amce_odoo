# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from odoo.exceptions import ValidationError
from datetime import timedelta, date


class asw_precio_categoria(models.Model):
    _name = "asw.precio_categoria"
    _inherit = ["mail.thread", "asw.calcula.periodo"]
    _description = "Precio de categoria"
    _order = "pca_fecha desc"
    _rec_name = "id"

    pca_categoria = fields.Many2one(
        string="Categoría",
        comodel_name="asw.categoria",
        ondelete="restrict",
        track_visibility="onchange",
    )

    pca_fecha = fields.Date(
        string="Fecha desde",
        default=fields.Date.context_today,
    )

    pca_precio = fields.Float(
        string="Precio",
        track_visibility="onchange",
    )

    pca_act_precio = fields.Many2one(
        string="Proceso de Actualización de precio",
        comodel_name="asw.actualizacion_precio",
        ondelete="set null",
    )

    pca_guardias_emitidas = fields.Boolean(
        string="Posee Guardias emitidas", compute="_compute_pca_guardias_emitidas"
    )

    pca_periodo_cerrado = fields.Boolean(
        string="Periodo Cerrado", compute="_compute_pca_periodo_cerrado"
    )

    pca_periodo = fields.Many2one(
        string="Periodo",
        comodel_name="asw.periodo",
        ondelete="set null",
        compute="_compute_pca_periodo_cerrado",
    )

    def _compute_pca_periodo_cerrado(self):
        for record in self:
            fecha = fields.Datetime.from_string(self.pca_fecha)
            fecha_busqueda = fields.Datetime.to_string(fecha + timedelta(hours=12))
            grupo = self.pca_categoria.cat_grupo
            periodo = self.obtenerPeriodo(fecha_busqueda, self.pca_categoria.cat_grupo)
            record.pca_periodo = periodo
            record.pca_periodo_cerrado = periodo.get_esta_cerrado(grupo)

    def _compute_pca_guardias_emitidas(self):
        for record in self:
            guardias = record.get_guardias_registro()
            record.pca_guardias_emitidas = len(guardias) > 0

    @api.model
    def create(self, vals):
        # Agregar codigo de validacion aca
        precio = vals["pca_precio"]
        if float(precio) == 0:
            raise exceptions.ValidationError(
                "No puede crearse un registro de Precio de Categoria con un Precio igual a 0"
            )

        result = super(asw_precio_categoria, self).create(vals)
        result.actualizar_precio_guardias()

        return result

    def actualizar_precio_guardias(self):
        guardias = self.get_guardias_registro()
        guardias.actualizar_precio()

    def get_guardias_registro(self):
        guardias = self.env["asw.guardia"].search(
            [
                ("gua_categoria", "=", self.pca_categoria.id),
                ("gua_ingreso", ">=", self.pca_fecha),
            ]
        )
        return guardias

    @api.multi
    def write(self, vals):
        # Agregar codigo de validacion aca
        if "pca_precio" in vals:
            precio = vals["pca_precio"]
            if float(precio) == 0:
                raise exceptions.ValidationError(
                    "No puede crearse un registro de Precio de Categoria con un Precio igual a 0"
                )

        if self.pca_periodo_cerrado:
            raise ValidationError(
                "No se puede modificarse este precio categoria ya que pertenece a un periodo que se encuentra cerrado"
            )

        return super(asw_precio_categoria, self).write(vals)

    def checkeo(self):
        for record in self:
            if len(
                self.env["asw.guardia"].search([("gua_ingreso", ">", record.pca_fecha)])
            ):
                raise ValidationError(
                    "No se puede eliminar este precio categoria ya que existen guardias emitidas luego de su fecha."
                )
            else:
                return True

    @api.multi
    def unlink(self):
        # Agregar codigo de validacion aca
        result = True
        for record in self:
            record.checkeo()
            result = super(asw_precio_categoria, record).unlink()

        return result
