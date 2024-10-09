# -*- coding: utf-8 -*-
from openerp import models, fields, api
import unicodedata


class asw_formateador_manager(models.AbstractModel):
    _name = "asw.formateador.manager"

    def formatear_campo(self, valores, campo):
        if campo in valores:
            nvalor = valores[campo] or ""
            nvalor = self.chau_acentos(nvalor)
            valores[campo] = nvalor.upper()

    def chau_acentos(self, s):
        return "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )
