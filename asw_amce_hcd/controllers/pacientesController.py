# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo.http import route, request, Controller
from odoo.exceptions import UserError, ValidationError


import logging
_logger = logging.getLogger(__name__)



class PacientesController(Controller):
    """ The summary line for a class docstring should fit on one line.

        Routes:
          /pacientes_sincronizar: Se utilizara esta url para ser llamada desde una tarea
          programada y separar dicho procesamiento del guardado de la HCD
    """

    @route('/web/pacientes/sincronizar', type='http', auth='public')
    def pacientes_sincronizar(self, **kw):
        historias_clinicas = request.env['asw.historia'].sudo().search([('historia_proceso_paciente','=',False),('hpa_dni', '!=', False)], 
             order='id')
        tot = len(historias_clinicas)
        cnt = 0
        
        for reg in historias_clinicas:
            request.env['asw.paciente'].sudo().crear_desde_hcd(reg)
            reg.historia_proceso_paciente = True
            cnt +=1
            self.print_texto_detalle(tot, cnt)

        return "OK"
    
    @route('/web/pacientes/sincronizar_antecedentes', type='http', auth='public')
    def pacientes_sincronizar_antecedentes(self, **kw):
        pacientes = request.env['asw.paciente'].sudo().search([])
        tot = len(pacientes)
        cnt = 0
        
        for pac in pacientes:
            pac.actualizar_antecedentes()
            cnt +=1
            self.print_texto_detalle(tot, cnt)

        return "OK"

    @route('/web/firmas/sincronizar', type='http', auth='public')
    def firmas_sincronizar(self, **kw):
        domain_firma_paciente = [('historia_archivo_firma_pac_acompanante', '!=', False),
                ('historia_firma_pac_acompanante','=', False)]
        historias_clinicas = request.env['asw.historia'].sudo().search(domain_firma_paciente, order='id')
        tot = len(historias_clinicas)
        cnt = 0
        
        for reg in historias_clinicas:
            reg.recuperar_desde_paciente_firebase()
            reg.recuperar_desde_medico_firebase()
            reg.recuperar_desde_med_derivante_firebase()
            cnt +=1
            self.print_texto_detalle(tot, cnt)


        return "OK"

    def print_texto_detalle(self, tot, cnt):
        _logger.info("Sincronizando Pacientes {} de {}".format(cnt,tot))
