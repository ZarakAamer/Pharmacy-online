from core.models import Product
from core.models import (Consultation, ProductReview, Insurance)
from django import forms
from stripe import Review
from django.utils.translation import gettext_lazy as _


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": _("Write review")})
    )

    class Meta:
        model = ProductReview
        fields = ["review", "rating"]


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ("subject", "content", "prescription", "bank_invoice")
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": _("Subject")}),
            "content": forms.Textarea(
                attrs={"placeholder": _("Attend your problem...")}
            ),
        }


class InsuranceForm(forms.ModelForm):
    CHOICES = (
        ("1", "الشركة التعاونية للتأمين"),
    )
    company = forms.ChoiceField(choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs.update({'class': 'select_field'})

    class Meta:
        model = Insurance
        fields = ("subject", "company", "prescription", "insurance_card")
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": _("Subject")}),
        }


# from bootstrap_datepicker_plus import DatePickerInput


class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Product Title", "class": "form-control"}))
    title_ar = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Product Title", "class": "form-control"}))
    title_fr = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Product Title", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))
    description_ar = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))
    description_fr = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))
    specifications = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))
    specifications_ar = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))
    specifications_fr = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Product Description", "class": "form-control"}))

    price = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': "Sale Price", "class": "form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': "Old Price", "class": "form-control"}))
    stock_count = forms.CharField(widget=forms.NumberInput(
        attrs={'placeholder': "How many are in stock?", "class": "form-control"}))
    expiry_date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'placeholder': "e.g: 2040-04-21 21:47:00", "class": "form-control"}))

    image = forms.ImageField(widget=forms.FileInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = Product
        fields = [
            'title',
            'title_ar',
            'title_fr',
            'image',
            'description',
            'description_ar',
            'description_fr',
            'price',
            'old_price',
            'specifications',
            'specifications_ar',
            'specifications_fr',
            'stock_count',
            'expiry_date',
            'category',
        ]

        widgets = {
            # 'mdf': DateTimePickerInput
        }
