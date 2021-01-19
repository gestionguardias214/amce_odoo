# -*- coding: utf-8 -*-
from openerp import models, fields, api

class asw_liquidacion_report(models.TransientModel):
    _name = 'asw.liquidacion.report'
    _description = 'Reporte de Liquidacion'
    
    rli_periodo = fields.Many2one(
        string=u'Periodo',
        comodel_name='asw.periodo',
        ondelete='set null',              
    )

    rli_tipo = fields.Selection(
        string=u'Tipo',
        selection=[('todas', 'Todas'), ('normal', 'Normal'), ('sac', 'SAC')],        
        default='todas',        
    )

    
    rli_liquidaciones = fields.Many2many(
        string=u'Liquidaciones',
        comodel_name='asw.liquidacion',
        relation='asw_liquidacion_report_list',
        column1='asw_liquidacion_id',
        column2='asw_liquidacion_report_id',
    )

    
    rli_conceptos = fields.Many2many(
        string=u'Conceptos',
        comodel_name='asw.concepto',
        relation='asw_concepto_liquidacion_report',
        column1='asw_concepto_id',
        column2='asw_liquidacion_report_id',
    )
    
    
    @api.multi
    def imprimir(self):
        domain = [('liq_periodo','=',self.rli_periodo.id)]

        if(self.rli_tipo != 'todas'):
            domain.append(('liq_tipo','=', self.rli_tipo))

        liquidaciones = self.env['asw.liquidacion'].search(domain)
        conceptos = liquidaciones.mapped('liq_lineas.lin_concepto')        

        self.write({
            'rli_liquidaciones' : [(6,0, liquidaciones.ids)],
            'rli_conceptos' : [(6,0, conceptos.ids)]
        })

        return self.env['report'].get_action(self, 'asw_amce.listadoliquidacion')

        

    
