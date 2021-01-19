# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from odoo.exceptions import ValidationError

class asw_profesional_concepto(models.Model):
    _name = 'asw.profesional_concepto'
    _inherit = ['mail.thread']
    _description = 'Profesional conceptos'
    _order = 'id desc'
    _rec_name= 'id'

    
    prc_profesional = fields.Many2one(
        string=u'Profesional',
        comodel_name='asw.profesionales',
        ondelete='restrict',
    )
    
    prc_concepto = fields.Many2one(
        string=u'Concepto',
        comodel_name='asw.concepto',
        ondelete='restrict',
    )       
    
    prc_descripcion = fields.Char(
        string=u'Descripción',
    )
    
    prc_importe = fields.Float(
        string=u'Importe',
    )
        
    prc_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='restrict',
    )
    
    prc_liquidacion = fields.Many2one(
        string=u'Liquidacion',
        comodel_name='asw.liquidacion',
        ondelete='set null',
    )        
    
    prc_porcentaje = fields.Float(
        string=u'Porcentaje',
    )
    
    prc_categoria = fields.Many2one(
        string=u'Categoría',
        comodel_name='asw.categoria',
        ondelete='restrict',
    )    
    
    prc_linea_presentismo = fields.Many2one(
        string=u'Presentismo',
        comodel_name='asw.linea_presentismo',
        ondelete='restrict',
    )

    prc_guardias = fields.Many2many(
        string=u'Guardias',
        comodel_name='asw.guardia',
        relation='asw_amce_profesionales_conceptos_guaridas',
        column1='asw_guardia_id',
        column2='conceptos_profesionales_id',
    )    
    
    prc_tipo = fields.Selection(
        string=u'Tipo',
        selection=[('otro', 'Otro'), ('presentismo', 'Presentismo')]
    )    
    
    prc_guardia = fields.Many2one(
        string=u'Guardias',
        comodel_name='asw.guardia',
        ondelete='restrict',
    )    
    
    prc_tuf = fields.Many2one(
        string=u'Turno fabrica',
        comodel_name='asw.turno_fabrica',
        ondelete='restrict',
    )
    
    prc_posee_liquidacion = fields.Boolean(
        string=u'Posee liquidacion',
        compute='_compute_posee_liquidacion'       
    )
    
    @api.depends('prc_liquidacion')
    def _compute_posee_liquidacion(self):
        for record in self:
            if len( record.prc_liquidacion ) > 0:
                record.prc_posee_liquidacion = True
            else:
                record.prc_posee_liquidacion = False
    
    @api.multi
    def unlink(self):
    # Agregar codigo de validacion aca
        for record in self:
            if record.prc_posee_liquidacion:
                raise ValidationError("No se puede eliminar este concepto ya que posee una liquidacion relacionada.")
            else:
                return super(asw_profesional_concepto, record).unlink()
    @api.model
    def create(self, vals):
        if self.env['asw.concepto'].search( [ ('id', '=', vals['prc_concepto'] ) ] ).con_negativo:
            vals['prc_importe'] = abs(vals['prc_importe']) * -1
        
        liquidacion_actual = self.env['asw.liquidacion'].search([('liq_profesional', '=', vals['prc_profesional'] ), ('liq_periodo','=', vals['prc_periodo'] )])

        if(len(liquidacion_actual) == 1):
            vals['prc_liquidacion'] = liquidacion_actual.id
            linea = self.env['asw.linea_liquidacion'].create({
                'lin_concepto': vals['prc_concepto'],
                'lin_importe': vals['prc_importe'],
                'lin_liquidacion': liquidacion_actual.id,
                'lin_descripcion' : vals['prc_descripcion']
            })

        return super(asw_profesional_concepto, self).create(vals)

    @api.multi
    def write(self, vals):
        # Agregar codigo de validacion aca
        
        if(len(self) == 1):
            liquidacion_actual = self.env['asw.liquidacion'].search([('liq_profesional', '=', self.prc_profesional.id ), ('liq_periodo','=', self.prc_periodo.id )])

            if(len(liquidacion_actual) == 1 and self.prc_liquidacion.id == False):
                vals['prc_liquidacion'] = liquidacion_actual.id
                linea = self.env['asw.linea_liquidacion'].create({
                    'lin_concepto': self.prc_concepto.id,
                    'lin_importe': self.prc_importe,
                    'lin_liquidacion': liquidacion_actual.id,
                    'lin_descripcion' : self.prc_descripcion
                })

        return super(asw_profesional_concepto, self).write(vals)

      
