# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from datetime import timedelta, date
from odoo.exceptions import ValidationError
class asw_proceso_liquidacion(models.Model):
    _name = 'asw.proceso_liquidacion'
    _inherit = ['mail.thread', 'asw.calcula.periodo']
    _description = 'Proceso de liquidacion'
    _rec_name = 'id'
    _order = 'id desc'

    prl_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='restrict',
    )
    
    prl_grupo = fields.Many2many(
        string=u'Grupo',
        comodel_name='asw.grupo',
        relation='asw_grupo_liquidacion',
        column1='grupo_id',
        column2='proceso_liquidacion_id',
    )    
    
    prl_fecha_desde = fields.Date(
        string=u'Fecha Desde',
    )
    
    prl_fecha_hasta = fields.Date(
        string=u'Fecha Hasta',
    )
    
    prl_tipo = fields.Selection(
        string=u'Tipo',
        selection=[('masivo', 'Masivo'), ('especifico', 'Específico')],
        default="masivo"
    )
    
    prl_pro_especifico = fields.Many2one(
        string=u'Profesional',
        comodel_name='asw.profesionales',
        ondelete='restrict',
    )      
    
    prl_profesional = fields.Many2many(
        string=u'Profesionales',
        comodel_name='asw.profesionales',
        relation='asw_profesional_liquidacion',
        column1='profesionales_id',
        column2='proceso_liquidacion_id',
    )
    
    prl_liq_ids = fields.One2many(
        string=u'Liquidaciones',
        comodel_name='asw.liquidacion',
        inverse_name='liq_proc_id',
    )    

    state = fields.Selection(
        string=u'Estado',
        selection=[('borrador', 'Borrador'), ('validado', 'Validado')],
        default = 'borrador',
    )

    def cargar(self):        
        guardias = self.env['asw.guardia'].search([('gua_profesional.pro_grupo','in', self.prl_grupo.ids), ('gua_periodo','=', self.prl_periodo.id)])
        #prof = self.env['asw.profesionales'].search([ ('pro_grupo', '=', self.prl_grupo.id) ])     
        prof = guardias.mapped('gua_profesional')

        self.write({
            'prl_profesional': [(6, 0, prof.ids)]
        })

    def validar(self):    
        if(self.prl_tipo == 'masivo'):
            if(len(self.prl_profesional) == 0):
                raise ValidationError("Deben cargarse al menos un profesional para poder validar")

            guardias = self.env['asw.guardia'].search([
                ('gua_periodo', '=', self.prl_periodo.id),
                ('gua_profesional', 'in', self.prl_profesional.ids)
            ])
            
            for prof in self.prl_profesional:
                guardias_prof = guardias.filtered(lambda r: r.gua_profesional == prof)                
                
                conceptos = self.env['asw.profesional_concepto'].search([('prc_profesional','=',prof.id), ('prc_periodo', '=', self.prl_periodo.id)])

                self.generar_liquidacion(guardias_prof, prof, self.prl_periodo, conceptos)
                
        else:
            guardias = self.env['asw.guardia'].search([
                ('gua_ingreso', '>=', self.prl_fecha_desde),
                ('gua_ingreso', '<=', self.prl_fecha_hasta),
                ('gua_profesional', '=', self.prl_pro_especifico.id),
                ('gua_liquidacion', '=', False)
            ])

            if(len(guardias) == 0):
                raise ValidationError("El profesional seleccionado no tiene guardias cargadas pendientes de liquidar para el rango de fechas")

            periodo = self.obtenerPeriodo(date.today().strftime('%Y-%m-%d')  ,self.prl_pro_especifico.pro_grupo)

            conceptos = self.env['asw.profesional_concepto'].search(
                [('prc_profesional','=', self.prl_pro_especifico.id), 
                ('prc_periodo.per_desde', '>=', self.prl_fecha_desde),
                ('prc_periodo.per_desde', '<=', self.prl_fecha_hasta)])
            
            self.generar_liquidacion(guardias, self.prl_pro_especifico, periodo, conceptos)
        
        self.state = 'validado'
    
    def generar_liquidacion(self, guardias, profesinal, periodo, conceptos ):
        liq = self.env['asw.liquidacion'].create({
            'liq_profesional': profesinal.id,
            'liq_periodo': periodo.id,
            'liq_fecha': date.today(),
            'liq_tipo': 'normal',
            'liq_proc_id' : self.id
        })
        liq._compute_semestre()

        guardias.write({
            'gua_liquidacion': liq.id,
            'state' : 'liquidada'
        })

        lineas = []

        for con in conceptos:
            linea = self.env['asw.linea_liquidacion'].create({
                'lin_concepto': con.prc_concepto.id,
                'lin_importe': con.prc_importe,
                'lin_liquidacion': liq.id,
                'lin_descripcion' : con.prc_descripcion
            })
            con.prc_liquidacion = liq.id
            lineas.append(linea.id)
        
        liq.write({
            'liq_lineas': [(6, 0, lineas)],
            'liq_guardia': [(6, 0, guardias.ids)]
        })


    def cancelar(self):
        if self.prl_periodo.get_esta_cerrado(self.prl_grupo):
            raise ValidationError("No se puede cancelar la liquidacion ya que pertenece a un periodo cerrado")
        else:            
            guardias = self.prl_liq_ids.mapped('liq_guardia')  
            guardias.write({'state' : 'c'})
            
            self.prl_liq_ids.unlink()
            self.state="borrador"

    @api.multi
    def unlink(self):
        if self.prl_periodo.get_esta_cerrado(self.prl_grupo):
            raise ValidationError("No se puede cancelar la liquidacion ya que pertenece a un periodo cerrado")
        else:  
            return super(asw_proceso_liquidacion, record).unlink()