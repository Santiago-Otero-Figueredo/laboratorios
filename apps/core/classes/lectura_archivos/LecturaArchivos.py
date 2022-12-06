from django.core.files.uploadedfile import InMemoryUploadedFile

from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
import unicodedata
from typing import Optional, Tuple, Dict, List, Union

from apps.core.utils import normalizar_nombres


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

    def __init__(self, archivo, columnas_esperadas=[],
        prohibir_celdas_vacias=False, prohibir_columnas_vacias=False,
        modelo=None, columnas_a_normalizar=[], columnas_ignorar=[], *args, **kwargs):

        super().__init__(archivo, *args, **kwargs)

        self.columnas_esperadas = set(map(normalizar_texto, columnas_esperadas)) # Convierto los elementos a minúscula y quito acentos
        self.prohibir_celdas_vacias = prohibir_celdas_vacias
        self.prohibir_columnas_vacias = prohibir_columnas_vacias
        self.modelo = modelo
        self.datos_normalizados = pd.DataFrame()
        self.columnas_a_normalizar = list(set(map(normalizar_texto, columnas_a_normalizar))) # Convierto los elementos a minúscula y quito acentos
        self.columnas_ignorar = list(set(map(normalizar_texto, columnas_ignorar))) # Convierto los elementos a minúscula y quito acentos

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
        self.datos.columns = list(map(normalizar_texto, self.datos.columns))
        if self.prohibir_columnas_vacias:
           self.datos.dropna(how='all', axis='columns', inplace=True) # Eliminar columnas na
        self.datos.dropna(how='all', axis='index', inplace=True) # Eliminar filas na

        if self.columnas_ignorar:
            self.datos.drop(self.columnas_ignorar, axis=1, inplace=True)


        self._remplazar_na()


    def _validar_datos(self) -> None:
        total_datos = self.datos.shape[0]
        columnas_en_df = set(self.datos.columns)

        if total_datos == 0:  # no hay registros de estudiantes
            self.errores.append({'vacio':'No hay registros en el archivo'})

        df_auxiliar = self.datos.replace(r'^\s*$', np.nan, regex=True)
        if self.prohibir_celdas_vacias and df_auxiliar.isnull().any().any():  # hay al menos 1 celda vacia
            self.errores.append({'celdas':'No deben haber celdas vacías'})

        if len(self.columnas_esperadas) > 0:

            if self.datos.shape[1] != len(self.columnas_esperadas):
                self.errores.append({'datos':f'La cantidad de columnas no son las definidas, se esperan {len(self.columnas_esperadas)} columnas'})

            if len(self.columnas_esperadas & columnas_en_df) != len(self.columnas_esperadas):
                self.errores.append({'datos':'Los nombres de las columnas no coinciden'})

        if self.modelo:
            datos_normalizados = self.datos.copy()
            if self.columnas_a_normalizar:
                if set(self.datos.columns).intersection(self.columnas_a_normalizar):
                    datos_normalizados = datos_normalizados[self.columnas_a_normalizar].applymap(lambda x:normalizar_nombres(x), na_action='ignore')
                else:
                    self.errores.append({'normalizacion':'Las columnas a normalizar no existen el el archivo'})

            validacion_modelo = self.modelo.validar_registro_masivo(datos_normalizados)
            resultado = validacion_modelo['resultado']
            errores_modelo = validacion_modelo['errores']
            datos = validacion_modelo['datos']

            if resultado:
                self.datos_normalizados = datos

            self.errores.extend(errores_modelo) # Añado los elementos para ser parte de la lista, no los agrego asi evito una lista vacía dentro de la lista errores


    def _obtener_datos_cargados(self) -> Dict[str, Union[bool, pd.DataFrame, List[str]]]:
        respuesta = {'resultado':True, 'datos':self.datos, 'errores':self.errores}
        if len(self.errores) != 0:
            respuesta.update({'resultado':False, 'datos':None})
        return respuesta


