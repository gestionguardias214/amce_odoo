# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_paciente(models.AbstractModel):
    _name = 'asw.historia_paciente'

    hpa_cobertura = fields.Char(string=u'Cobertura' )
    hpa_plan = fields.Char(string=u'Plan' )
    hpa_nro_socio = fields.Char(string=u'Nro Socio' )
    hpa_dni = fields.Char(string=u'DNI' )
    hpa_nombre = fields.Char(string=u'Nombre' )
    hpa_edad = fields.Char(string=u'Edad' )
    hpa_apellido = fields.Char(string=u'Apellido' )
    hpa_localidad = fields.Char(string=u'Localidad' )
    hpa_calle = fields.Char(string=u'Calle' )
    hpa_interseccion = fields.Char(string=u'Interseccion' )
    hpa_nro = fields.Char(string=u'Nro' )
    hpa_piso = fields.Char(string=u'Piso' )
    hpa_dto = fields.Char(string=u'Dto' )
    