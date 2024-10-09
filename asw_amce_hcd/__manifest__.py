# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2015  TM_FULLNAME
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses
#
###############################################################################
{
    "name": "asw_amce_hcd",
    "summary": "asw_amce_hcd Module Project",
    "version": "0.20.06.12",
    "description": """
asw_amce_hcd Module Project.
==============================================


    """,
    "author": "ANAC SOFT",
    "maintainer": "ANAC SOFT",
    "contributors": ["ANAC SOFT <ANAC SOFT@gmail.com>"],
    "website": "http://anacsoft.com",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "depends": ["base", "asw_framework", "asw_amce"],
    "external_dependencies": {
        "python": [],
    },
    "data": [
        "reportes/template_reporte_hcd.xml",
        "reportes/reporte_hcd.xml",
        "view/view_usuario_app.xml",
        "view/cobertura.xml",
        "view/plan_view.xml",
        "view/movil_view.xml",
        "view/mla_view.xml",
        "view/pac_view.xml",
        "view/mco_view.xml",
        "view/antecedente_view.xml",
        "view/piel_mucosa_view.xml",
        "view/signos_view.xml",
        "view/score_view.xml",
        "view/neuro_view.xml",
        "view/edema.xml",
        "view/ap_respiratorio_view.xml",
        "view/cyc_view.xml",
        "view/abdomen_view.xml",
        "view/cardio_view.xml",
        "view/cardio_soplo.xml",
        "view/cardio_pulso.xml",
        "view/gco_view.xml",
        "view/urogen_view.xml",
        "view/psi_view.xml",
        "view/trauma_view.xml",
        "view/trauma_lugar_view.xml",
        "view/trauma_tipo_view.xml",
        "view/mec_view.xml",
        "view/diagnos_view.xml",
        "view/des_view.xml",
        "view/evol_view.xml",
        "view/al_llegar_view.xml",
        "view/clas_llam_view.xml",
        "view/hosp_view.xml",
        "view/medicacion_view.xml",
        "view/medicamentos_view.xml",
        "view/quem_view.xml",
        "view/historia_view.xml",
        "view/estado_mental.xml",
        "view/instituciones_view.xml",
        "view/historia_imagenes_ecg.xml",
        "view/menu.xml",
        "security/permisos.xml",
        "security/ir.model.access.csv",
        "datos/abdomen.xml",
        "datos/al_llegar.xml",
        "datos/antecedente.xml",
        "datos/cardio.xml",
        "datos/clas_llam.xml",
        "datos/cyc.xml",
        "datos/des.xml",
        "datos/edema.xml",
        "datos/evol.xml",
        "datos/gco.xml",
        "datos/mec.xml",
        "datos/piel_mucosa.xml",
        "datos/psi.xml",
        "datos/quem.xml",
        "datos/ap_respiratorio.xml",
        "datos/trauma_lugar.xml",
        "datos/trauma_tipo.xml",
        "datos/urogen.xml",
        "datos/neuro.xml",
        "datos/estado_mental.xml",
        "datos/cardio_soplo.xml",
        "datos/cardio_pulso.xml",
    ],
    "demo": [],
    "js": [],
    "css": [],
    "qweb": [],
    "images": [],
    "test": [],
    "installable": True,
    "application": True,
}
