# -*- coding: utf-8 -*-
from odoo import models, fields, api


class asw_historia_imagenes_ecg(models.Model):
    _name = 'asw.historia_imagenes_ecg'
    _description = 'Imagenes de ECG'

    name = fields.Char(string='Nombre del archivo')
    file = fields.Binary(
        string='Imagen', 
        required=False
    )

    historia_id = fields.Many2one(string='Historia Clinica', comodel_name='asw.historia', ondelete='restrict')