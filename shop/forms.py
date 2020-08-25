from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML

PAYMENT_CHOICES = [
        ('S', 'Stripe'), 
        ('P', 'PayPal')
        ]

class CheckoutForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    #country = forms.MultipleChoiceField()
    #state = forms.MultipleChoiceField()
    city = forms.CharField()
    zipcode = forms.CharField()
    phone = forms.IntegerField(required=False)
    email = forms.CharField(required=False)
    #same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    #save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            Fieldset(
                'Shipping address information',
                'first_name',
                'last_name',
                'street_address',
                'apartment_address',
                #'country',
                #'state',
                'city',
                'zipcode',
                'phone',
                'email',
                #'same_billing_address',
                #'save_info',
                'payment_option',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    order_number = forms.CharField(required = False)
    message = forms.CharField()