from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML

PAYMENT_CHOICES = [
        ('C', 'Credit Card'), 
        ('D', 'Debit Card'), 
        ('P', 'PayPal')
        ]

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    zipcode = forms.CharField()
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            Fieldset(
                'Continue the checkout process, {{ username }}',
                'street_address',
                'apartment_address',
                'zipcode',
                'same_shipping_address',
                'save_info',
                'payment_option',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )