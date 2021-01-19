# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from datetime import timedelta, date
from odoo.exceptions import ValidationError

class asw_calculo_sac(models.Model):
    _name = 'asw.calculo_sac'
    _inherit = ['mail.thread']
    _description = 'Calculo SAC'
    _rec_name= "id"
    
    sac_semestre = fields.Selection(
        string=u'Semetre',
        selection=[('primero', 'Primero'), ('segundo', 'Segundo')],
    )

    sac_grupo = fields.Many2many(
        string=u'Grupo',
        comodel_name='asw.grupo',
        relation='asw_grupo_sac',
        column1='asw_grupo_id',
        column2='asw_calculo_sac_id',
    )

    # sac_profesional = fields.Many2one(
    #     string=u'Profesional',
    #     comodel_name='asw.profesionales',
    #     ondelete='restrict',
    #     track_visibility='onchange',
    # )
    
    sac_liquidaciones = fields.One2many(
        string=u'Liquidaciones',
        comodel_name='asw.liquidacion',
        inverse_name='liq_sac',
    )
    
    sac_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='restrict',
    )    
    
    sac_estado = fields.Selection(
        string=u'Estado',
        selection=[('borrador', 'Borrador'), ('validado', 'Validado')],
        default = 'borrador',       
        track_visibility='onchange',        
    )
    
    sac_periodo_ids = fields.Many2many(
        string='Sac Periodo',
        comodel_name='asw.periodo',
        relation='asw_periodo_calculo_sac_rel',
        column1='asw_periodo_id',
        column2='asw_calculo_sac_id',
    )
    

    def cancelar(self):
        for record in self:
            if record.get_esta_cerrado(record.sac_grupo) != False:
                raise ValidationError("No se puede cancelar el calculo de SAC, ya que las liquidaciones generadas pertenecen a un periodo cerrado.")
            else:
                record.sac_liquidaciones.unlink()
                record.sac_estado = 'borrador'

    @api.onchange('sac_semestre')
    def calcular_periodo(self):
        for record in self:
            filtro = ''
            if record.sac_semestre == 'primero':
                filtro = '06-01'
            if record.sac_semestre == 'segundo':
                filtro = '12-01'                
            
            periodo = self.env['asw.periodo'].search([('per_desde','like',filtro),('per_cerrado', '=', False)],order='id desc', limit=1)
            self.sac_periodo = periodo        

    def elim_sac(self, profesional):
        for record in self:
            self.env['asw.liquidacion'].search([
                ('liq_semestre', '=', record.sac_semestre), 
                ('liq_tipo','=','sac'), 
                ('liq_profesional', '=', profesional.id)
                ]).unlink()

    def buscar_lineas(self, profesional):
        for record in self:
            lineas = self.env['asw.linea_liquidacion'].search([
                ('lin_concepto.con_sac', '=', True),
                ('lin_liquidacion.liq_profesional', '=', profesional.id)
            ])           

            return lineas

    def crear_liquidacion(self, periodo, concepto, total, profesional):        
        liquidacion = self.env['asw.liquidacion'].create({
            'liq_profesional': profesional.id,
            'liq_periodo': periodo.id,
            'liq_fecha': datetime.datetime.now(),
            'liq_lineas': [(0,0, {
                'lin_concepto': concepto,
                'lin_importe': round(total, 2),
                'lin_descripcion' : 'SAC'
            })],
            'liq_tipo': 'sac',
            'liq_semestre': self.sac_semestre,
            'liq_sac': self.id,                
        })
        liquidacion.liq_semestre = self.sac_semestre

        return liquidacion

    def calcular_dias_semestre(self):        
        hoy = date.today()        

        finicio = date(hoy.year, 1, 1)
        ffin = date(hoy.year, 6, 30)
        
        if self.sac_semestre == 'segundo':
            finicio = date(hoy.year, 7, 1)
            ffin = date(hoy.year, 12, 31)

        dif = ffin - finicio

        return dif.days

    def calcular_dias_trabajados(self, profesional):
        hoy = date.today()
        ffin = date(hoy.year, 6, 30)
        finicio = date(hoy.year, 1, 1)

        if self.sac_semestre == 'segundo':
            finicio = date
            
            (hoy.year, 7, 1)
            ffin = date(hoy.year, 12, 31)

        if(profesional.pro_fecha_ultimo_sac == False):            
            finicio = fields.Date.from_string(profesional.pro_fecha_alta)
            if(finicio == False):
                raise ValidationError("El profesional %s no tiene definida fecha de ultimo SAC ni Fechad e ALTA".format(profesional.pro_nombre))

        if(profesional.pro_fecha_baja != False):
            ffin = fields.Date.from_string(profesional.pro_fecha_baja)

        dif = ffin - finicio
        return dif.days
    
    def calcular_fecha_calculo_sac(self):
        hoy = date.today()        
        fecha = date(hoy.year,6, 30)
        
        if self.sac_semestre == 'segundo':
            fecha = date(hoy.year, 12, 31)

        return fecha
            

    def validar(self):
        for record in self:
            concepto = self.env['asw.configuracion'].browse(1).con_concepto_sac.id   

            liquidaciones = self.env['asw.liquidacion'].search([('liq_periodo', 'in', self.sac_periodo_ids.ids),('liq_profesional.pro_grupo','in', record.sac_grupo.ids)])            
            profesionales = liquidaciones.mapped('liq_profesional')
            liquidaciones.calcular_monto_sac()

            dias_semestre = self.calcular_dias_semestre()
            fecha_calculo_sac = self.calcular_fecha_calculo_sac()
            for prof in profesionales:
                if prof.id != False:
                    liquidaciones_profesional = liquidaciones.filtered(lambda r: r.liq_profesional.id == prof.id)
                    
                    cnt_periodos = len(liquidaciones_profesional)

                    total_bruto = sum(liquidaciones_profesional.mapped('liq_monto_aplicable_sac'))
                    total_bruto /= (cnt_periodos * 2)
                    dias_trabajados = record.calcular_dias_trabajados(prof)

                    total = (total_bruto / dias_semestre) * dias_trabajados

                    liq = record.crear_liquidacion(self.sac_periodo, concepto, total, prof)
                    
                    prof.write({ 'pro_fecha_ultimo_sac' : fecha_calculo_sac })
                    liquidaciones_profesional.write({ 'liq_liquidaciones_sac' : liq.id })

            record.sac_estado='validado'

    @api.multi
    def unlink(self):
        for record in self:
            if record.get_esta_cerrado(record.sac_grupo):
                raise ValidationError("No se puede eliminar el calculo de SAC, ya que las liquidaciones generadas pertenecen a un periodo cerrado.")
            else:
                return super(asw_calculo_sac, record).unlink()