from django import forms

from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

class ModelSelect2WidgetConfigurable(forms.ModelChoiceField):

    def __init__(self, model, search_fields=[], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widget=ModelSelect2Widget(
            model=model,
            queryset=self.queryset,
            search_fields=search_fields,
            max_results=100,
            attrs={
                'data-minimum-input-length':0
            }
        )


class ModelSelect2MultipleWidgetConfigurable(forms.ModelMultipleChoiceField):

    def __init__(self, model, search_fields=[], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.widget=ModelSelect2MultipleWidget(
            model=model,
            search_fields=search_fields,
            max_results=100,
            attrs={
                'data-minimum-input-length':0
            }
        )


class FormRegistroMasivo(forms.Form):
    archivo = forms.FileField()