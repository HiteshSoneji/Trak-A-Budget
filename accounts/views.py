from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Ind_User, Org_User
from django.core.mail import EmailMessage
import smtplib
import xlsxwriter
from django.core.files.storage import FileSystemStorage, default_storage
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from openpyxl import Workbook
from openpyxl import load_workbook
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import time

# Splash Screen (First Page)

def splash(request):
    return render(request, 'accounts/splash.html')

#Individual User Register and excel creation

def ind_register_view(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("Username Exists")
            elif User.objects.filter(email=email).exists():
                print("email Taken")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=f_name, last_name = l_name)
                user.save();
                s = Ind_User(username=username, l_name=l_name, f_name=f_name, password=password1, email=email)
                s.save();
                headers = ['loans', 'utility bills', 'insurance', 'entertainment', 'groceries', 'transportation', 'retirement fund', 'emergency fund', 'childcare and school costs', 'clothing', 'maintainance', 'total']
                wb = Workbook()
                ws = wb.active
                ws.title='budget'
                ws.append(headers)
                ws1 = wb.create_sheet('expenses')
                ws1.append(headers)
                u = username
                u = str(u)
                wb.save(settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
                fn = (r'uploads\Indiv_'+u+'_Data.xlsx')
                s.e_file = fn
                s.save()
        else:
            print("Password does not match")
        return redirect('/')
    else:
        return render(request, 'accounts/register_ind.html')

#Individual User Login

def ind_login_view(request):
    if request.method=='POST':
        username = request.POST.get('username', False)
        password1 = request.POST.get('password1', False)

        user = auth.authenticate(username=username, password = password1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        # else:
        #     print("Error")
        #     return redirect('/')
    return render(request, 'accounts/login_ind.html')

# For Budget
def home(request):

# Checking current user and loading excel

    if request.user.is_authenticated:
        u = request.user.username
        u = str(u)
        if u == 'hitesh25':
            fn = (settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
        elif u == 'hitesh98':
            fn = (settings.MEDIA_ROOT+r'\uploads\Organ_'+u+'_Data_1.xlsx')
        fn = str(fn)
        print(fn)
        workbook = load_workbook(fn)
        ws = workbook.get_sheet_by_name('budget')
        # ws = workbook.active
        # print(a1.value)

#Fetching the category and amount

        if request.method == 'POST':
            m = request.POST['mymonth']
            m = str(m)
            m = m.lower()
            # print(m)
            if m == 'none':
                messages.add_message(request, messages.INFO, 'Error No Month Selected')
            if m == 'january':
                s = 1
            if m == 'february':
                s = 2
            if m == 'march':
                s = 3
            if m == 'april':
                s = 4
            if m == 'may':
                s = 5
            if m == 'june':
                s = 6
            if m == 'july':
                s = 7
            if m == 'august':
                s = 8
            if m == 'september':
                s = 9
            if m == 'october':
                s = 10
            if m == 'november':
                s = 11
            if m == 'december':
                s = 12
            l = request.POST['myselection']
            l = str(l)
            l = l.lower()
            # print(l)
            bal = request.POST['exp']
            # print(bal)
            row = 1
            column = 1

# Adding Data to Excel

            for i in range(1,12):
                ref = ws.cell(row = row, column = i)
                ref_value = ref.value
                ref_value = str(ref_value)
                ref_value = ref_value.lower()
                # print(ref_value)
                if ref_value == l:
                    ws.cell(row = row + 1, column = i, value = int(bal))
                    workbook.save(settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
                    break
                else:
                    continue
# # Calculating Total Column
#             for i in range(2,13):
#                 total = 0
#                 for j in range(2,12):
#                     ref = ws.cell(row = row, column = i)
#                     ref_value = ref.value
#                     ref_value = (ref_value)
#                     total = total + ref_value
#                     ws.cell(row = i, column = 12, value = total)
    return render(request, 'accounts/home.html')

#Individual User Logout

def logout_view(request):
    auth.logout(request)
    return render(request, 'accounts/splash.html')

def graph_view(request):

# Sample Graph (Line)

    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8, marker_color='green')],
                    output_type='div')
    u = request.user.username
    u = str(u)
    fn = (settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
    fn = str(fn)
    workbook = load_workbook(fn)
    ws = workbook.get_sheet_by_name('expenses')
    values = []
    total = []
    for i in range(1,12):
        ref = ws.cell(row = 2, column = i)
        ref_value = ref.value
        ref_value = int(ref_value)
        values.append(ref_value)

    for j in range(2,14):
        ref = ws.cell(row = j, column = 12)
        ref_value = ref.value
        if ref_value == None:
            total.append(0)
        elif ref_value != None:
            ref_value = int(ref_value)
            total.append(ref_value)
        # print(total)
    months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'Ocotber', 'November', 'December']
    labels = ['loans', 'utility bills', 'insurance', 'entertainment', 'groceries', 'transportation', 'retirement fund', 'emergency fund', 'childcare and school costs', 'clothing', 'maintainance']

    # p = make_subplots(rows=2, cols=1)
    # plot_div1 = plot(go.Figure(data=[go.Pie(labels=labels, values=values)]))
    # plot_div2 = plot(go.Figure(data=[go.Bar(x=months, y=total)]))
    return render(request, "accounts/home_graph.html", context={'months':months, 'labels':labels, 'values':values, 'total': total})

#For Expenses
def expense_view(request):

#Fetching current user name and loading excel

    if request.user.is_authenticated:
        u = request.user.username
        u = str(u)
        fn = (settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
        fn = str(fn)
        workbook = load_workbook(fn)
        ws = workbook.get_sheet_by_name('expenses')
        # ws = workbook.active
        # print(a1.value)
        if request.method == 'POST':

# Fetching the month, category and amount

            m = request.POST['mymonth']
            m = str(m)
            m = m.lower()
            # print(m)
            if m == 'none':
                messages.add_message(request, messages.INFO, 'Error No Month Selected')
            if m == 'january':
                s = 1
            if m == 'february':
                s = 2
            if m == 'march':
                s = 3
            if m == 'april':
                s = 4
            if m == 'may':
                s = 5
            if m == 'june':
                s = 6
            if m == 'july':
                s = 7
            if m == 'august':
                s = 8
            if m == 'september':
                s = 9
            if m == 'october':
                s = 10
            if m == 'november':
                s = 11
            if m == 'december':
                s = 12
            # print(s)
            l = request.POST['myselection']
            l = str(l)
            l = l.lower()
            # print(l)
            bal = request.POST['exp']
            # print(bal)
            row = 1
            column = 1

# Adding Data to Excel

            for i in range(1,12):
                ref = ws.cell(row = row, column = i)
                ref_value = ref.value
                ref_value = str(ref_value)
                ref_value = ref_value.lower()
                # print(ref_value)
                if ref_value == l:
                    ws.cell(row = s + 1, column = i, value = int(bal))
                    workbook.save(settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')
                    break
                else:
                    continue

# Calculating Total Column

            workbook = load_workbook(fn)
            ws = workbook.get_sheet_by_name('expenses')
            for i in range(2,14):
                total = 0
                for j in range(1,12):
                    ref = ws.cell(row = i, column = j)
                    ref_value = ref.value
                    if ref_value == None:
                        continue
                    else:
                        total = total + ref_value
                        ws.cell(row = i, column = 12, value = total)

                workbook.save(settings.MEDIA_ROOT+r'\uploads\Indiv_'+u+'_Data.xlsx')

    return render(request, 'accounts/home_expenses.html')

# Organisations Register and excel creation

def org_register_view(request):

    if request.method == 'POST':
        c_name = request.POST['c_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("Username Exists")
            elif User.objects.filter(email=email).exists():
                print("email Taken")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name = c_name)
                user.save();
                s = Org_User(username=username, c_name=c_name, password=password1, email=email)
                s.save();
                headers = ['loans', 'utility bills', 'insurance', 'entertainment', 'groceries', 'transportation', 'retirement fund', 'emergency fund', 'childcare and school costs', 'clothing', 'maintainance', 'total']

# Workbook 1 creation
                wb1 = Workbook()
                ws1 = wb1.active
                ws1.title='budget'
                ws1.append(headers)
                ws2 = wb1.create_sheet('expenses')
                ws2.append(headers)
                u = username
                u = str(u)
                wb1.save(settings.MEDIA_ROOT+r'\uploads\Organ_'+u+'_Data_1.xlsx')
                fn = (r'uploads\Organ_'+u+'_Data_1.xlsx')
                s.e_file = fn
                s.save()

#Workbook 2 Creation
                wb2 = Workbook()
                ws1 = wb2.active
                ws1.title='budget'
                ws1.append(headers)
                ws2 = wb2.create_sheet('expenses')
                ws2.append(headers)
                u = username
                u = str(u)
                wb2.save(settings.MEDIA_ROOT+r'\uploads\Organ_'+u+'_Data_2.xlsx')
                fn = (r'uploads\Organ_'+u+'_Data_2.xlsx')
                s.e_file = fn
                s.save()

#Workbook 3 Creation
                wb3 = Workbook()
                ws1 = wb3.active
                ws1.title='budget'
                ws1.append(headers)
                ws2 = wb3.create_sheet('expenses')
                ws2.append(headers)
                u = username
                u = str(u)
                wb3.save(settings.MEDIA_ROOT+r'\uploads\Organ_'+u+'_Data_3.xlsx')
                fn = (r'uploads\Organ_'+u+'_Data_3.xlsx')
                s.e_file = fn
                s.save()

#Workbook 4 Creation
                wb4 = Workbook()
                ws1 = wb4.active
                ws1.title='budget'
                ws1.append(headers)
                ws2 = wb4.create_sheet('expenses')
                ws2.append(headers)
                u = username
                u = str(u)
                wb4.save(settings.MEDIA_ROOT+r'\uploads\Organ_'+u+'_Data_4.xlsx')
                fn = (r'uploads\Organ_'+u+'_Data_4.xlsx')
                s.e_file = fn
                s.save()
        else:
            print("Password does not match")
        return redirect('/')
    else:
        return render(request, 'accounts/register_corp.html')

# Organization Login

def org_login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password1 = request.POST['password1']

        user = auth.authenticate(username=username, password = password1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            print("Error")
            return redirect('')
    return render(request, 'accounts/login_corp.html')

def indiv_pdf_view(request):
    s = "Lol lol lol lol lol lol lol lol " \
        "ok ok ok ok ok ok ok ok ok ok ok" \
        "ok o k dnsosnsodkvnsdpvdsn vobbfhffbhfbfnjs"
    u = request.user.username
    saving = settings.MEDIA_ROOT+r'\uploads\Report_for_'+u+'.pdf'
    c = canvas.Canvas(saving, bottomup=False, pagesize=A4)
    c.drawString(5 ,15 , s)
    c.drawString(5, 30, s)
    c.drawString(5,45,u+',')
    d = Drawing(200, 100)
    pc = Pie()
    pc.x = 65
    pc.y = 15
    pc.width = 70
    pc.height = 70
    pc.data = [10,20,30,40,50,60]
    pc.labels = ['a','b','c','d','e','f']
    pc.slices.strokeWidth=0.5
    pc.slices[3].popout = 10
    pc.slices[3].strokeWidth = 2
    pc.slices[3].strokeDashArray = [2,2]
    pc.slices[3].labelRadius = 1.75
    pc.slices[3].fontColor = colors.red
    d.add(pc)
    d.drawOn(c, 5, 50)
    c.save()
    file_path = os.path.join(settings.MEDIA_ROOT, saving)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        raise Http404
    # time.sleep(0.5)
    # if os.path.isfile(saving):
    #     os.remove(saving)

    return render(request, 'accounts/indiv_pdf.html')
