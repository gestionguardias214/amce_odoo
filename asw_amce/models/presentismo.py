# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.exceptions import ValidationError

class asw_presentismo(models.Model):
    _name = 'asw.presentismo'
    _inherit = ['mail.thread']
    _description = 'Presentismo'
    _rec_name = 'id'
    _order = 'id desc'

    
    pre_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='restrict',
    )
    
    pre_grupo = fields.Many2many(
        string=u'Grupo',
        comodel_name='asw.grupo',
        relation='asw_grupo_presentismo',
        column1='grupo_id',
        column2='presentismo_id',
    )    
    
    pre_linea_presentismo = fields.One2many(
        string=u'Lineas de presentismo',
        comodel_name='asw.linea_presentismo',
        inverse_name='lpr_presentismo',
    )
    
    pre_estado = fields.Selection(
        string=u'Estado',
        selection=[('borrador', 'Borrador'), ('validado', 'Validado')],
        default = 'borrador',
    )

    @api.multi
    def agregar(self):        
        result = {'value': {'pre_linea_presentismo': []}} 

        self.pre_linea_presentismo.unlink()

        if(len(self.pre_grupo) == 0):
            raise ValidationError("Debe seleccionar al menos un grupo para buscar profesionales")

        guardias  = self.env['asw.guardia'].search([('gua_periodo','=',self.pre_periodo.id), ('gua_categoria.cat_grupo', 'in', self.pre_grupo.ids),('gua_categoria.cat_presentismo','>', 0)])
        profesionales = guardias.mapped('gua_profesional')

        for prof in profesionales:
            self.pre_linea_presentismo.create(({
                'lpr_profesional' : prof.id,
                'lpr_presentismo' : self.id              
            }))
            
        return result

    def validar_duplicado(self):
        proceso_periodo = self.search([('id', '!=', self.id),('pre_periodo', '=', self.pre_periodo.id)])

        if(len(proceso_periodo) > 0):
            for record in proceso_periodo:                
                for grup in record.pre_grupo:
                    if(grup.id in self.pre_grupo.ids):
                        raise ValidationError("No puede validarse este proceso ya que existe otro proceso para el mismo periodo y grupo, el proceso es el nro %s" % (record.id))
        return True
    
    def validar(self):
        #self.validar_duplicado()

        if(len(self.pre_linea_presentismo) == 0):
            raise ValidationError("No puede procesarse un proceso de presentismo sin profesionales seleccionados, por favor agregue primero los profesionales")
            
        guardias = self.env['asw.guardia']
        concepto = self.env['asw.configuracion'].browse(1).con_concepto

        for profesional in self.pre_linea_presentismo:
            prof = profesional.lpr_profesional
            guardias_filt = guardias.search([
                ('gua_periodo','=',self.pre_periodo.id), 
                ('gua_categoria.cat_presentismo','!=',0),
                ('gua_profesional','=',prof.id)
            ])

            cats = guardias_filt.mapped('gua_categoria')
            for cat in cats:
                gua = guardias_filt.filtered(lambda r: r.gua_categoria.id == cat.id)
                imp_total = gua.mapped('gua_importe')
                suma = round(sum(imp_total), 2)
                pres = suma * cat.cat_presentismo/100

                parametros = (cat.name, cat.cat_presentismo, suma)
                
                self.env['asw.profesional_concepto'].create({
                    'prc_profesional': prof.id,
                    'prc_descripcion': "Presentismo de la categoria %s usando el porcentaje %s por el importe total de guardias %s$" % parametros,
                    'prc_importe': pres,
                    'prc_periodo': self.pre_periodo.id,
                    'prc_concepto': concepto.id,
                    'prc_tipo' : 'presentismo',
                    'prc_guardias' : [(6,0, gua.ids)],
                    'prc_categoria' : cat.id,
                    'prc_porcentaje' : cat.cat_presentismo,
                    'prc_linea_presentismo' : profesional.id})

        self.pre_estado = 'validado'

    def checkeo(self):
        for record in self:            
            if record.pre_periodo.get_esta_cerrado(record.pre_grupo):
                raise ValidationError("No puede cancelarse un Presentismo de un periodo que se encuentra cerrado. Por favor abra el periodo y vuelva a intentarlo")

            # conceptos = record.pre_linea_presentismo.mapped('lpr_profesional_concepto')
            # conceptos.unlink() 

            for linea in record.pre_linea_presentismo:
                for prc in linea.lpr_profesional_concepto:
                    if prc.prc_periodo.get_esta_cerrado(record.pre_grupo):
                        raise ValidationError("No se puede cancelar este presentismo ya que posee conceptos de periodos ya cerrados")
                    prc.unlink()        

    def cancelar(self):       
        self.checkeo()        
        self.pre_estado = 'borrador'

    @api.multi
    def unlink(self):
        result = True
        for record in self:
            if(self.pre_estado == 'validado'):
                raise ValidationError("No puede eliminarse un Presentismo que se encuentre Validado")
                
            record.checkeo()            
            result = super(asw_presentismo, record).unlink()
        
        return result