# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime


class asw_actualizacion_precio(models.Model):
    _name = "asw.actualizacion_precio"
    _inherit = ["mail.thread"]
    _description = "Actualizacion de precios"
    # _sql_constraints = {
    #     ('desde_unique', 'UNIQUE(acp_fecha_desde)', 'Ya se han actualizado los precios desde esa fecha, ingrese una fecha diferente'),
    # }

    acp_estado = fields.Selection(
        string="Estado",
        selection=[("borrador", "Borrador"), ("validado", "Validado")],
        default="borrador",
    )

    acp_fecha_desde = fields.Date(
        string="Fecha desde",
        default=fields.Date.context_today,
    )

    acp_grupo = fields.Many2many(
        string="Grupos",
        comodel_name="asw.grupo",
        relation="asw_grupo_precio",
        column1="grupo_id",
        column2="actualizacion_precio_id",
    )

    acp_porcentaje = fields.Float(
        string="Porcentaje de actualizacion",
    )

    acp_linea_actualizacion = fields.One2many(
        string="Lineas de actualizacion",
        comodel_name="asw.linea_actualizacion",
        inverse_name="lia_actualizacion",
    )

    name = fields.Char(
        string="Nombre",
        compute="_compute_name",
        store=True,
    )

    acp_pca_ids = fields.One2many(
        string="Precios de Categorias",
        comodel_name="asw.precio_categoria",
        inverse_name="pca_act_precio",
    )

    @api.depends("acp_fecha_desde")
    def _compute_name(self):
        for record in self:
            record.name = str(record.id) + " - " + record.acp_fecha_desde

    def aumentar(self):
        for record in self:
            for linea in record.acp_linea_actualizacion:
                linea.lia_precio_nuevo += (
                    linea.lia_precio_actual * record.acp_porcentaje / 100
                )

    def disminuir(self):
        for record in self:
            for linea in record.acp_linea_actualizacion:
                linea.lia_precio_nuevo -= (
                    linea.lia_precio_actual * record.acp_porcentaje / 100
                )

    @api.multi
    def agregar(self):
        result = {"value": {"acp_linea_actualizacion": []}}

        self.acp_linea_actualizacion.unlink()

        for group in self.acp_grupo:
            precio = 0
            for cat in group.gru_categoria:

                fecha = datetime.datetime.now()
                precio = cat._compute_buscar_precio(fecha)

                self.acp_linea_actualizacion.create(
                    (
                        {
                            "lia_categoria": cat.id,
                            "lia_precio_actual": precio,
                            "lia_precio_nuevo": precio,
                            "lia_actualizacion": self.id,
                        }
                    )
                )
        return result

    def validar(self):
        for record in self:
            for linea in record.acp_linea_actualizacion:
                self.env["asw.precio_categoria"].create(
                    {
                        "pca_categoria": linea.lia_categoria.id,
                        "pca_fecha": record.acp_fecha_desde,
                        "pca_precio": linea.lia_precio_nuevo,
                        "pca_act_precio": self.id,
                    }
                )

            # Buscar las categorias
            record.acp_estado = "validado"

    def cancelar(self):
        for record in self:
            self.acp_pca_ids.checkeo()
            self.acp_pca_ids.unlink()
            self.actualizar_precio_guardias()
            record.acp_estado = "borrador"
