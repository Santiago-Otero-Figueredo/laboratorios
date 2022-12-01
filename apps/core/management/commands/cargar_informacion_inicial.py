from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from apps.usuarios.models import Usuario
from apps.matriculas.models import Matricula
from apps.periodos_academicos.models import PeriodoAcademico
from apps.programas.models import Programa

import names

import openpyxl
from django.conf import settings

UBICACION_ARCHIVOS ="/_datos_iniciales/produccion/"

class Command(BaseCommand):
    help = 'Guarda un archivo de backup.'

    def handle(self, *args, **kwargs):
        pass