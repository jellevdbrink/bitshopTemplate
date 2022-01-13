from django.forms import ModelForm, DateTimeInput

from shopApp.models import Bestelling


class DatumInput(DateTimeInput):
    input_type = 'date'


class BestellingForm(ModelForm):
    class Meta:
        model = Bestelling
        fields = ['klant', 'dag_ophalen']
        widgets = {
            'dag_ophalen': DatumInput(),
        }
