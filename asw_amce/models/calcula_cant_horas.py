# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import timedelta, date, datetime


class asw_calcula_cant_horas(models.AbstractModel):
    _name = "asw.calcula_cant_horas"

    def calcular_horas(self, fecha_fin, fecha_inicio):
        result = 0
        if fecha_fin != False and fecha_inicio != False:
            datetimeFormat = "%Y-%m-%d %H:%M:%S"

            inicio = datetime.strptime(fecha_inicio, datetimeFormat)
            fin = datetime.strptime(fecha_fin, datetimeFormat)

            timedelta = fin - inicio
            result = round(float(timedelta.total_seconds() / 3600), 2)

        return result
