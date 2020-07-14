from django import forms


class Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        required_fields = kwargs.pop('required_fields', [])

        super(Form, self).__init__(*args, **kwargs)

        if required_fields:
            for field, value in self.fields.items():
                value.required = field in required_fields


class RealmSessionForm(Form):
    def __init__(self, *args, **kwargs):
        super(RealmSessionForm, self).__init__(*args, **kwargs, required_fields=['realm'])


class CustomerForm(Form):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs, required_fields=['realm', 'name'])


class InvoiceLineForm(Form):
    def __init__(self, *args, **kwargs):
        super(InvoiceLineForm, self).__init__(*args, **kwargs, required_fields=['realm', 'invoice', 'type', 'rate'])


class InvoiceForm(Form):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs, required_fields=['realm', 'customer', 'due_date'])


class ItemServiceForm(Form):
    def __init__(self, *args, **kwargs):
        super(ItemServiceForm, self).__init__(*args, **kwargs, required_fields=['realm', 'name', 'account'])


class BillAddressForm(Form):
    def __init__(self, *args, **kwargs):
        super(BillAddressForm, self).__init__(*args, **kwargs, required_fields=['customer'])


class ShipAddressForm(Form):
    def __init__(self, *args, **kwargs):
        super(ShipAddressForm, self).__init__(*args, **kwargs, required_fields=['customer'])
