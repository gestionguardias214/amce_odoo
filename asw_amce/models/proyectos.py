# -*- coding: utf-8 -*-
from openerp import models, fields, api

class proyectos(models.Model):
    _name = 'asw.proyectos'
    _inherit = ['mail.thread'] # No se que hace (cambiar)
    _description = 'Proyectos'
    order = 'proyecto_fabrica'
    _rec_name = 'proyecto_fabrica'
    # _sql_constraints = [
    # ('fab_codigo', 'UNIQUE(fab_codigo)', 'Ya se ha ingresado una fabrica con este codigo, por favor elija un codigo diferente'),   
    # ] # No se que hace (cambiar)

    proyecto_fabrica = fields.Char(
        string=u'Proyecto',
    )