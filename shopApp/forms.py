from django.forms import ModelForm, DateTimeInput

from shopApp.models import Bestelling, Klant


class DatumInput(DateTimeInput):
    input_type = 'date'


class BestellingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BestellingForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w3-input w3-border w3-round'

    class Meta:
        model = Bestelling
        fields = ['klant', 'dag_ophalen']
        widgets = {
            'dag_ophalen': DatumInput(),
        }


class KlantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KlantForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w3-input w3-border w3-round'

    class Meta:
        model = Klant
        fields = ['naam', 'email', 'telnr']

