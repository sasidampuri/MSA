from django import forms
from django.forms import widgets
from .models import Employee, Medicine, Vendor, Stock, Sales,Bill
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput

import datetime
from django.forms import modelformset_factory

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

CHOICES = (
    (1, 'True'),
    (0, 'False')
)

class CreateEmployee(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Only letters and numbers', 'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}), label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']

class EmployeeData(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'eg.Abhijeet', 'required':'true'}), label='First Name', required=True)
    middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'eg.Kamal', 'required':'false'}), label='Middle Name', required=False)
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'eg.Choudhary', 'required':'true'}), label='Last Name', required=True)
    date_of_birth = forms.DateField(label='DOB', required=True, widget=forms.DateInput(attrs={'class':'form-control', 'required':'true', 'placeholder':'yyyy-mm-dd'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'form', 'required':'true'}), label='Gender', required=True)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter mobile number', 'required':'true'}), label='Mobile Number', required=True)
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address here(200 characters)', 'required':'true'}), label='Address', required=True)
    is_admin = forms.BooleanField(label='Admin', required=False)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true', }),required=True,label='Password')
    confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true', }),required=True,label='Confirm Password')

    def clean(self):
        cleaned_data = super(EmployeeData, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password do not match"
            )
    
        mobile = cleaned_data.get('phone')
        mobile_str = str(mobile)
        if not len(mobile_str) is 10:
            raise forms.ValidationError(
                "Mobile number is not valid"
            )     

        dob = cleaned_data.get('date_of_birth')
        valid_dob = datetime.date.today() - datetime.timedelta(days=365*18)
        if dob > valid_dob:
            raise forms.ValidationError(
                "The date of birth is not valid"
            )
    class Meta:
        model = Employee
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'phone', 'address', 'is_admin', 'password', 'confirm_password']
       
        widget = {
            'date_of_birth':DatePickerInput
        }

class MedicineData(forms.ModelForm):
    trade_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Trade Name', 'required':'true'}), label='Trade Name', required=True)
    generic_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Generic Name', 'required':'true'}), label='Generic Name', required=True)
    unit_sell_price = forms.DecimalField(decimal_places=2, max_digits=7, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Unit MRP', 'required':'true'}), label='Unit Selling Price', required=True)
    unit_purchase_price = forms.DecimalField(decimal_places=2, max_digits=7, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Unit Cost Price', 'required':'true'}), label='Unit Purchase Price', required=True)

    class Meta:
        model = Medicine
        fields = ['trade_name', 'generic_name', 'unit_sell_price', 'unit_purchase_price']

class VendorData(forms.ModelForm):
    vendor_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vendor Name', 'required':'true'}), label='Vendor Name', required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}), label='Email')
    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter mobile number', 'required':'true'}), label='Mobile Number', required=True)
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address here(200 characters)', 'required':'true'}), label='Address', required=True)
    medicine_ids = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Semicolon(;) seperated medicine IDs', 'required':'true'}), label='Medicine IDs', required=True)

    def clean(self):
        cleaned_data = super(VendorData, self).clean()
        mobile = cleaned_data.get('mobile')
        mobile_str = str(mobile)
        if not len(mobile_str) is 10:
            raise forms.ValidationError(
                "Mobile number is not valid"
            )

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'email', 'mobile', 'address', 'medicine_ids']

class StockData(forms.ModelForm):
    vendor_id = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Vendor ID', 'required':'true'}), label='Vendor ID', required=True)
    medicine_id = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Medicine ID', 'required':'true'}), label='Medicine ID', required=True)
    batch_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Batch ID', 'required':'true'}), label='Batch ID', required=True)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'No. of units', 'required':'true'}), label='Quantity', required=True)
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'required':'true', 'placeholder':'yyyy-mm-dd'}), label='Expiry Date', required=True)

    class Meta:
        model = Stock
        fields = ['vendor_id','medicine_id', 'batch_id', 'quantity', 'expiry_date']

StockDataSet = modelformset_factory(
    Stock,
    fields = ['vendor_id','medicine_id', 'batch_id','quantity','expiry_date'],
    extra = 1,
    #widgets={
    #    'medicine-id':forms.TextInput(attrs={'class':"form-control m-input", 'placeholder':"medicine ID", 'autocomplete':"off"}),
    #    'quantity':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'No. of units', 'required':'true'})
    #},
    #labels={
    #    'medicine-id':'Medicine ID',
    #    'quantity':'Quantity',
    #},
    #required={
     #   'medicine-id':True,
      #  'quantity':True,
    #}
)

class RevenueProfit(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'required':'true'}), label='From:', required=True)
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'required':'true'}), label='To:', required=True)
class SalesData(forms.ModelForm):
    customer_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Customer Name', 'required':'true'}), label='Customer Name', required=True)
    customer_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter mobile number', 'required':'true'}), label='Customer Mobile Number', required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'required':'true', 'placeholder':'yyyy-mm-dd'}), label='Todays Date', required=True)
    #medicine_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'medicine ID', 'required':'true'}), label='Medicine ID', required=True)
    #quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'No. of units', 'required':'true'}), label='Quantity', required=True)

    class Meta:
        model = Bill
        fields = ['customer_name','customer_number','date']
       

SalesDataSet = modelformset_factory(
    Sales,
    fields = ['medicine_id', 'quantity'],
    extra = 1,
    #widgets={
    #    'medicine-id':forms.TextInput(attrs={'class':"form-control m-input", 'placeholder':"medicine ID", 'autocomplete':"off"}),
    #    'quantity':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'No. of units', 'required':'true'})
    #},
    #labels={
    #    'medicine-id':'Medicine ID',
    #    'quantity':'Quantity',
    #},
    #required={
     #   'medicine-id':True,
      #  'quantity':True,
    #}
)