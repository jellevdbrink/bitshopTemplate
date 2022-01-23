from django import forms

from shopApp.models import Bestelling, Klant


class DatumInput(forms.DateTimeInput):
    input_type = 'date'


class BestellingForm(forms.ModelForm):
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


class KlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KlantForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w3-input w3-border w3-round'

    class Meta:
        model = Klant
        fields = ['naam', 'email', 'telnr']


class ProductPlusForm(forms.Form):
    aantal = forms.IntegerField(min_value=1)
    extra_optie = forms.IntegerField()
