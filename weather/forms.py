from django.forms import ModelForm

from weather.models import Weather


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class WeatherForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Weather
        fields = ('city', )
        labels = {
            'city': 'Город',
        }
