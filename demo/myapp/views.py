from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from datetime import date
import datetime
from django.http import JsonResponse


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
def dsKhambenh(request,ngaykhamstr):
    if request.user.is_authenticated:
        # ngaykham = datetime.datetime.strptime(ngaykhamstr,'%Y-%m-%d')
        benhnhans = Benhnhan.objects.filter(ngaykham = ngaykhamstr)
        return render(request, 'dsKhambenh.html',{'benhnhans':benhnhans,'ngaykhamstr':ngaykhamstr})

def themBN(request,ngaykhamstr):
    form = FormThemBN(request.POST or None)
    # form.initial['ngaykham'] = datetime.datetime.strptime(ngaykhamstr,'%Y-%m-%d')
    form.initial['ngaykham'] = ngaykhamstr

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()                
                messages.success(request, "Record Added!")
                return redirect('dsKhambenh',ngaykhamstr = ngaykhamstr)
            else:
                messages.error(request, "Record not added! Please correct errors.")
        return render(request, 'themBN.html', {'form': form,'ngaykhamstr':ngaykhamstr})
    else:
        messages.error(request, "You must be logged in to use that page!")
        return redirect('home')

def phieukb(request,id):
    target_BN = Benhnhan.objects.get(id = id)
    # ngaykhamstr = target_BN.ngaykham.strftime('%m/%d/%Y')
    ngaykhamstr = target_BN.ngaykham
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
    return render(request, 'phieukb.html',{'pkbthuocs':pkbthuocs,'phieukb':phieukb,'idBenhnhan':target_BN.id,'ngaykhamstr': ngaykhamstr})

def add_thuocphieukb(request,id):
    if request.user.is_authenticated:
        form = FormthemThuocPKB(request.POST or None)
        benhnhan = Benhnhan.objects.get(id = id)
        phieukb = PhieuKB.objects.get(benhnhan = benhnhan)
        
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
                # phieukbthuoc = PKBthuoc(phieukb = phieukb,donvi = form.cleaned_data['donvi'],soluong = form.cleaned_data['soluong'],cachdung = form.cleaned_data['cachdung'])
                # phieukbthuoc.save()  
                # phieukbthuoc.thuoc.add(thuoc)
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id)
        return render(request, 'add_thuocphieukb.html',{'form':form,'id':id})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def add_phieukb(request,id):
    form = FormPhieuKB(request.POST or None)
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
                # record = form.save(commit=False)
                # record.phieukb = phieukb
                # record.save()
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id)
        return render(request, 'add_phieukb.html',{'form':form,'id':id})
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


def chonNgaydskb(request):
    
    return render(request, 'chonNgaydskb.html')

def list_patient(request):
	if request.user.is_authenticated:
		patients = Benhnhan.objects.all()
		reports = MedicalReport.objects.all()
		return render(request, 'list_patient.html',{'patients':patients,'reports':reports})

def hoadon(request,id):
    if request.user.is_authenticated:
        target_BN = Benhnhan.objects.get(id = id)
        hoadon = MedicalReport.objects.get(benhnhan = target_BN)
        return render(request, 'hoadon.html',{'hoadon':hoadon})

def add_bill(request,pk):
    patient = Benhnhan.objects.get(id = pk)
    form = AddBill(request.POST or None)
    form.initial['name'] = patient.name
    form.initial['date'] = patient.date
    report = MedicalReport.objects.get(name = patient.name,date = patient.date)
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
