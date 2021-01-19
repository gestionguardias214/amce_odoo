# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError

class asw_grupo(models.Model):
    _name = 'asw.grupo'
    _inherit = ['mail.thread']
    _description = 'Grupos'
    _sql_constraints = [
    ('gru_codigo', 'UNIQUE(gru_codigo)', 'Ya se ha ingresado un grupo con ese codigo, por favor elija otro'),   
    ]

    gru_codigo = fields.Char(
        string=u'Codigo',
        track_visibility='onchange',
    )
    
    gru_nombre = fields.Char(
        string=u'Nombre',
        track_visibility='onchange',
    )
    
    gru_profesional = fields.One2many(
        string=u'Profesionales',
        comodel_name='asw.profesionales',
        inverse_name='pro_grupo',
    )

    gru_categoria = fields.One2many(
        string=u'Categorias',
        comodel_name='asw.categoria',
        inverse_name='cat_grupo',
    )

    gru_acp = fields.Many2many(
        string=u'Grupo',
        comodel_name='asw.actualizacion_precio',
        relation='asw_grupo_precio',
        column1='actualizacion_precio_id',
        column2='grupo_id',
    )
    
    gru_profesional = fields.One2many(
        string=u'Profesionales',
        comodel_name='asw.profesionales',
        inverse_name='pro_grupo',
    )    
    
    gru_dia_inicio = fields.Integer(
        string=u'Día de Inicio de periodo',        
        track_visibility='onchange',        
    )
    
    gru_dia_inicio_especial = fields.Boolean(
        string=u'Inicia la guardia un día distinto al Primero',
    )    
    
    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name',
        store=True,
    )

    @api.onchange('gru_dia_inicio_especial')
    def onchange_gru_dia_inicio_especial(self):
        self.gru_dia_inicio = 0
    
    @api.depends('gru_codigo', 'gru_nombre')
    def _compute_name(self):
        for record in self:
            record.name=record.gru_codigo+' - '+record.gru_nombre
       
    @api.multi
    def unlink(self):
        for record in self:
            if len(record.gru_profesional) > 0 and len(record.gru_categoria) > 0:
                raise ValidationError("No se puede eliminar este grupo ya que posee uno o mas profesionales y categorias asociados a el. Elimine estas relaciones para borrar el grupo.")

            elif len(record.gru_profesional) > 0:
                raise ValidationError("No se puede eliminar este grupo ya que posee uno o mas profesionales asociados a el. Elimine estas relaciones para borrar el grupo.")

            elif len(record.gru_categoria) > 0:
                raise ValidationError("No se puede eliminar este grupo ya que posee una o mas categorias asociadas a el. Elimine estas relaciones para borrar el grupo.")

            else:            
                super(asw_grupo,record).unlink()
    
    @api.model
    def default_get(self, vals):
        result = super(asw_grupo, self).default_get(vals)        
        result['gru_codigo'] = self.search([], order="id desc", limit=1).id + 1     
        return result