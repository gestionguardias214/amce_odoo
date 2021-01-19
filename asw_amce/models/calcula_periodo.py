# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

class asw_calcula_periodo(models.AbstractModel):
    _name = 'asw.calcula.periodo'

    def obtenerPeriodo(self, fecha, grupo):
        suma = 0
        datetimeFormat = '%Y-%m-%d' 
        hoy = date.today()
       
        
        fecha_aux = fields.Datetime.from_string(fecha)
        fecha_fin = fields.Datetime.context_timestamp(self, timestamp=fecha_aux)

        if(self.env.user.has_group('asw_amce.module_category_asw_amce_administrador') == False):
            if(fecha_fin.date() > hoy):
                raise exceptions.ValidationError("No pueden cargarse registros con fecha mayor a la actual")

        mes_fin = fecha_fin        
        if(grupo.gru_dia_inicio > 0):
            if(grupo.gru_dia_inicio < fecha_fin.day):
                mes_fin += relativedelta(months=1)            
            if(grupo.gru_dia_inicio == fecha_fin.day and fecha_fin.hour >= 9):
                mes_fin += relativedelta(months=1)
        else:
            if(1 == fecha_fin.day and fecha_fin.hour < 9):
                mes_fin -= relativedelta(months=1)

        fecha_filtro = datetime.datetime(mes_fin.year, mes_fin.month, 1, 0, 0, 0)
        filtro = fecha_filtro.strftime('%Y-%m-%d')        
        periodo = self.env['asw.periodo'].search([('per_desde','=', filtro)], limit=1)  

        if(periodo.id == False):
            raise exceptions.ValidationError("No existe periodo generado para %s, por favor contacte al administrador para que genere el nuevo periodo" % (filtro))

        return periodo    