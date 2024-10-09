# -*- coding: utf-8 -*-
from openerp import api, fields, models
from odoo import exceptions


class asw_historia(models.Model):
    _name = "asw.historia"
    _description = "Historia Clínica"
    _ord = "hpa_nombre"
    _rec_name = "hpa_nombre"
    _inherit = ["asw.historia_paciente", "asw.firestore"]
    _order = "historia_fecha desc"

    active = fields.Boolean(string="Activo", default=True)

    historia_fecha = fields.Datetime(string="Fecha")

    historia_medico = fields.Char(string="Medico")

    historia_chofer = fields.Char(string="Chofer")

    historia_enfermero = fields.Char(string="Enfermero")

    historia_movil_id = fields.Char(string="Movil")

    historia_ubicacion_atencion = fields.Char(
        string="Ubicacion de la atencion",
    )

    historia_motivo_llamada_color = fields.Char(string="Color")

    historia_motivo_llamada_motivo = fields.Char(string="Motivo de Llamada")

    historia_tiempo_dia = fields.Integer(string="Dias")

    historia_tiempo_hora = fields.Integer(string="Horas")

    historia_tiempo_minuto = fields.Integer(string="Minutos")

    historia_antecedentes_id = fields.Char(string="Antecedentes")

    # TODO: Signos Vitales Pendientes
    # TODO: Score Glasgow Pendiente

    historia_piel_mucosa = fields.Char(string="Piel y Mucosa")

    historia_neuro = fields.Char(string="Examen Neurológico")

    historia_ap_respiratorio = fields.Char(string="AP Respiratorio")

    historia_cyc = fields.Char(string="Cabeza y Cuello")

    historia_cardio = fields.Char(string="Ap. Cardiovascular")

    historia_ecg_desc = fields.Char(string="Informe ECG Descripción")

    historia_sist_oseoart_muscular = fields.Char(string="Sist. Oseoart. y Muscular")

    historia_abdomen = fields.Char(string="Abdomen")

    historia_urogen = fields.Char(string="Urogenital")

    historia_gco = fields.Char(string="Ginecobstétrico")

    historia_psiquiatrico = fields.Char(string="Psiquiatrico")

    historia_mec_id = fields.Char(string="Mecanismo")

    historia_diagnos = fields.Char(string="Diagnóstico presuntivo")

    historia_proc = fields.Char(string="Procedimientos")

    historia_epicrisis = fields.Char(string="Epicrisis")

    historia_medicamentos = fields.Char(string="Medicamentos")

    historia_evol_id = fields.Char(string="Evolución")

    historia_des_id = fields.Char(string="Desenlace")

    historia_al_llegar_id = fields.Char(string="Al llegar había")

    historia_abona_copago = fields.Boolean(string="Abona Copago")

    historia_nombre_med_derivante = fields.Char(string="Medico Derivante")

    historia_mat_med_derivante = fields.Char(string="Matricula del medico Derivante")

    historia_hosp = fields.Char(string="Derivacion")

    historia_signos_vitales_ids = fields.Many2many(
        string="Historia SIgnos Vitales",
        comodel_name="asw.historia_signos_vitales",
        relation="asw_historia_signos_vitales_asw_historia_rel",
        column1="asw_historia_signos_vitales_id",
        column2="asw_historia_id",
    )

    historia_score_glasgow_ids = fields.Many2many(
        string="Historia SCore Glasgow",
        comodel_name="asw.historia_score_glasgow",
        relation="asw_historia_score_glasgow_asw_historia_rel",
        column1="asw_historia_score_glas_id",
        column2="asw_historia_id",
    )

    historia_trauma_detalle_ids = fields.Many2many(
        string="Historia TRauma Detalle",
        comodel_name="asw.historia_trauma_detalle",
        relation="asw_historia_trauma_detalle_asw_historia_rel",
        column1="asw_historia_trauma_detalle_id",
        column2="asw_historia_id",
    )

    historia_firma_pac_acompanante = fields.Binary(
        string="Firma del Paciente / Acompañante",
    )

    historia_firma_med_derivante = fields.Binary(
        string="Firma del Medico Derivante",
    )

    firma = fields.Binary(
        string="Firma del Medico",
    )

    motivo_cancelacion = fields.Char(
        string="Motivo de Cancelación",
    )

    historia_aclaracion_pac_acompanante = fields.Char(
        string="Aclaración",
    )

    historia_dni_pac_acompanante = fields.Char(
        string="DNI Acompañante",
    )

    id_firebase = fields.Char(
        string="id_firebase",
    )

    archivo_firma = fields.Char(
        string="Firma del Medico Firestore",
    )

    historia_archivo_firma_med_derivante = fields.Char(
        string="Firma del Medico Der. Firestore",
    )

    historia_archivo_firma_pac_acompanante = fields.Char(
        string="Archivo de Firma del Paciente",
    )

    historia_matricula_medico = fields.Char(
        string="Historia Matricula Medico", compute="_compute_historia_matricula_medico"
    )

    historia_proceso_paciente = fields.Boolean(
        string="Historia Proceso Paciente", default=False
    )

    imagenes_ecg_ids = fields.One2many(
        string="Imagenes ECG",
        comodel_name="asw.historia_imagenes_ecg",
        inverse_name="historia_id",
    )

    key = fields.Char(
        string="key",
    )

    id_interno = fields.Char(
        string="Id Interno de Tablet",
    )

    version_app = fields.Char(
        string="Version de la App que Informa",
    )

    @api.depends("historia_medico")
    def _compute_historia_matricula_medico(self):
        for record in self:
            usuario = self.env["asw.usuario_app"].search(
                [("app_nombre", "ilike", record.historia_medico)], limit=1
            )
            record.historia_matricula_medico = usuario.app_matricula

    @api.model
    def create(self, vals):
        ids_signos_vitales = []
        ids_score_glasgow = []
        ids_trauma_detalle = []

        if "medicionesSignosVitales" in vals:
            for msv in vals["medicionesSignosVitales"]:
                nsv = self.historia_signos_vitales_ids.create(msv)
                ids_signos_vitales.append(nsv.id)

            vals["historia_signos_vitales_ids"] = [(6, 0, ids_signos_vitales)]

        if "medicionesScoreGlasgow" in vals:
            for msg in vals["medicionesScoreGlasgow"]:
                nsg = self.historia_score_glasgow_ids.create(msg)
                ids_score_glasgow.append(nsg.id)

            vals["historia_score_glasgow_ids"] = [(6, 0, ids_score_glasgow)]

        if "historia_traumas" in vals:
            for ht in vals["historia_traumas"]:
                nhtd = self.historia_trauma_detalle_ids.create(
                    {"lugar": ht, "detalle": vals["historia_traumas"][ht]}
                )
                ids_trauma_detalle.append(nhtd.id)

            vals["historia_trauma_detalle_ids"] = [(6, 0, ids_trauma_detalle)]

        result = super(asw_historia, self).create(vals)

        if "imagenesEcg" in vals:
            for mecg in vals["imagenesEcg"]:
                mecg.update({"historia_id": result.id})
                nsv = self.imagenes_ecg_ids.create(mecg)

        return result

    # @api.multi
    # def obtener_datos_firebase(self):
    #     self.recuperar_desde_med_derivante_firebase()
    #     self.recuperar_desde_medico_firebase()
    #     self.recuperar_desde_paciente_firebase()

    # @api.multi
    # def recuperar_desde_paciente_firebase(self):
    #     if(self.historia_archivo_firma_pac_acompanante != False):
    #         archivo = self.historia_archivo_firma_pac_acompanante
    #         self.historia_firma_pac_acompanante = self.obtener_archivo(archivo)

    # @api.multi
    # def recuperar_desde_medico_firebase(self):
    #     if(self.archivo_firma != False):
    #         self.firma = self.obtener_archivo(self.archivo_firma)

    @api.multi
    def recuperar_desde_med_derivante_firebase(self):
        if self.historia_archivo_firma_med_derivante != False:
            self.historia_firma_med_derivante = self.obtener_archivo(
                self.historia_archivo_firma_med_derivante
            )
