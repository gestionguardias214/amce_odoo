# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError

class asw_categoria(models.Model):
    _name = 'asw.categoria'
    _inherit = ['mail.thread']
    _description = 'categorias'
    _sql_constraints = [
    ('codigo_unique', 'UNIQUE(cat_codigo)', 'Ya se ha ingresado una categoria con ese codigo, por favor elija otro'),   
    ]
    _rec_name = 'name'
    _order = 'name'
    
    cat_codigo = fields.Char(
        string=u'Código',
        track_visibility='onchange',
    )
    
    cat_nombre = fields.Char(
        string=u'Nombre',
        track_visibility='onchange',
    )

    cat_presentismo = fields.Float(
        string=u'% de Presentismo',
    )
     
    cat_grupo = fields.Many2one(
        string=u'Grupo',
        comodel_name='asw.grupo',
        ondelete='restrict',
        track_visibility='onchange',
        group_expand='_read_group_grupo'
    )    
    
    active = fields.Boolean(
        string=u'Activo',        
        default=True,        
    )    

    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name',
        store=True,
    )

    cat_profesional = fields.Many2many(
        string=u'Profesional',
        comodel_name='asw.profesionales',
        relation='asw_profesional_categoria',
        column1="asw_profesionales_id",
        column2="asw_categoria_id",
    )
    
    cat_precio_categoria = fields.One2many(
        string=u'Precio de categoria',
        comodel_name='asw.precio_categoria',
        inverse_name='pca_categoria',
    )

    
    cat_precio_importacion = fields.Float(
        string=u'cat_precio_importacion',
    )
    
    cat_guardia = fields.One2many(
        string=u'Guardias',
        comodel_name='asw.guardia',
        inverse_name='gua_categoria',
    )
    
    cat_es_fabrica = fields.Boolean(
        string=u'Se utiliza en Turnos de Fábrica?',
    )
    
    cat_fabrica = fields.Many2one(
        string=u"Fabrica",
        comodel_name="asw.fabrica"
    )   
    
    @api.depends('cat_codigo', 'cat_nombre')
    def _compute_name(self):
        for record in self:
            record.name=record.cat_codigo+' - '+record.cat_nombre
    
    @api.depends('cat_codigo', 'cat_nombre')
    def _compute_name(self):
        for record in self:
            record.name=record.cat_codigo+' - '+record.cat_nombre
    
    @api.model
    def _read_group_grupo(self,stages,domain,order):
        grupos = self.env['asw.grupo'].search([])
        return grupos

    def _compute_buscar_precio(self, fecha):
        for record in self:
            precio = self.env['asw.precio_categoria'].search([('pca_fecha','<=', fecha),('pca_categoria', '=', self.id)], order='pca_fecha desc', limit=1)
            return precio.pca_precio

    @api.multi
    def unlink(self):
        for record in self:
            if len(record.cat_profesional) > 0 and len(record.cat_guardia.search([ ('state', '=', 'a') ])) > 0:
                raise ValidationError("No se puede eliminar esta categoria ya que posee una o mas guardias y profesionales asociados a ella. Elimine estas relaciones para borrar la categoria.")

            elif len(record.cat_profesional) > 0:
                raise ValidationError("No se puede eliminar esta categoria ya que posee uno o mas profesionales asociados a ella. Elimine estas relaciones para borrar la categoria.")

            elif len(record.cat_guardia) > 0:
                raise ValidationError("No se puede eliminar esta categoria ya que posee una o mas guardias asociadas a ella. Elimine estas relaciones para borrar la categoria.")

            else:            
                super(asw_categoria,record).unlink()

    @api.multi
    def write(self, vals):
        # Agregar codigo de validacion aca
        
        result = super(asw_categoria, self).write(vals)

        if('cat_fabrica' in vals):
            self.cat_guardia._compute_gua_fabrica()

        return result

    @api.model
    def default_get(self, vals):
        result = super(asw_categoria, self).default_get(vals)        
        result['cat_codigo'] = self.search([], order="id desc", limit=1).id + 1     
        return result
   