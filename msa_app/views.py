from django.shortcuts import render, redirect
from .forms import CreateEmployee, EmployeeData, MedicineData, VendorData, StockData,StockDataSet,SalesData,SalesDataSet,RevenueProfit
from .models import Employee, ExpiredMedicines, Medicine, MedicineStock, Sales, Vendor, MedicineToVendor, Stock,Bill
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from django.shortcuts import get_object_or_404


from django.contrib.auth.decorators import login_required

import datetime



@login_required(login_url='/login/', redirect_field_name=None)
def HomePageafterlogin(request):
    return render(request, 'app/index.html')


def aboutus(request):
    return render(request, 'registration/aboutus.html')



def HomePage(request):
    return render(request, 'registration/index.html')



@login_required(login_url='/login/', redirect_field_name=None)
def CreateUser(request):
    # form_user = forms.CreateEmployee()
    # form_data = forms.EmployeeData()
    # context = {
    #     'form_data': form_data,
    #     'form_user': form_user
    # }
    # return render(request, 'registration/create-user.html', context)
    if request.method != 'POST':
        if request.session["is_admin"]:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            context = {
                'form_data': form_data,
                'form_user': form_user
            }
            return render(request, 'app/create-user.html', context)
        else:
            context = {
                'err': "Only admins can access this page"
            }
            return render(request, 'app/create-user.html', context)
    else:
        user_form = CreateEmployee(request.POST)
        employee_data_form = EmployeeData(request.POST)
        if user_form.is_valid() and employee_data_form.is_valid():
            # user = user_form.save()
            # employee_data = employee_data_form.save(commit=False)
            # user.set_password(employee_data.password)
            # user.save()
            # password = 0
            # employee_data.user = user
            # employee_data.save()
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            first_name = employee_data_form.cleaned_data['first_name']
            middle_name = employee_data_form.cleaned_data['middle_name']
            last_name = employee_data_form.cleaned_data['last_name']
            date_of_birth = employee_data_form.cleaned_data['date_of_birth']
            gender = employee_data_form.cleaned_data['gender']
            phone = employee_data_form.cleaned_data['phone']
            address = employee_data_form.cleaned_data['address']
            is_admin = employee_data_form.cleaned_data['is_admin']
            password = employee_data_form.cleaned_data['password']
            confirm_password = employee_data_form.cleaned_data['confirm_password']
            u = User(username=username, email=email)
            u.set_password(password)
            u.save()
            e = Employee(user=u, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth,
                        gender=gender, phone=phone, address=address, is_admin=is_admin, password=password, confirm_password=confirm_password)
            e.save()
            form_user = CreateEmployee()
            form_data = EmployeeData()
            context = {
            'form_data': form_data,
            'form_user': form_user
            }
            return render(request, 'app/create-user.html', context) 
        else:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            err1 = user_form.errors
            err2 = employee_data_form.errors
            context = {
                'form_data': form_data,
                'form_user': form_user,
                'err1': err1,
                'err2': err2
            }
            return render(request, 'app/create-user.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def CreateMedicine(request):
    if request.method != 'POST':
        form_med = MedicineData()
        context ={
            'form_med': form_med
        }
        return render(request, 'app/create-medicine.html', context)
    else:
        form_med = MedicineData(request.POST)
        if form_med.is_valid():
            trade_name = form_med.cleaned_data['trade_name']
            generic_name = form_med.cleaned_data['generic_name']
            unit_sell_price = form_med.cleaned_data['unit_sell_price']
            unit_purchase_price = form_med.cleaned_data['unit_purchase_price']

            try:
                t = Medicine.objects.get(generic_name=generic_name)
                form_med = MedicineData()
                context = {
                    'form_med':form_med,
                    'err':"Medicine " + generic_name+" already exists"
                }
                return render(request, 'app/create-medicine.html', context)
            except:
                m = Medicine(trade_name=trade_name,generic_name=generic_name,unit_sell_price=unit_sell_price,unit_purchase_price=unit_purchase_price)
                m.save()
                id = m.id
                med_id = "MED"+str(id)
                m.medicine_id = med_id
                m.save()

                ms = MedicineStock(medicine_id=med_id)
                ms.save()
                
                form_med = MedicineData()
                context ={
                'form_med': form_med,
                'med_id': med_id
                }
                return render(request, 'app/create-medicine.html', context)
        else:
            form_med = MedicineData()
            err = form_med.errors
            context ={
                'form_med': form_med,
                'err': err
            }
            return render(request, 'app/create-medicine.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def CreateVendor(request):
    if request.method != 'POST':
        form_ven = VendorData()
        context ={
            'form_ven': form_ven
        }
        return render(request, 'app/create-vendor.html', context)
    else:
        form_ven = VendorData(request.POST)
        if form_ven.is_valid():
            vendor_name = form_ven.cleaned_data['vendor_name']
            email = form_ven.cleaned_data['email']
            mobile = form_ven.cleaned_data['mobile']
            address = form_ven.cleaned_data['address']
            medicine_ids = form_ven.cleaned_data['medicine_ids']

            try:
                d = Vendor.objects.get(email=email)
                form_ven = VendorData()
                context = {
                    'form_ven':form_ven,
                    'err':"Vendor data already exists"
                }
                return render(request, 'app/create-vendor.html', context)
            except:
                meds = medicine_ids.split(";")
                for med in meds:
                    try:
                        Medicine.objects.get(medicine_id=med)
                    except:
                        form_ven = VendorData()
                        context={
                            'form_ven':form_ven,
                            'err': "Medicine_id "+med+" not found"
                        }
                        return render(request, 'app/create-vendor.html', context)

                v = Vendor(vendor_name=vendor_name,mobile=mobile,email=email,address=address, medicine_ids=medicine_ids)
                v.save()
                id = v.id
                ven_id = "VEN"+str(id)
                v.vendor_id = ven_id
                v.save()

                for m in meds:
                    k = MedicineToVendor(medicine_id=m, vendor_id=ven_id)
                    k.save()
                
                form_ven = VendorData()
                context ={
                'form_ven': form_ven,
                'ven_id': ven_id
                }
                return render(request, 'app/create-vendor.html', context)
        else:
            form_ven = VendorData()
            err = form_ven.errors
            context ={
                'form_ven': form_ven,
                'err': err
            }
            return render(request, 'app/create-vendor.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def AddStock(request):
    if request.method != 'POST':
        form_stock = StockData(None)
        formset = StockDataSet(queryset=Stock.objects.none())
        context ={
            'form_stock': form_stock,
            'formset': formset,
        }
        return render(request, 'app/add-stock.html', context)
    else:
        form_stock = StockData(request.POST)
        formset = StockDataSet(request.POST)
        #if form_stock.is_valid() and formset.is_valid():
        if formset.is_valid():
            #vendor_id = form_stock.cleaned_data['vendor_id']
            for formstock in formset:
                medicine_id = formstock.cleaned_data['medicine_id']
                batch_id = formstock.cleaned_data['batch_id']
                quantity = formstock.cleaned_data['quantity']
                expiry_date = formstock.cleaned_data['expiry_date']
                vendor_id = formstock.cleaned_data['vendor_id']

                try:
                    Medicine.objects.get(medicine_id=medicine_id)
                except:
                    form_stock = StockData()
                    formset = StockDataSet(queryset=Stock.objects.none())
                    err = medicine_id + " is not valid"
                    context ={
                    'form_stock': form_stock,
                    'formset' : formset,
                    'err': err
                    }
                    return render(request, 'app/add-stock.html', context)

                s = Stock(medicine_id=medicine_id, batch_id=batch_id, quantity=quantity, expiry_date=expiry_date , vendor_id = vendor_id)
                s.save()

                ms = MedicineStock.objects.get(medicine_id=medicine_id)
                ms.stock += quantity
                ms.save()
            
            form_stock = StockData()
            formset = StockDataSet(queryset=Stock.objects.none())
            context ={
            'form_stock': form_stock,
            'formset' : formset,
            }
            return render(request, 'app/add-stock.html', context)
        else:
            form_stock = StockData()
            err = form_stock.errors
            context ={
                'form_stock': form_stock,
                'err': err
            }
            return render(request, 'app/add-stock.html', context)
    

@login_required(login_url='/login/', redirect_field_name=None)
def TableMedicines(request):
    medicines = Medicine.objects.all()
    context = {
        'medicines': medicines
    }
    return render(request, 'app/all-medicines.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def TableVendors(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'app/all-vendors.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def TableEmployees(request):
    if request.session["is_admin"]:
        employees = Employee.objects.all()
        context = {
            'employees': employees
        }
        return render(request, 'app/all-employees.html', context)
    else:
        context = {
            'err': "Only admins can access this page"
        }
        return render(request, 'app/all-employees.html', context)
    
    


@login_required(login_url='/login/', redirect_field_name=None)   
def TableExpired(request):
    all_stock = Stock.objects.all()
    today = datetime.date.today()

    expired = []

    for stock in all_stock:
        if stock.expiry_date <= today:
            med_id = stock.medicine_id
            ven_id = stock.vendor_id
            batch_id = stock.batch_id
            ms = MedicineStock.objects.get(medicine_id = stock.medicine_id)

            available_stock = ms.stock - stock.quantity

            v = Vendor.objects.get(vendor_id = stock.vendor_id)
            ven_email = v.email
            ven_address = v.address
            expired.append({
                'med_id': med_id,
                'ven_id':ven_id,
                'batch_id':batch_id,
                'available_stock':available_stock,
                'ven_email':ven_email,
                'ven_address':ven_address
            })
            e = ExpiredMedicines(medicine_id = med_id, quantity = stock.quantity, expiry_date=stock.expiry_date)
            e.save()
    
    context = {
        'expired_meds': expired
    }
    return render(request, 'app/expired-medicines.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def TablePurchase(request):
    all_meds_stock = MedicineStock.objects.all()
    
    purchase = []

    for med in all_meds_stock:
        if med.stock <= med.threshold:
            med_id = med.medicine_id
            stock = med.stock
            threshold = med.threshold
            try:
                v = MedicineToVendor.objects.filter(medicine_id=med_id).first()
                ven_id = v.vendor_id
                v_info = Vendor.objects.get(vendor_id=ven_id)
                number = v_info.mobile
                email = v_info.email
                address = v_info.address
                purchase.append({
                    'med_id':med_id,
                    'stock':stock,
                    'threshold':threshold,
                    'ven_id':ven_id,
                    'number':number,
                    'email':email,
                    'address':address
                })
            except:
                ven_id="No vendor"
                number = ""
                email = ""
                address = ""
                purchase.append({
                    'med_id':med_id,
                    'stock':stock,
                    'threshold':threshold,
                    'ven_id':ven_id,
                    'number':number,
                    'email':email,
                    'address':address
                })

    context = {
        'purchase':purchase
    }

    return render(request, 'app/purchase-table.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def RevenueProfitView(request):
    if request.method == 'POST':
        form = RevenueProfit(request.POST)
        if  form.is_valid():
            from_date = datetime.datetime.strptime(form.data['from_date'], '%Y-%m-%d').date()
            to_date = datetime.datetime.strptime(form.data['to_date'], '%Y-%m-%d').date()


        if to_date <= from_date:
            context={
                'form': RevenueProfit(),
                'err': "To date should be after from date"
            }
            return render(request, 'app/revenue-profit.html', context)

        sales = Sales.objects.all()
        expired = ExpiredMedicines.objects.all()

        revenue = profit = 0
        try:
            for sale in sales:
                if sale.date > from_date and sale.date <= to_date:
                    print("************")
                    print(sale.date)
                    print(from_date)
                    print(to_date)
                
                    print("************")
                    print(sale.date)
                    print("************")
                    print(sale.medicine_id)
                    m= Medicine.objects.get(medicine_id=sale.medicine_id)
                    print("************")
                    revenue += (m.unit_sell_price)*sale.quantity
                    profit += (m.unit_sell_price-m.unit_purchase_price)*sale.quantity
            
            print("sasi")
            for med in expired:
                print(type(from_date))
                print(type(to_date))
                print(type(med.expiry_date))
                if med.expiry_date > from_date and med.expiry_date <= to_date:
                    print("123456")
                    m = Medicine.objects.get(medicine_id=med.medicine_id)
                    profit -= med.quantity*(m.unit_purchase_price)

            form = RevenueProfit()
            context={
                'form':form,
                'revenue':revenue,
                'profit':profit
            }
            return render(request, 'app/revenue-profit.html', context)
        except:
            context={
                'form':form,
                'err':"Some error occured"
            }
            return render(request, 'app/revenue-profit.html', context)
    else:
        if request.session["is_admin"]:
            form = RevenueProfit()
            return render(request, 'app/revenue-profit.html', {'form':form})
        else:
            context = {
                'err': "Only admins can access this page"
            }
            return render(request, 'app/revenue-profit.html', context)




# -*- coding: utf-8 -*-


def generatemed_pdf(request):
    """Generate pdf."""
    # Model data
    medicines = Medicine.objects.all()
    # Rendered
    html_string = render_to_string('pdf/medpdf.html', {'medicines': medicines})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_medicines.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def generateven_pdf(request):
    """Generate pdf."""
    # Model data
    vendors = Vendor.objects.all()
    # Rendered
    html_string = render_to_string('pdf/vendorpdf.html', {'vendors': vendors})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_vendors.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def generateemp_pdf(request):
    """Generate pdf."""
    # Model data
    employees = Employee.objects.all()
    # Rendered
    html_string = render_to_string('pdf/employeespdf.html', {'employees': employees})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_employees.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response


def generateexpiredmed_pdf(request):
    """Generate pdf."""
    # Model data
    all_stock = Stock.objects.all()
    today = datetime.date.today()

    expired = []

    for stock in all_stock:
        if stock.expiry_date <= today:
            med_id = stock.medicine_id
            ven_id = stock.vendor_id
            batch_id = stock.batch_id
            ms = MedicineStock.objects.get(medicine_id = stock.medicine_id)
            available_stock = ms.stock - stock.quantity
            ms.stock = available_stock
            ms.save()
            v = Vendor.objects.get(vendor_id = stock.vendor_id)
            ven_email = v.email
            ven_address = v.address
            expired.append({
                'med_id': med_id,
                'ven_id':ven_id,
                'batch_id':batch_id,
                'available_stock':available_stock,
                'ven_email':ven_email,
                'ven_address':ven_address
            })
            stock.delete()
           
    # Rendered
    html_string = render_to_string('pdf/expiredmedicinespdf.html', { 'expired_meds': expired})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_expiredmedicines.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response



def generatepurchasetable_pdf(request):
    """Generate pdf."""
    # Model data
    all_meds_stock = MedicineStock.objects.all()
    
    purchase = []

    for med in all_meds_stock:
        if med.stock <= med.threshold:
            med_id = med.medicine_id
            stock = med.stock
            threshold = med.threshold
            try:
                v = MedicineToVendor.objects.filter(medicine_id=med_id).first()
                ven_id = v.vendor_id
                v_info = Vendor.objects.get(vendor_id=ven_id)
                number = v_info.mobile
                email = v_info.email
                address = v_info.address
                purchase.append({
                    'med_id':med_id,
                    'stock':stock,
                    'threshold':threshold,
                    'ven_id':ven_id,
                    'number':number,
                    'email':email,
                    'address':address
                })
            except:
                ven_id="No vendor"
                number = ""
                email = ""
                address = ""
                purchase.append({
                    'med_id':med_id,
                    'stock':stock,
                    'threshold':threshold,
                    'ven_id':ven_id,
                    'number':number,
                    'email':email,
                    'address':address
                })

           
    # Rendered
    html_string = render_to_string('pdf/purchasetablepdf.html', { 'purchase':purchase})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_purchasetable.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response



def EmployeeLogin(request):
    if request.method == 'POST':
        try:
            if request.session['username']:
                #print('*&*&*&*')

                return render(request ,'app/index.html',{})
        except:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(username=username,password=password)

                if user:
                    if user.is_active:
                        login(request,user)
                        request.session['username'] = username
                        emp = Employee.objects.get(user=user)
                        request.session['is_admin'] = emp.is_admin
                        return render(request ,'app/index.html',{})
                    else:
                        context = {
                            'err':"Account is inactive"
                        }
                        return render(request, 'registration/login.html', context)
                else:
                    context = {
                        'err':"Invalid credentials"
                    }
                    return render(request, 'registration/login.html', context)
            else:
                return render(request, 'registartion/login.html')
    else:
        return render(request, 'registration/login.html', {})


@login_required(login_url='/login/', redirect_field_name=None)
def Selling(request):
    template = 'app/sales.html'

    if request.method != 'POST':
        formsale = SalesData(None)
        form_saleset = SalesDataSet(queryset=Sales.objects.none())
        context ={
            'form_saleset': form_saleset,
            'formsale' : formsale
        }
        return render(request, 'app/sales.html' , context)
        
    else:

        form_saleset = SalesDataSet(request.POST)
        formsale = SalesData(request.POST)
        if form_saleset.is_valid() and formsale.is_valid():
            customer_name = formsale.cleaned_data['customer_name']
            customer_number = formsale.cleaned_data['customer_number']
            date =  formsale.cleaned_data['date']
            sell_price = 0
            i=0
            form_medid = []
            form_med = []
            form_quan = []
            form_sub=[]
            for form_sale in form_saleset: 
                medicine_id = form_sale.cleaned_data['medicine_id']
                quantity = form_sale.cleaned_data['quantity']

                try:
                    Medicine.objects.get(medicine_id=medicine_id)
                except:
                    form_sale = SalesDataSet()
                    context={
                        'formsale' : formsale,
                        'form_sale':form_sale,
                        'err': "Medicine_id "+medicine_id+" not found"
                    }
                    return render(request, 'app/sales.html', context)
                
                allstock = Stock.objects.all()
                tquantity = 0

                for stocks in allstock:
                    if ( stocks.medicine_id == medicine_id):
                        tquantity = tquantity + stocks.quantity
                    
                if( tquantity >= quantity):
                    pass

                            
                else:
                    form_sale = SalesDataSet()
                    context={
                        'formsale' : formsale,
                        'form_sale':form_sale,
                        'err': "Medicine_id "+medicine_id+" is out of stock"
                    }
                    return render(request, 'app/sales.html', context)
                
                req_quantity = quantity
                allstock = Stock.objects.all()

                for stocks in allstock:
                    if ( stocks.medicine_id == medicine_id):
                        if(req_quantity > 0):
                            if(req_quantity >= stocks.quantity):
                                req_quantity = req_quantity - stocks.quantity
                                stocks.quantity = 0
                                stocks.delete()
                                ms = MedicineStock.objects.get(medicine_id=medicine_id)
                                ms.stock = 0
                                ms.save()
                            else:
                                ms = MedicineStock.objects.get(medicine_id=medicine_id)
                                ms.stock = ms.stock - req_quantity
                                ms.save()
                                stocks.quantity = stocks.quantity - req_quantity
                                req_quantity = 0
                                stocks.save()




                f1 = []
                
                k = Bill.objects.all()
                a =len(k)
                f = Sales(medicine_id=medicine_id ,quantity = quantity,date =date,sale_id = a)
                f.save()
                f1.append(f)
                med = Medicine.objects.get(medicine_id=medicine_id)
                sub = quantity * med.unit_sell_price
                sell_price = sell_price + quantity * med.unit_sell_price


                
                
                form_med.append(med.generic_name)
                form_medid.append(medicine_id)
                form_quan.append(quantity)
                form_sub.append(sub)

            
            x = zip(form_medid , form_med , form_quan , form_sub)
           

            b = Bill(customer_name =customer_name,customer_number=customer_number,amount = sell_price,bill_id =a)
            b.save()

  
            context ={
                'formsale': formsale,
                'x' : x,
                #'allsales' : allsales,
                'Sales':f,
                #'Sales': f1,
                'Bill' : b, 
                      
            }
            return render(request,'app/bill.html', context)

        else:
            formsale = SalesData()
            form_saleset = SalesDataSet()
            err = form_saleset.errors
            context ={
               'form_saleset': form_saleset,
               'formsale': formsale,
                'Bill' : b,
                'err': err,
            }
            return render(request, 'app/sales.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def ViewSales(request):
    sales = Sales.objects.all()
    context = {
        'sales': sales
    }
    return render(request, 'app/view-sales.html', context)

def generatesales_pdf(request):
    """Generate pdf."""
    # Model data
    sales = Sales.objects.all()
    # Rendered
    html_string = render_to_string('pdf/salespdf.html', {'sales': sales})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_sales.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

@login_required(login_url='/login/', redirect_field_name=None)
def EditMedicine(request, id):
    if request.method == 'POST':
        form = MedicineData(request.POST)
        if form.is_valid():
            trade_name = form.cleaned_data['trade_name']
            generic_name = form.cleaned_data['generic_name']
            unit_sell_price = form.cleaned_data['unit_sell_price']
            unit_purchase_price = form.cleaned_data['unit_purchase_price']

            m = Medicine.objects.get(medicine_id=id)
            m.trade_name = trade_name
            m.generic_name = generic_name
            m.unit_sell_price = unit_sell_price
            m.unit_purchase_price = unit_purchase_price
            m.save()

            return redirect('/allmedicines/')

        else:
            form = MedicineData()
            context = {
                'form':form,
                'err': form.errors,
                'id':id
            }
            return render(request, 'app/edit-medicine.html',context)
    else:
        form = MedicineData()
        context = {
            'form':form,
            'id':id
        }
        return render(request, 'app/edit-medicine.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def EditVendor(request, id):
    if request.method == 'POST':
        form = VendorData(request.POST)
        if form.is_valid():
            vendor_name = form.cleaned_data['vendor_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            medicine_ids = form.cleaned_data['medicine_ids']

            meds = medicine_ids.split(";")
            for med in meds:
                try:
                    Medicine.objects.get(medicine_id=med)
                except:
                    form_ven = VendorData()
                    context={
                        'form':form,
                        'err': "Medicine ID "+med+" not found",
                        'id':id
                    }
                    return render(request, 'app/edit-vendor.html', context)            

            v = Vendor.objects.get(vendor_id=id)
            v.vendor_name = vendor_name
            v.email = email
            v.mobile = mobile
            v.address = address
            v.medicine_ids = medicine_ids
            v.save()

            MedicineToVendor.objects.filter(vendor_id=id).delete()

            for m in meds:
                k = MedicineToVendor(medicine_id=m,vendor_id=id)
                k.save()

            return redirect('/allvendors')

        else:
            form = VendorData()
            context = {
                'form':form,
                'err': form.errors,
                'id':id
            }
            return render(request, 'app/edit-vendor.html',context)
    else:
        form = VendorData()
        context = {
            'form':form,
            'id':id
        }
        return render(request, 'app/edit-vendor.html', context)

@login_required(login_url='/login/', redirect_field_name=None)
def EditEmployee(request, id):
    if request.method == 'POST':
        user_form = CreateEmployee(request.POST)
        employee_data_form = EmployeeData(request.POST)
        if user_form.is_valid() and employee_data_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            first_name = employee_data_form.cleaned_data['first_name']
            middle_name = employee_data_form.cleaned_data['middle_name']
            last_name = employee_data_form.cleaned_data['last_name']
            date_of_birth = employee_data_form.cleaned_data['date_of_birth']
            gender = employee_data_form.cleaned_data['gender']
            phone = employee_data_form.cleaned_data['phone']
            address = employee_data_form.cleaned_data['address']
            is_admin = employee_data_form.cleaned_data['is_admin']
            password = employee_data_form.cleaned_data['password']
            confirm_password = employee_data_form.cleaned_data['confirm_password']

            prev = Employee.objects.get(id = id).user
            prev_user = User.objects.get(username=prev.username)
            prev_user.delete()

            u = User(username=username, email=email)
            u.set_password(password)
            u.save()
            e = Employee(user=u, first_name=first_name, middle_name=middle_name, last_name=last_name, date_of_birth=date_of_birth,
                        gender=gender, phone=phone, address=address, is_admin=is_admin, password=password, confirm_password=confirm_password)
            e.save()
            return redirect('/allemployees') 
        else:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            err1 = user_form.errors
            err2 = employee_data_form.errors
            context = {
                'form_data': form_data,
                'form_user': form_user,
                'err1': err1,
                'err2': err2,
                'id':id
            }
            return render(request, 'app/edit-employee.html', context)
    else:
        if request.session["is_admin"]:
            form_user = CreateEmployee()
            form_data = EmployeeData()
            context = {
                'form_user':form_user,
                'form_data':form_data,
                'id':id
            }
            return render(request, 'app/edit-employee.html', context)
        else:
            context = {
                'err': "Only admins can access this page"
            }
            return render(request, 'app/edit-employee.html', context)



def generatebill_pdf(request):
    """Generate pdf."""
    # Model data
    bill = Bill.objects.all()
    sales = Sales.objects.all()

    i =len(bill)-1
    

    # Rendered
    html_string = render_to_string('pdf/billpdf.html', {'sales': sales , 'bill':bill,'i':i})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_bill.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def Logout(request):
    logout(request)
    return render(request, 'registration/index.html')