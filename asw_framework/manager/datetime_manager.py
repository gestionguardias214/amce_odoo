# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



class asw_datetime_manager(models.AbstractModel):
    _name = 'asw.datetime.manager'

    def get_dias_semana(self):
        return ["Lunes","Martes","Miércoles","Jueves","Virnes","Sabado","Domingo"]

    def obtenerDifHoras(self, horaInicio, horaFinal):
        horaI = fields.Datetime.from_string(horaInicio)
        horaF = fields.Datetime.from_string(horaFinal)
        dif = horaF - horaI
        diferencia = dif.total_seconds() / 3600        
        return diferencia

    def diferencia_dias(self, desde, hasta):        
        ddesde = fields.Date.from_string(desde)
        dhasta = fields.Date.from_string(hasta)
        diferencia = (dhasta - ddesde).days      
        return diferencia
    
    def obtener_dia_semana(self, fecha):
        dtfecha = fields.Date.from_string(fecha)
        dias_semana = self.get_dias_semana()

        index_dia = dtfecha.weekday()

        return dias_semana[index_dia]


    def sumar_dias(self,dia_desde,cantidad):
        dia_hasta = fields.Date.from_string(dia_desde) + relativedelta(days=+cantidad)
        return dia_hasta

    def fecha_proximo_anio(self):
        dia_hasta = datetime.now() + relativedelta(years=1)
        return dia_hasta

        