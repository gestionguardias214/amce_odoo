# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_localidad(models.Model):
    _name = 'asw.localidad'
    _inherit = ['mail.thread']
    _description = 'Localidades'
    _sql_constraints = [
        ('codigo_unique', 'UNIQUE(codigo)', 'Ya se ha ingresado un Localidades con este codigo, por favor ingrese un codigo diferente'), 
    ]
    _rec_name= 'descripcion'
    
    descripcion = fields.Char(
        string=u'Nombre',
    )    
    
    loc_codigo_postal = fields.Integer(
        string=u'Código postal',
    )    
    
    loc_provincia = fields.Many2one(
        string=u'Provincia',
        comodel_name='asw.provincia',
        ondelete='set null',
    )

    @api.multi
    def unlink(self):
        for record in self:
            cnt = self.env['asw.zona'].search_count([('zon_loc_id','=',record.id)])

            if(cnt > 0):
                raise exceptions.ValidationError("No se puede eliminar una localidad con zonas relacionadas, por favor eliminelas y vuelva a intentarlo")
                
            super(asw_localidad, record).unlink()
    
    