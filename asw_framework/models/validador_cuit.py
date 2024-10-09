# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import re


class asw_validador_cuit(models.Model):
    _name = "asw.validador_cuit"

    def es_cuit_valido(self, codigo_afip, nro_doc):
        if codigo_afip == "80" and nro_doc is not False and nro_doc.isdigit():
            cuit = nro_doc
            cuit = re.sub("\D", "", cuit)

            if len(cuit) != 11:
                return False
            base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

            cuit = cuit.replace("-", "")  # remuevo las barras

            # calculo el digito verificador:
            aux = 0
            for i in xrange(10):
                aux += int(cuit[i]) * base[i]
            aux = 11 - (aux - (int(aux / 11) * 11))
            if aux == 11:
                aux = 0
            if aux == 10:
                aux = 9
            if aux != int(cuit[10]):
                return False

        return True
