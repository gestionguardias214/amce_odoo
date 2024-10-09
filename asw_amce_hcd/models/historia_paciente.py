# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_paciente(models.AbstractModel):
    _name = "asw.historia_paciente"

    hpa_cobertura = fields.Char(string="Cobertura")
    hpa_plan = fields.Char(string="Plan")
    hpa_nro_socio = fields.Char(string="Nro Socio")
    hpa_dni = fields.Char(string="DNI")
    hpa_nombre = fields.Char(string="Nombre")
    hpa_edad = fields.Char(string="Edad")
    hpa_apellido = fields.Char(string="Apellido")
    hpa_localidad = fields.Char(string="Localidad")
    hpa_calle = fields.Char(string="Calle")
    hpa_interseccion = fields.Char(string="Interseccion")
    hpa_nro = fields.Char(string="Nro")
    hpa_piso = fields.Char(string="Piso")
    hpa_dto = fields.Char(string="Dto")
