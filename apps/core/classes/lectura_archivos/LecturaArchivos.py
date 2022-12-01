from django.core.files.uploadedfile import InMemoryUploadedFile

from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
import unicodedata
from typing import Optional, Tuple

def normalizar_texto(input_str: str) -> str:
    input_str = input_str.lower()
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    only_ascii = only_ascii.decode("utf-8")
    return only_ascii

class LecturaArchivos(metaclass=ABCMeta):

    def __init__(self, archivo, *args, **kwargs):
        self.errores = []
        self.ruta_archivo = archivo
        self.datos = pd.DataFrame()
        if not self.ruta_archivo:
            raise ArithmeticError("La ruta del archivo no es correcta")



    def _remplazar_na(self, nuevo_valor=''):
        self.datos.replace(np.nan, nuevo_valor, inplace=True)


    def _obtener_errores(self):
        return self.errores

    @abstractmethod
    def _leer_archivo(self):
        raise NotImplementedError

    @abstractmethod
    def _validar_datos(self):
        raise NotImplementedError

    abstractmethod
    def _obtener_datos_cargados(self):
        raise NotImplementedError


class LecturaExcelPandas(LecturaArchivos):

    def __init__(self, archivo, columnas_esperadas=[], prohibir_celdas_vacias=False, prohibir_columnas_vacias=False, *args, **kwargs):
        super().__init__(archivo, *args, **kwargs)

        self.columnas_esperadas = {normalizar_texto(item) for item in columnas_esperadas} #Convierto los elementos a minúscula y quito acentos
        self.prohibir_celdas_vacias = prohibir_celdas_vacias
        self.prohibir_columnas_vacias = prohibir_columnas_vacias

        self._leer_archivo(self.ruta_archivo)
        self._validar_datos()

    def _leer_archivo(self, archivo) -> 'pd.DataFrame':
        """
            Retorna un dataframe usando un archivo de excel como parámetro

            Parámetros:

            Retorno:
                None
        """

        self.datos = pd.read_excel(archivo, engine='openpyxl')
        if self.prohibir_columnas_vacias:
           self.datos.dropna(how='all', axis='columns', inplace=True) # Eliminar columnas na
        self.datos.dropna(how='all', axis='index', inplace=True) # Eliminar filas na
        self._remplazar_na()


    def _validar_datos(self):
        if not self.columnas_esperadas:
            return True, "El archivo no presenta errores"
        else:
            total_datos = self.datos.shape[0]

            if total_datos == 0:  # no hay registros de estudiantes
                self.errores.append({'vacio':'No hay registros en el archivo'})

            if self.datos.shape[1] != len(self.columnas_esperadas):
                self.errores.append({'datos':f'La cantidad de columnas no son las definidas, se esperan {len(self.columnas_esperadas)} columnas'})

            df_auxiliar = self.datos.replace(r'^\s*$', np.nan, regex=True)
            if self.prohibir_celdas_vacias and df_auxiliar.isnull().any().any():  # hay al menos 1 celda vacia
                self.errores.append({'celdas':'No deben haber celdas vacías'})

            self.datos.columns = list(map(normalizar_texto, self.datos.columns))

            columnas_en_df = set(self.datos.columns)

            if len(self.columnas_esperadas & columnas_en_df) != len(self.columnas_esperadas):
                self.errores.append({'datos':'Lo nombres de las columnas no coinciden'})

            if len(self.errores) != 0:
                return False, self.errores
            else:
                return True, "El archivo no presenta errores"

    def _obtener_datos_cargados(self) -> Tuple[bool, pd.DataFrame, list]:
        if len(self.errores) != 0:
            return False, None, self.errores
        return True, self.datos, self.errores


