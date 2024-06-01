from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from datetime import date
import datetime
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
        phieukb = phieukb.objects.get(benhnhan = target_BN)
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

def add_phieukb(request,id):
    form = FormPhieuKB(request.POST or None)
    benhnhan = Benhnhan.objects.get(id = id)
    form.initial['hoten'] = benhnhan.hoten
    form.initial['ngaykham'] = benhnhan.ngaykham
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Report Added!")
                return redirect('phieukb',id = id)
        return render(request, 'add_phieukb.html',{'form':form,'id':id})
    else:
        messages.success(request, "You must be logged in to use that page!")
        return redirect('home')

def chonNgaydskb(request):
    
    return render(request, 'chonNgaydskb.html')
# def list_patient(request):
# 	if request.user.is_authenticated:
# 		patients = PatientList.objects.all()
# 		reports = MedicalExamination.objects.all()
# 		return render(request, 'list_patient.html',{'patients':patients,'reports':reports})

def thuoc(request):
    if request.user.is_authenticated:
        thoucs = Thuoc.objects.all()
        return render(request, 'thuoc.html',{'thuocs':thoucs})

def them_thuoc(request):
    if request.user.is_authenticated:
        form = FormthemThuoc(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Report Added!")
                return redirect('thuoc')
        return render(request, 'themthuoc.html',{'form':form})
# def all_patients(request):
# 	if request.user.is_authenticated:
# 		detailed_patients = DetailedPatientList.objects.select_related('patientlist__patient', 'examination').all()
# 		return render(request, 'all_patients.html', {'detailed_patients': detailed_patients})
# 	else:
# 		messages.success(request, "You must be logged in to use that page!")
# 		return redirect('home')

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

def xoaTBi(request, pk):
    device = get_object_or_404(thietbiYte, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('danhsachTBi')
    return render(request, 'xacnhanXoaTBi.html', {'device': device})