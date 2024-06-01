from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name ="home"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.register_user, name = "register"),
    path("dsKhambenh/<str:ngaykhamstr>/",views.dsKhambenh, name = "dsKhambenh"),
    path('themBN/<str:ngaykhamstr>/', views.themBN, name='themBN'),
    path("phieukb/<int:id>/",views.phieukb, name ="phieukb"),
    path("add_phieukb/<int:id>/",views.add_phieukb, name ="add_phieukb"),
    path("add_thuocphieukb/<int:id>/",views.add_thuocphieukb, name ="add_thuocphieukb"),
    path('xoa_pkbthuoc/<int:id_pkbthuoc>/<int:id_benhnhan>', views.xoa_pkbthuoc, name='xoa_pkbthuoc'),

    path("hoadon/<int:id>/",views.hoadon, name ="hoadon"),
    path("add_bill/<int:pk>/",views.add_bill, name ="add_bill"),
    path("thuoc/",views.thuoc, name ="thuoc"),
    path("them_loai_thuoc/",views.them_loai_thuoc, name ="them_loai_thuoc"),
    path('update_thuoc/', views.update_thuoc, name='update_thuoc'),

    path("chonNgaydskb/",views.chonNgaydskb, name ="chonNgaydskb"),

    #path("list_patient/",views.list_patient, name ="list_patient"),
    # path('all_patients/', views.all_patients, name='all_patients'),


    path('danhsachTBi/', views.danhsachTBi, name='danhsachTBi'),
    path('them_thietbi/', views.themTBi_new, name='them_thietbi'),
    path('sua_thietbi/<int:pk>/', views.suaTBi, name='sua_thietbi'),
    path('xoa_thietbi<int:pk>/', views.xoaTBi, name='xoa_thietbi')
]


