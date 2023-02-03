# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger(__name__)

class asw_guardia(models.Model):
    _name = 'asw.guardia'
    _inherit = ['mail.thread', 'asw.calcula_cant_horas', 'asw.calcula.periodo']
    _description = 'Guardia'
    _order = 'gua_ingreso desc'
    _rec_name = 'id'
    
    gua_profesional = fields.Many2one(
        string=u'Profesional',
        comodel_name='asw.profesionales',
        ondelete='restrict',
        track_visibility='onchange',
    )
    
    gua_categoria = fields.Many2one(
        string=u'Categoria',
        comodel_name='asw.categoria',
        ondelete='restrict',
        track_visibility='onchange',
    )
    
    state = fields.Selection(
        string=u'Estado',
        selection=[('a', 'Abierta'), ('c', 'Cerrada'), ('liquidada','Liquidada')],
        default='a',
    )

    gua_ingreso = fields.Datetime(
        string=u'Fecha y hora de Ingreso',
        default=fields.Datetime.now,
    )

    gua_egreso = fields.Datetime(
        string=u'Fecha y hora de Egreso',
    )
    
    gua_precioxhora = fields.Float(
        string=u'Precio por Hora',
        compute='_compute_precioxhora'
    )

    gua_canthoras = fields.Float(
        string=u'Cantidad de horas',
        compute='_compute_canthoras',
        store=True
    )
    
    gua_importe = fields.Float(
        string=u'Importe',
        track_visibility='onchange',
    )

    gua_proyecto = fields.Many2one(
        string=u'Nombre del Proyecto',
        comodel_name='asw.proyectos',
        ondelete='set null',
        related='gua_tuf.tuf_proyectos',
        store=True
    )

    gua_importe_conceptos = fields.Float(string='Importe Conceptos', compute='calcular_importe_conceptos',store=True)
    
    gua_importe_total = fields.Float(string='Importe Total', compute='calcular_importe_total', store=True)
    
    
    gua_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='restrict',
    )
    
    gua_observaciones = fields.Text(
        string=u'Observaciones',
    )
    
    gua_fecha_liquidacion = fields.Date(
        string=u'Fecha de liquidacion',
        default=fields.Date.context_today,
    )        
    
    gua_liquidacion = fields.Many2one(
        string=u'Liquidación',
        comodel_name='asw.liquidacion',
        ondelete='restrict',
        domain="[('liq_profesional', '=', self.id)]"
    )
    
    gua_tuf = fields.Many2one(
        string=u'Turno fabrica',
        comodel_name='asw.turno_fabrica',
        ondelete='restrict',        
    )    

    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name',
        store=True,
    )
    
    gua_usu_fin = fields.Many2one(
        string=u'Usuario de Fin',
        comodel_name='res.users',
        ondelete='restrict',
    )
    
    gua_liquidacion = fields.Many2one(
        string=u'Liquidación',
        comodel_name='asw.liquidacion',
        ondelete='set null',
    )
    
    gua_grupo = fields.Many2one(
        string=u'Grupo',
        comodel_name='asw.grupo',
        ondelete='restrict',
        related='gua_categoria.cat_grupo',
        store= True
    )    

    gua_profesional_concepto = fields.One2many(
        string=u'Profesional concepto',
        comodel_name='asw.profesional_concepto',
        inverse_name='prc_guardia',
    )
    
    gua_editable = fields.Boolean(
        string=u'Editable',        
        compute='_compute_gua_editable',
        default=True
    )

    gua_fabrica = fields.Many2one(
        string=u"Fabrica",
        comodel_name="asw.fabrica",
        ondelete='set null',
        store=  True,        
        compute='_compute_gua_fabrica'
    )
    
    gua_refuerzo = fields.Boolean(
        string='Es refuerzo?',
    )

        
    @api.depends('gua_categoria')
    def _compute_gua_fabrica(self):
        _logger.info("Informando guardias: {}".format(len(self)))
        tot = len(self)
        cnt = 1
        for record in self:
            fabrica = record.gua_categoria.cat_fabrica
            if(record.gua_tuf.id != False):
                fabrica = record.gua_tuf.tuf_fabrica
            
            record.gua_fabrica = fabrica.id
            cnt = cnt + 1
            _logger.info("Informando {} de {}".format(cnt, tot))
    
    def actualizar_precio(self):
        for record in self:
            record._compute_precioxhora()
            record._compute_canthoras()      
            record._compute_importe()  
    
    @api.depends('gua_profesional_concepto')
    def calcular_importe_conceptos(self):
        for record in self:
            record.gua_importe_conceptos = sum(record.gua_profesional_concepto.mapped('prc_importe'))
    
    @api.depends('gua_importe','gua_importe_conceptos')
    def calcular_importe_total(self):
        for record in self:
            record.gua_importe_total = record.gua_importe + record.gua_importe_conceptos

    @api.depends('gua_periodo')
    def _compute_gua_editable(self):
        for record in self:            
            if(record.gua_periodo.id == False):
                record.gua_editable = True
            else:                    
                record.gua_editable = not (record.gua_periodo.per_cerrado == True and record.gua_grupo.id in record.gua_periodo.per_gru_ids.ids )
   
    @api.multi
    def write(self, vals):
        # Agregar codigo de validacion aca
        if(len(self) == 1):
            if('gua_egreso' in vals):
                vals['state'] = 'c'
            
            liquidacion_actual = self.env['asw.liquidacion'].search([('liq_profesional', '=', self.gua_profesional.id), ('liq_periodo','=', self.gua_periodo.id)])

            if(len(liquidacion_actual) == 1 and self.gua_liquidacion.id == False):
                vals['gua_liquidacion'] = liquidacion_actual.id
                vals['state'] = 'liquidada'

        result = super(asw_guardia, self).write(vals)            
        return result

    @api.model
    def create(self, vals):
        # Agregar codigo de validacion aca
        if('gua_egreso' in vals):
            vals['state'] = 'c'

        result = super(asw_guardia, self).create(vals)       
        
        if('gua_periodo' in vals):
            liquidacion_actual = self.env['asw.liquidacion'].search([('liq_profesional', '=', vals['gua_profesional']), ('liq_periodo','=', vals['gua_periodo'])])

            if(len(liquidacion_actual) == 1):
                result.write({'gua_liquidacion': liquidacion_actual.id, 'state' : 'liquidada' })
            
        return result    

    @api.depends('gua_profesional', 'gua_categoria', 'gua_ingreso')
    def _compute_name(self):
        for record in self:
            record.name= 'Hola mundo' #record.gua_profesional.name+' - '+record.gua_categoria.name+' - '+record.gua_ingreso
               
    @api.onchange('gua_ingreso', 'gua_egreso')
    def _compute_canthoras(self):
        datetimeFormat = '%Y-%m-%d %H:%M:%S' 
        for record in self:
            if(record.gua_egreso != False):                                
                record.gua_canthoras = record.calcular_horas(record.gua_egreso, record.gua_ingreso)                                           
                record.gua_periodo = record.obtenerPeriodo(record.gua_egreso, record.gua_profesional.pro_grupo)
    
    @api.onchange('gua_canthoras', 'gua_precioxhora')
    def _compute_importe(self):
        for record in self:
            record.gua_importe = record.gua_canthoras * record.gua_precioxhora

    def poner_periodo(self):
        self.gua_periodo = self.obtenerPeriodo(self.gua_egreso, self.gua_profesional.pro_grupo)

    @api.depends('gua_categoria', 'gua_ingreso')
    def _compute_precioxhora(self):
        for record in self:
            record.gua_precioxhora = record.gua_categoria._compute_buscar_precio(record.gua_ingreso)

    def checkeo(self):
        for record in self:
            if record.gua_periodo.get_esta_cerrado(record.gua_grupo) == True and record.state == 'l':
                raise ValidationError("No se puede eliminar esta guardia ya que el periodo asociado a ella esta cerrado, y su estado es liquidada.")

            elif record.gua_periodo.get_esta_cerrado(record.gua_grupo) == True:
                raise ValidationError("No se puede eliminar esta guardia ya que el periodo asociado a ella esta cerrado.")

            elif record.state == 'l':
                raise ValidationError("No se puede eliminar esta guardia ya que su estado es liquidada.")

            else:
                return True

    @api.multi
    def unlink(self):
        for record in self:
            record.checkeo()
            super(asw_guardia,record).unlink()