from django.urls import path
from django.conf.urls import url
from .  import views

app_name = 'msa_app'

urlpatterns = [

    path('', views.HomePage, name='home'),
    path('user/', views.HomePageafterlogin, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('login/', views.EmployeeLogin, name='login'),
    path('createuser/', views.CreateUser, name='create-user'),
    path('createmed/', views.CreateMedicine, name='create-medicine'),
    path('createven/', views.CreateVendor, name='create-vendor'),
    path('addstock/', views.AddStock, name='add-stock'),
    path('allmedicines/', views.TableMedicines, name='all-medicines'),
    path('allvendors/', views.TableVendors, name='all-vendors'),
    path('allemployees/', views.TableEmployees, name='all-employees'),
    path('generatemedpdf/', views.generatemed_pdf, name='generatemed_pdf'),
    path('generatevenpdf/', views.generateven_pdf, name='generateven_pdf'),
    path('generateemppdf/', views.generateemp_pdf, name='generateemp_pdf'),
    path('generateexpiredmedpdf/', views.generateexpiredmed_pdf, name='generateexpiredmed_pdf'),
    path('generatepurchasetablepdf/', views.generatepurchasetable_pdf, name='generatepurchasetable_pdf'),
    path('generatebillpdf/', views.generatebill_pdf, name='generatebill_pdf'),
    path('generatesalespdf/', views.generatesales_pdf, name='generatesales_pdf'),
    path('expiredmedicines/', views.TableExpired, name='expired-medicines'),
    path('purchasemedicines/', views.TablePurchase, name='purchase-medicines'),
    path('revenueprofit/', views.RevenueProfitView, name='revenue-profit'),
    path('viewsales/', views.ViewSales , name = 'viewsale'),
    path('sales/', views.Selling, name='sales'),
    path('editmedicine/<id>', views.EditMedicine, name='edit-medicine'),
    path('editvendor/<id>', views.EditVendor, name='edit-vendor'),
    path('editemployee/<id>', views.EditEmployee, name='edit-employee'),
    path('logout/', views.Logout, name='logout')
]