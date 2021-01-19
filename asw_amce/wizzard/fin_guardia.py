# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
import datetime 
from datetime import timedelta, date


class asw_fin_guardia(models.TransientModel):
    _name = 'asw.fin_guardia'
    _inherit = ['asw.calcula.periodo', 'asw.calcula_cant_horas']


    fin_profesional = fields.Many2one(
        string=u'Profesional',
        comodel_name='asw.profesionales',
        ondelete='restrict',
    )    
    
    fin_fechahora = fields.Datetime(
        string=u'Fecha y hora finalizacion',
        default=fields.Datetime.now,
    )
    
    
    fin_profesional_concepto = fields.Many2many(
         string=u'Profesional concepto',
        comodel_name='asw.profesional_concepto',
        relation='asw_fin_guardia_profesional_concepto',
        column1='asw_profesional_concepto_id',
        column2='asw_fin_guardia_id',
    )

    fin_guardia = fields.Many2one(
        string=u'Guardia a Finalizar',
        comodel_name='asw.guardia',
        ondelete='restrict',
    )   

    fin_fechahora_inicio = fields.Datetime(
        string=u'Fecha y hora Inicio',
    )
    
    fin_categoria = fields.Many2one(
        string=u'Categoria',
        comodel_name='asw.categoria',
        ondelete='restrict',        
        related='fin_guardia.gua_categoria',        
    )
    
    fin_observaciones = fields.Text(
        string=u'Observaciones',
    )

    fin_cantidad_horas = fields.Float(
        string=u'Cantidad de Hs',        
        readonly=True,        
    )
    
    fin_precio = fields.Float(
        string=u'Precio por Hora',        
        related='fin_guardia.gua_precioxhora',        
    )
    
    fin_importe = fields.Float(
        string=u'Importe',              
    )

    msg_error = fields.Char(string='Mensaje Error', default='')        

    @api.onchange('fin_fechahora')
    def compute_cant_horas(self):    
        if(self.fin_fechahora != False and self.fin_fechahora_inicio != False):                            
            self.fin_cantidad_horas = self.calcular_horas(self.fin_fechahora, self.fin_fechahora_inicio)            
            self.fin_importe = self.fin_cantidad_horas * self.fin_precio
            
            msg = ''
            if (self.fin_cantidad_horas < 0):
                msg = '''Revise la fecha y hora de finalización ya que la CANTIDAD de hora dio un numero NEGATIVO, CAMBIE LA FECHA DE FINALIZACION y vuelva a intentarlo.  \nHasta que no corrija esto, NO SE PODRA FINALIZAR LA GUARDIA '''
            
            self.msg_error = msg.upper()

    @api.onchange('fin_profesional')
    def _compute_obs(self):        
        if(self.fin_profesional.id != False):
            guardia = self.env['asw.guardia'].search([('state','=', 'a'),('gua_profesional', '=', self.fin_profesional.id)]) 
            self.fin_observaciones = guardia.gua_observaciones            
            self.fin_fechahora_inicio = guardia.gua_ingreso
            self.fin_guardia = guardia
            self.compute_cant_horas()

    # @api.onchange('fin_profesional')
    # def concepto(self):
    #     if len(self.fin_profesional) > 0:
    #         guardias_abiertas = self.env['asw.guardia'].search([('state','=', 'a')])
    #         guardia = guardias_abiertas.filtered(lambda r: r.gua_profesional == self.fin_profesional)

    #         self.fin_profesional_concepto = guardia.gua_profesional_concepto
            

    def actualizar_fin(self):
        # if(self.fin_cantidad_horas == 0):
        #     raise exceptions.ValidationError("No puede finalizar una guardia con la cantidad de horas igual a cero, por favor revise la fecha de finalización y vuelva a intentarlo")
        periodo = self.obtenerPeriodo(self.fin_fechahora, self.fin_profesional.pro_grupo)
        
        if(periodo.id == False):
            raise exceptions.ValidationError("No existe un periodo configurado para guardar la guardia, por favor revise los periodos cargados.")
        
        self.fin_guardia.write({
            'state' : 'c',
            'gua_egreso' : self.fin_fechahora,
            'gua_observaciones' : self.fin_observaciones,
            'gua_canthoras' : self.fin_cantidad_horas,
            'gua_usu_fin' : self.env.uid,
            'gua_periodo' : periodo.id
        })
        self.fin_guardia._compute_canthoras()
        self.fin_guardia.gua_importe = self.fin_importe
        
        #self.fin_guardia.gua_profesional_concepto = self.fin_profesional_concepto 


        
    
