# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import tools


class asw_reporte_guardias_fabricas(models.Model):
    _name = "asw_reporte_guardias_fabricas"
    _description = "Reporte de Guardias de Fábrica"
    _auto = False

    importe_normal = fields.Float(
        string="Imp. Normal",
    )

    importe_adicionales = fields.Float(
        string="Imp. Adicionales",
    )

    gua_importe_conceptos = fields.Float(
        string="Conceptos",
    )

    gua_importe_total = fields.Float(
        string="Total",
    )

    gua_cnt_horas = fields.Integer(
        string="Hs Normales",
    )

    gua_horas_adicionales = fields.Integer(
        string="Hs Adicionales",
    )

    gua_canthoras = fields.Integer(
        string="Hs Totales",
    )

    gua_profesional = fields.Many2one(
        string="Profesional",
        comodel_name="asw.profesionales",
        ondelete="restrict",
    )

    gua_categoria = fields.Many2one(
        string="Categoria",
        comodel_name="asw.categoria",
        ondelete="restrict",
    )

    gua_periodo = fields.Many2one(
        string="Periodo",
        comodel_name="asw.periodo",
        ondelete="restrict",
    )

    gua_fabrica = fields.Many2one(
        string="Fabrica",
        comodel_name="asw.fabrica",
        ondelete="restrict",
    )

    gua_proyecto = fields.Many2one(
        string="Nombre del Proyecto",
        comodel_name="asw.proyectos",
        ondelete="set null",
    )

    gua_grupo = fields.Many2one(
        string="Grupo",
        comodel_name="asw.grupo",
        ondelete="restrict",
    )

    gua_ingreso = fields.Datetime(
        string="Fecha de Ingreso",
    )

    def init(self):
        """Build database view which will be used as module origin"""
        self._sql_query = """
            select 
                id,
                gua_profesional,
                gua_categoria,
                gua_ingreso,
                gua_fabrica,
                gua_periodo,
                gua_grupo,
                case when gua_refuerzo then
                    0
                else
                    gua_canthoras
                end as gua_cnt_horas,
                case when gua_refuerzo then
                    gua_canthoras
                else
                    0
                end as gua_horas_adicionales,
                gua_canthoras,
                case when gua_refuerzo then
                    0
                else
                    gua_importe
                end as importe_normal,
                case when gua_refuerzo then
                    gua_importe
                else
                    0
                end as importe_adicionales,
                gua_importe_conceptos,
                gua_importe_total,
            gua_refuerzo,
            gua_proyecto
            from asw_guardia
        """

        tools.drop_view_if_exists(self._cr, self._name)
        self._cr.execute(
            "create or replace view {} as ({})".format(self._table, self._sql_query)
        )
