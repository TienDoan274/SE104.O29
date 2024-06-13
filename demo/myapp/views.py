from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from datetime import date
import datetime
from django.http import JsonResponse
from django.db.models import Sum
default_values = DefaultValues.objects.get(id= 1)
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import datetime


def home(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again")
			return redirect('home')
	else:
		return render(request, 'home.html')
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')
def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username = username, password = password)
			login(request,user)
			messages.success(request, "You have successfully registered")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html',{'form': form})
	return render(request, 'register.html',{'form': form})
def dsKhambenh(request,ngaykham):
    if request.user.is_authenticated:
        # ngaykham = datetime.datetime.strptime(ngaykham,'%Y-%m-%d')
        benhnhans = Benhnhan.objects.filter(ngaykham = ngaykham)
        return render(request, 'dsKhambenh.html',{'benhnhans':benhnhans,'ngaykham':ngaykham})

def themBN(request,ngaykham):
    form = FormThemBN(request.POST or None)
    # form.initial['ngaykham'] = datetime.datetime.strptime(ngaykham,'%Y-%m-%d')
    form.initial['ngaykham'] = ngaykham
    benhnhans = Benhnhan.objects.filter(ngaykham = ngaykham)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid() :
                ten_benh_nhan = form.cleaned_data['hoten']
                # if benhnhans.filter(hoten=ten_benh_nhan).exists():
                    
                    
                if benhnhans.count()<int(default_values.max_patient):
                    form.save()                
                    messages.success(request, "Record Added!")
                    return redirect('dsKhambenh',ngaykham = ngaykham)
                else:
                    messages.success(request, f"Không được khám quá {default_values.max_patient} bệnh nhân")
                    return redirect('dsKhambenh',ngaykham = ngaykham)
            else:
                messages.error(request, "Record not added! Please correct errors.")
        return render(request, 'themBN.html', {'form': form,'ngaykham':ngaykham})
    else:
        messages.error(request, "You must be logged in to use that page!")
        return redirect('home')

def update_BN(request,id):
    if request.user.is_authenticated:
        target_BN = Benhnhan.objects.get(id = id)
        form = FormThemBN(request.POST or None,instance= target_BN)
        form.initial['hoten'] = target_BN.hoten
        form.initial['gioitinh'] = target_BN.gioitinh
        form.initial['namsinh'] = target_BN.namsinh
        form.initial['diachi'] = target_BN.diachi
        form.initial['ngaykham'] = target_BN.ngaykham

        ngaykham = target_BN.ngaykham
        if request.method == "POST":
            if form.is_valid():
                form.save() 
                messages.success(request, "Record Added!")
                return redirect('dsKhambenh',ngaykham = ngaykham)
            else:
                messages.error(request, "Record not added! Please correct errors.")
        return render(request, 'update_BN.html', {'form': form,'id':id,'ngaykham':ngaykham})
    else:
        messages.error(request, "You must be logged in to use that page!")
        return redirect('home')

def delete_BN(request,id):
    target_BN = Benhnhan.objects.get(id = id)
    ngaykham = target_BN.ngaykham
    target_BN.delete()
    return redirect('dsKhambenh',ngaykham = ngaykham)

def check_patient(request):
    ho_ten = request.GET.get('hoTen', None)
    ngay_kham = request.GET.get('ngayKham', None)
    data = {
        'is_taken': Benhnhan.objects.filter(hoten=ho_ten, ngaykham=ngay_kham).exists()
    }
    return JsonResponse(data)

def phieukb(request,id):
    target_BN = Benhnhan.objects.get(id = id)
    ngaykham = target_BN.ngaykham
    try:
        phieukb = PhieuKB.objects.get(benhnhan = target_BN)
    except:
        phieukb = None
    if phieukb:
        try:
            pkbthuocs = PKBthuoc.objects.filter(phieukb = phieukb)
        except:
            pkbthuocs = None
    else:   
        pkbthuocs = None
    return render(request, 'phieukb.html',{'pkbthuocs':pkbthuocs,'phieukb':phieukb,'idBenhnhan':target_BN.id,'ngaykham': ngaykham})

def add_thuocphieukb(request,id):
    if request.user.is_authenticated:
        form = FormthemThuocPKB(request.POST or None)
        form.fields['cachdung'].choices = [(cachdung,cachdung) for cachdung in default_values.cachdung.split(',')]

        benhnhan = Benhnhan.objects.get(id = id)
        phieukb = PhieuKB.objects.get(benhnhan = benhnhan)
        thuocs = Thuoc.objects.all().values('tenThuoc')
        choices = [(thuoc['tenThuoc'], thuoc['tenThuoc']) for thuoc in thuocs]
        form.fields['tenThuoc'].choices = choices
        if request.method == "POST":
            if form.is_valid():
                thuoc = Thuoc.objects.get(tenThuoc = form.cleaned_data['tenThuoc'])
                phieukbthuoc = PKBthuoc.objects.create(
                    phieukb = phieukb,
                    thuoc = thuoc,
                    donvi = form.cleaned_data['donvi'],
                    soluong = form.cleaned_data['soluong'],
                    cachdung = form.cleaned_data['cachdung']
                )
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id)
        return render(request, 'add_thuocphieukb.html',{'form':form,'id':id,'sua':0})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def add_phieukb(request,id):
    form = FormPhieuKB(request.POST or None)
    form.fields['dudoan'].choices = [(loaibenh,loaibenh) for loaibenh in default_values.loaibenh.split(',')]
    benhnhan = Benhnhan.objects.get(id = id)
    form.initial['hoten'] = benhnhan.hoten
    form.initial['ngaykham'] = benhnhan.ngaykham
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                phieukb = PhieuKB.objects.create(
                    benhnhan = benhnhan,
                    trieuchung = form.cleaned_data['trieuchung'],
                    dudoan = form.cleaned_data['dudoan']
                )
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id)
        return render(request, 'add_phieukb.html',{'form':form,'id':id,'sua':0})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def xoa_phieukb(request,id):
    phieukb = PhieuKB.objects.get(id = id)
    id_benhnhan = phieukb.benhnhan.id
    PKBthuocs = PKBthuoc.objects.filter(phieukb = phieukb)
    phieukb.delete()
    PKBthuocs.delete()
    return redirect('phieukb',id = id_benhnhan)

def sua_phieukb(request,id_phieukb):
    phieukb = PhieuKB.objects.get(id = id_phieukb)
    form = FormPhieuKB(request.POST or None)
    form.fields['dudoan'].choices = [(loaibenh,loaibenh) for loaibenh in default_values.loaibenh.split(',')]
    id_benhnhan = phieukb.benhnhan.id
    form.initial['hoten'] = phieukb.benhnhan.hoten
    form.initial['ngaykham'] = phieukb.benhnhan.ngaykham
    form.initial['trieuchung'] = phieukb.trieuchung
    form.initial['dudoan'] = phieukb.dudoan

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                phieukb2,created = PhieuKB.objects.update_or_create(
                    benhnhan = phieukb.benhnhan,
                    defaults={'trieuchung':form.cleaned_data['trieuchung'],
                    'dudoan':form.cleaned_data['dudoan']}
                )
                phieukb2.save()
                # messages.success(request, "Report Added!")
                return redirect('phieukb',id = id_benhnhan)
        return render(request, 'add_phieukb.html',{'form':form,'id':id_benhnhan,'sua':1})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def xoa_pkbthuoc(request,id_pkbthuoc,id_benhnhan):
    pkbthuoc = PKBthuoc.objects.get(id = id_pkbthuoc)
    pkbthuoc.delete()
    return redirect('phieukb',id = id_benhnhan)

def sua_pkbthuoc(request,id_pkbthuoc,id_benhnhan):
    if request.user.is_authenticated:
        pkbthuoc = PKBthuoc.objects.get(id = id_pkbthuoc)
        form = FormthemThuocPKB(request.POST or None)
        form.fields['cachdung'].choices = [(cachdung,cachdung) for cachdung in default_values.cachdung.split(',')]

        benhnhan = Benhnhan.objects.get(id = id_benhnhan)
        phieukb = PhieuKB.objects.get(benhnhan = benhnhan)
        thuocs = Thuoc.objects.all().values('tenThuoc')
        choices = [(thuoc['tenThuoc'], thuoc['tenThuoc']) for thuoc in thuocs]
        form.fields['tenThuoc'].choices = choices
        form.fields['tenThuoc'].initial = pkbthuoc.thuoc.tenThuoc
        form.fields['donvi'].initial = pkbthuoc.donvi
        form.fields['soluong'].initial = pkbthuoc.soluong
        form.fields['cachdung'].initial = pkbthuoc.cachdung
        if request.method == "POST":
            if form.is_valid():
                pkbthuoc.delete()
                thuoc = Thuoc.objects.get(tenThuoc = form.cleaned_data['tenThuoc'])
                phieukbthuoc = PKBthuoc.objects.create(
                    phieukb = phieukb,
                    thuoc = thuoc,
                    donvi = form.cleaned_data['donvi'],
                    soluong = form.cleaned_data['soluong'],
                    cachdung = form.cleaned_data['cachdung']
                )
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id_benhnhan)
        return render(request, 'add_thuocphieukb.html',{'form':form,'id':id_benhnhan,'sua':1})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def thuoc(request):
    if request.user.is_authenticated:
        thoucs = Thuoc.objects.all()
        return render(request, 'thuoc.html',{'thuocs':thoucs})

def them_loai_thuoc(request):
    if request.user.is_authenticated:
        thuocs = Thuoc.objects.all()
        form = FormthemLoaiThuoc(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                try:
                    timthuoc = Thuoc.objects.get(tenThuoc = form.cleaned_data['tenThuoc'])
                except:
                    timthuoc = None
                if timthuoc == None:
                    thuoc = Thuoc.objects.create(
                        tenThuoc = form.cleaned_data['tenThuoc'],
                        giatheovien = form.cleaned_data['giatheovien'],
                        giatheochai = form.cleaned_data['giatheochai'],
                        soviencon = 0,
                        sochaicon = 0
                        )
                    
                else:
                    messages.success(request, "Mẫu thuốc đã tồi tại")
                messages.success(request, "Report Added!")
                return redirect('thuoc')
        return render(request, 'them_loai_thuoc.html',{'form':form})

def update_thuoc(request):
    if request.method == "POST":
        thuoc_id = request.POST.get("thuoc_id")
        field = request.POST.get("field")
        value = request.POST.get("value")
        
        try:
            thuoc = Thuoc.objects.filter(id=thuoc_id)
            thuoc.update(**{field: value})
            return JsonResponse({"status": "success"})
        except Thuoc.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Thuoc not found"})
    
    return JsonResponse({"status": "error", "message": "Invalid request"})

def danhsachTBi(request):
    devices = thietbiYte.objects.all()
    return render(request, 'danhsachTBi.html', {'devices': devices})

def themTBi_new(request):
    if request.method == 'POST':
        form = thietbiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danhsachTBi')
    else:
        form = thietbiForm()
    return render(request, 'them_suaTbi.html', {'form': form, 'title': 'Nhập thiết bị y tế'})
def delete_thuoc(request,id):
    thuoc = Thuoc.objects.get(id = id)
    thuoc.delete()
    return redirect('thuoc')

def chonNgaydskb(request):
    
    return render(request, 'chonNgaydskb.html')

def hoadon(request,id):
    if request.user.is_authenticated:
        target_BN = Benhnhan.objects.get(id = id)
        try:
            phieukb = PhieuKB.objects.get(benhnhan = target_BN)
        except:
            hoadon = None
            phieukb = None
        if phieukb:
            tienthuoc = 0
            try:
                pkbthuocs = PKBthuoc.objects.filter(phieukb = phieukb)
                for pkbthuoc in pkbthuocs:
                    if pkbthuoc.donvi == 'vien':
                        tienthuoc = tienthuoc + pkbthuoc.soluong * pkbthuoc.thuoc.giatheovien
                    else:
                        tienthuoc = tienthuoc + pkbthuoc.soluong * pkbthuoc.thuoc.giatheovien
            finally:
                hoadon,created = Hoadon.objects.update_or_create(
                    benhnhan = target_BN,
                    
                    defaults={'tienthuoc':tienthuoc,'tienkham':default_values.tienkham}
                )
                hoadon.save()
                
        return render(request, 'hoadon.html',{'hoadon':hoadon,'ngaykham':target_BN.ngaykham})

def add_bill(request,pk):
    patient = Benhnhan.objects.get(id = pk)
    form = AddBill(request.POST or None)
    form.initial['name'] = patient.name
    form.initial['date'] = patient.date
    report = thuoc.objects.get(name = patient.name,date = patient.date)
    form.initial['medicineCost'] = report.amount
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Bill Added!")
                return redirect('hoadon',pk = 1)
        return render(request, 'add_bill.html',{'form':form,'patient':patient,'pk':pk})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('hoadon',pk=1)	

       
    
def dsBenhnhan(request):
    phieukbs = PhieuKB.objects.all()
    return render(request, 'dsBenhnhan.html',{'phieukbs':phieukbs})

def thaydoi(request):
    
    return render(request, 'thaydoi.html',{'default_values':default_values})

def themloaibenh(request):
    if request.method == 'POST':
        loaibenh = request.POST['loaibenh']
        default_values.loaibenh = default_values.loaibenh + ',' + str(loaibenh)
        default_values.save()

    return redirect(thaydoi)

def themcachdung(request):
    if request.method == 'POST':
        cachdung = request.POST['cachdung']
        default_values.cachdung = default_values.cachdung + ',' + str(cachdung)
        default_values.save()
    return redirect(thaydoi) 

def updatetienkham(request):
    if request.method == 'POST':
        tienkham = request.POST['updatetienkham']
        default_values.tienkham = tienkham
        default_values.save()
    return redirect(thaydoi)

def updatemaxpatient(request):
    if request.method == 'POST':
        maxpatient = request.POST['updatemaxpatient']
        default_values.max_patient = maxpatient
        default_values.save()
    return redirect(thaydoi)            

def xoaTBi(request, pk):
    device = get_object_or_404(thietbiYte, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('danhsachTBi')
    return render(request, 'xacnhanXoaTBi.html', {'device': device})

def suaTBi(request, pk):
    device = get_object_or_404(thietbiYte, pk=pk)
    if request.method == 'POST':
        form = thietbiForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('danhsachTBi')
    else:
        form = thietbiForm(instance=device)
    return render(request, 'them_suaTbi.html', {'form': form, 'title': 'Sửa thiết bị y tế'}) 

def bao_cao_su_dung_thuoc(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            return redirect('bao_cao_su_dung_thuoc_report', month=month, year=year)
    else:
        form = ReportForm()
    
    return render(request, 'bao_cao_su_dung_thuoc_form.html', {'form': form})

def bao_cao_su_dung_thuoc_report(request, month, year):
    thuoc_data = PKBthuoc.objects.filter(
        phieukb__benhnhan__ngaykham__month=month,
        phieukb__benhnhan__ngaykham__year=year
    ).values('thuoc__tenThuoc', 'donvi').annotate(
        tong_soluong=Sum('soluong'),    
    )
    
    context = {
        'thuoc_data': thuoc_data,
        'month': month,
        'year': year
    }
    return render(request, 'bao_cao_su_dung_thuoc.html', context)

def chonThangbaocao(request):
    
    return render(request, 'chonThangbaocao.html')

def report_revenue_by_month(request, year, month):
    # Get the start and end dates for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    # Filter the invoices by the start and end dates
    invoices = Hoadon.objects.filter(benhnhan__ngaykham__range=(start_date, end_date)).select_related('benhnhan')


    # Calculate the revenue by day
    revenue_by_day = invoices.annotate(day=TruncDay('benhnhan__ngaykham')).values('day').annotate(total_revenue=Sum('tienthuoc')+Sum('tienkham'),patient_count=Count('benhnhan')).order_by('day')
    
    revenue_data = []
    for revenue in revenue_by_day:
        day = revenue['day'].strftime('%Y-%m-%d')
        total_revenue = revenue['total_revenue']
        patient_count = revenue['patient_count']
        revenue_data.append({'day': day, 'total_revenue': total_revenue, 'patient_count': patient_count})
    
    
    return render(request, 'report_revenue.html', {'revenue_data': revenue_data})
