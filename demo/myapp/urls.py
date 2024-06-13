from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name ="home"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.register_user, name = "register"),
    
    path("dsKhambenh/<str:ngaykham>/",views.dsKhambenh, name = "dsKhambenh"),
    path('themBN/<str:ngaykham>/', views.themBN, name='themBN'),
    path('update_BN/<int:id>/', views.update_BN, name='update_BN'),
    path('delete_BN/<int:id>/', views.delete_BN, name='delete_BN'),
    path('kiem-tra-benh-nhan/', views.check_patient, name='check_patient'),


    path("phieukb/<int:id>/",views.phieukb, name ="phieukb"),
    path("add_phieukb/<int:id>/",views.add_phieukb, name ="add_phieukb"),
    path("xoa_phieukb/<int:id>/",views.xoa_phieukb, name ="xoa_phieukb"),
    path("sua_phieukb/<int:id_phieukb>/",views.sua_phieukb, name ="sua_phieukb"),

    path("add_thuocphieukb/<int:id>/",views.add_thuocphieukb, name ="add_thuocphieukb"),
    path('xoa_pkbthuoc/<int:id_pkbthuoc>/<int:id_benhnhan>', views.xoa_pkbthuoc, name='xoa_pkbthuoc'),
    path('sua_pkbthuoc/<int:id_pkbthuoc>/<int:id_benhnhan>', views.sua_pkbthuoc, name='sua_pkbthuoc'),


    path("hoadon/<int:id>/",views.hoadon, name ="hoadon"),
        
    path("thuoc/",views.thuoc, name ="thuoc"),
    path("them_loai_thuoc/",views.them_loai_thuoc, name ="them_loai_thuoc"),
    path('update_thuoc/', views.update_thuoc, name='update_thuoc'),
    path('delete_thuoc/<int:id>/', views.delete_thuoc, name='delete_thuoc'),


    path("chonNgaydskb/",views.chonNgaydskb, name ="chonNgaydskb"),
    path("dsBenhnhan/",views.dsBenhnhan, name ="dsBenhnhan"),

    path("thaydoi/",views.thaydoi, name ="thaydoi"),
    path('updatemaxpatient/', views.updatemaxpatient, name='updatemaxpatient'),
    path("themloaibenh/",views.themloaibenh, name ="themloaibenh"),
    path("themcachdung/",views.themcachdung, name ="themcachdung"),
    path('updatetienkham/', views.updatetienkham, name='updatetienkham'),

    path('bao_cao_su_dung_thuoc/', views.bao_cao_su_dung_thuoc, name='bao_cao_su_dung_thuoc'),
    path('bao_cao_su_dung_thuoc_report/<int:month>/<int:year>/', views.bao_cao_su_dung_thuoc_report, name='bao_cao_su_dung_thuoc_report'),
    
    path('chonThangbaocao/', views.chonThangbaocao, name='chonThangbaocao'),
    path("report_revenue/<int:year>/<int:month>/",views.report_revenue_by_month, name = "revenue_report"),

    path('danhsachTBi/', views.danhsachTBi, name='danhsachTBi'),
    path('them_thietbi/', views.themTBi_new, name='them_thietbi'),
    path('sua_thietbi/<int:pk>/', views.suaTBi, name='sua_thietbi'),
    path('xoa_thietbi<int:pk>/', views.xoaTBi, name='xoa_thietbi')
]


