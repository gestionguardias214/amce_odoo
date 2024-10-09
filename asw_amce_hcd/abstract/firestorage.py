# -*- coding: utf-8 -*-
from odoo import models, fields, api

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage

# import base64

# path_credenciales = "/opt/credenciales/AMCE HCD-f6740cec6eb6.json"
# path_storage = "amce-hcd.appspot.com"

# cred = credentials.Certificate(path_credenciales)
# app = firebase_admin.initialize_app(cred, {
#     'storageBucket': path_storage,
# })


class asw_firestore(models.AbstractModel):
    _name = "asw.firestore"

    # def obtener_archivo(self, archivo):
    #     path_guardado = self.descargar_archivo(archivo)
    #     return self.leer_archivo(path_guardado)

    # def leer_archivo(self, path):
    #     file = open(path, "rb")
    #     out = file.read()
    #     file.close()
    #     file_64 = base64.b64encode(out)

    #     return file_64

    # def descargar_archivo(self, nombre):
    #     bucket = storage.bucket(app=app)
    #     blob = bucket.blob("firmas/" + nombre + '.jpeg')
    #     path_guardado = '/tmp/' + nombre
    #     "/tmp/591c6983-dd34-59bf-bac0-b4b978342142"
    #     blob.download_to_filename(path_guardado)

    #     return path_guardado
