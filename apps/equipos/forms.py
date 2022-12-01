from django import forms

from apps.core.forms import ModelSelect2WidgetConfigurable, ModelSelect2MultipleWidgetConfigurable

from apps.equipos.models import Equipo, TipoEquipo, CampoExtra, InformacionAdicionalEquipo, CampoExtraTipoEquipo
from apps.laboratorios.models import Laboratorio


class FormEquipo(forms.ModelForm):

    laboratorio = ModelSelect2WidgetConfigurable(
        model = Laboratorio,
        queryset = Laboratorio.obtener_activos(),
        search_fields = ['nombre__icontains'],
        label='Laboratorio',
        required=False
    )

    tipo_equipo = ModelSelect2WidgetConfigurable(
        model = TipoEquipo,
        queryset = TipoEquipo.obtener_activos(),
        search_fields = ['nombre__icontains'],
        label='Tipo equipo'
    )

    class Meta:
        model = Equipo
        fields = ('tipo_equipo', 'laboratorio', 'serial', 'activa')


class FormTipoEquipo(forms.ModelForm):

    campos_extra = ModelSelect2MultipleWidgetConfigurable(
        model = CampoExtra,
        queryset = CampoExtra.obtener_activos(),
        search_fields = ['nombre__icontains'],
        label='Campos extra',
        required = False
    )

    class Meta:
        model = TipoEquipo
        fields = ('nombre', 'campos_extra', 'activa')


class FormCampoExtra(forms.ModelForm):

    class Meta:
        model = CampoExtra
        fields = ('nombre', 'activa')


class FormInformacionAdicionalEquipo(forms.ModelForm):

    campo_extra_tipo = ModelSelect2WidgetConfigurable(
        model = CampoExtraTipoEquipo,
        queryset = CampoExtraTipoEquipo.obtener_activos(),
        search_fields = ['campo_extra__nombre__icontains'],
        label='Campo extra del tipo',
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        equipo = self.initial['equipo']
        self.fields['campo_extra_tipo'].queryset = CampoExtraTipoEquipo.obtener_por_tipo_equipo(equipo.tipo_equipo.pk)
        self.fields['campo_extra_tipo'].widget.queryset = CampoExtraTipoEquipo.obtener_por_tipo_equipo(equipo.tipo_equipo.pk)

    class Meta:
        model = InformacionAdicionalEquipo
        fields = ('campo_extra_tipo', 'valor', 'equipo', 'activa')
        widgets = {
            'equipo': forms.HiddenInput(attrs={'readonly': 'readonly'})
        }