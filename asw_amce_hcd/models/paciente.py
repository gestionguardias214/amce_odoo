# -*- encoding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_pac(models.Model):
    _name = 'asw.paciente'
    _description = "Paciente"
    _ord = 'pac_nombre'
    _rec_name = 'pac_nombre'
    
    pac_nombre = fields.Char(
        string = 'Nombre',
        default = ''
    )

    pac_apellido = fields.Char(
        string = 'Apellido',
        default = ''
    )

    pac_tel = fields.Char(
        string = u'Teléfono',
        default = ''
    ) 

    pac_dni = fields.Char(
        string = 'D.N.I.',
        default = ''
    )

    pac_nro_socio = fields.Char(
        string = u'N° Socio',
        default = ''
    )

    pac_cobertura = fields.Char(
        string = 'Cobertura',
        default = ''
    )

    pac_plan = fields.Char(
        string = 'Plan',
        default = ''
    )

    pac_edad = fields.Char(
        string = 'Edad',
        default = ''
    )

    pac_localidad = fields.Char(
        string = 'Localidad',
        default = ''
    )

    pac_calle = fields.Char(
        string = 'Calle',
        default = ''
    )

    pac_interseccion = fields.Char(
        string = 'Interseción',
        default = ''
    )

    pac_nro = fields.Char(
        string = 'Nro',
        default = ''
    )

    pac_piso = fields.Char(
        string = 'Piso',
        default = ''
    )

    pac_dto = fields.Char(
        string = 'dto',
        default = ''
    )

    pac_antecedentes = fields.Char(
        string='Antecedentes',
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = 'True'
    )

    def actualizar_antecedentes(self):
        hcd = self.env['asw.historia'].search([('historia_dni_pac_acompanante','=', self.pac_dni)],order='id desc', limit=1)        
        self.pac_antecedentes = hcd.historia_antecedentes_id
        

    def crear_desde_hcd(self, hcd):
        paciente = self.search([('pac_dni','=', hcd.hpa_dni)])
        vals = {
            'pac_cobertura': hcd.hpa_cobertura,
            'pac_plan': hcd.hpa_plan,
            'pac_nro_socio': hcd.hpa_nro_socio,
            'pac_dni': hcd.hpa_dni,
            'pac_nombre' : hcd.hpa_nombre,
            'pac_edad': hcd.hpa_edad,
            'pac_apellido': hcd.hpa_apellido,
            'pac_localidad': hcd.hpa_localidad,
            'pac_calle': hcd.hpa_calle,
            'pac_interseccion': hcd.hpa_interseccion,
            'pac_nro': hcd.hpa_nro,
            'pac_piso': hcd.hpa_piso,
            'pac_dto': hcd.hpa_dto,
            'pac_antecedentes': hcd.historia_dni_pac_acompanante
        }
        
        if(paciente.id == False):
            paciente = self.create(vals)
        else:
            paciente.write(vals)
        

    @api.model
    def create(self, values):
        if 'pac_dni' in values and values['pac_dni'] not in [False, '']:
            cnt = self.env['asw.paciente'].search_count([('pac_dni', '=', values['pac_dni'])])
            if cnt > 0:
                raise exceptions.Warning('''El dni provisto ya existe para otro paciente. Por favor revise
                nuevamente y vuelva a intentarlo.''')

        result = super(asw_pac, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'pac_dni' in values and values['pac_dni'] not in [False, '']:
            cnt = self.env['asw.paciente'].search_count([('pac_dni', '=', values['pac_dni']),('id', '!=', self.id)])
            if cnt > 0:
                raise exceptions.Warning('''El dni {} provisto ya existe para otro paciente. Por favor revise
                nuevamente y vuelva a intentarlo.'''.format(values['pac_dni']))

        result = super(asw_pac, self).write(values)

        return result