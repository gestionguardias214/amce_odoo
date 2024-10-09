# -*- coding: utf-8 -*-
from openerp import models, fields, api


class res_company(models.Model):
    _inherit = "res.company"

    def recalcular_fabricas_guardias(self):
        guardias = self.env["asw.guardia"].search([])
        guardias._compute_precioxhora()
