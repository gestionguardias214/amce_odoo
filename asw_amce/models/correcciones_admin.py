# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_correcciones_admin(models.Model):
    _name = "asw.correcciones.admin"
    _description = "Correccion"

    periodo_id = fields.Many2one(
        string="periodo_id",
        comodel_name="asw.periodo",
        ondelete="set null",
    )

    @api.multi
    def asignar_grupo(self):
        profesionales = self.env["asw.profesionales"].search(
            [("pro_grupo", "=", False)]
        )
        for record in profesionales:
            if len(record.pro_categoria) > 0:
                grupo = record.pro_categoria[0].cat_grupo
                record.pro_grupo = grupo

    @api.multi
    def recuardar_profesionales(self):
        profesionales = self.env["asw.profesionales"].search(
            [("partner_id", "=", False)]
        )

        for record in profesionales:
            try:
                partner = self.env["res.partner"].create(
                    {
                        "name": record.pro_nombre,
                        "email": record.pro_email or "",
                        "phone": record.pro_telefono or "",
                    }
                )
                record.partner_id = partner
            except:
                pass

    @api.multi
    def asignar_periodo(self):
        guardias = self.env["asw.guardia"].search([("gua_egreso", "!=", False)])
        for record in guardias:
            record.poner_periodo()

    @api.multi
    def actualizar_precio_guardias_fabrica(self):
        guardias = self.env["asw.guardia"].search(
            [("gua_tuf", "!=", False), ("gua_periodo", "=", self.periodo_id.id)]
        )
        for record in guardias:
            record.actualizar_precio()
