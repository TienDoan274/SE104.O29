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

    path("phieukb/<int:id>/pdf/", views.generate_pdf, name="generate_pdf"),
    path("phieukb/<int:id>/",views.phieukb, name ="phieukb"),
    path("add_phieukb/<int:id>/",views.add_phieukb, name ="add_phieukb"),
    path("add_thuocphieukb/<int:id>/",views.add_thuocphieukb, name ="add_thuocphieukb"),
    path('xoa_pkbthuoc/<int:id_pkbthuoc>/<int:id_benhnhan>', views.xoa_pkbthuoc, name='xoa_pkbthuoc'),

    path("hoadon/<int:id>/",views.hoadon, name ="hoadon"),
    path("add_bill/<int:pk>/",views.add_bill, name ="add_bill"),
    
    path("thuoc/",views.thuoc, name ="thuoc"),
    path("them_loai_thuoc/",views.them_loai_thuoc, name ="them_loai_thuoc"),
    path('update_thuoc/', views.update_thuoc, name='update_thuoc'),
    path('delete_thuoc/<int:id>/', views.delete_thuoc, name='delete_thuoc'),

    path("chonNgaydskb/",views.chonNgaydskb, name ="chonNgaydskb"),
    #path("list_patient/",views.list_patient, name ="list_patient"),
    # path('all_patients/', views.all_patients, name='all_patients'),
    path('bao_cao_su_dung_thuoc/', views.bao_cao_su_dung_thuoc, name='bao_cao_su_dung_thuoc'),
    path('bao_cao_su_dung_thuoc_report/<int:month>/<int:year>/', views.bao_cao_su_dung_thuoc_report, name='bao_cao_su_dung_thuoc_report'),
    path('bao_cao_su_dung_thuoc_report/<int:month>/<int:year>/pdf/', views.bao_cao_su_dung_thuoc_report_pdf, name='bao_cao_su_dung_thuoc_report_pdf'),
    path('chonThangbaocao/', views.chonThangbaocao, name='chonThangbaocao'),
    path("report_revenue/<int:year>/<int:month>/",views.report_revenue_by_month, name = "revenue_report"),
    path('report_revenue/<int:year>/<int:month>/pdf/', views.report_revenue_by_month_pdf, name='report_revenue_by_month_pdf'),
    path('danhsachTBi/', views.danhsachTBi, name='danhsachTBi'),
    path('them_thietbi/', views.themTBi_new, name='them_thietbi'),
    path('sua_thietbi/<int:pk>/', views.suaTBi, name='sua_thietbi'),
    path('xoa_thietbi<int:pk>/', views.xoaTBi, name='xoa_thietbi'),


    path('view_user_info/', views.view_user_info, name='view_user_info'),
    path('update_user_info/', views.edit_user_info, name='update_user_info'),

    path('employees/role-selection/', views.employee_role_selection, name='employee_role_selection'),
    path('employees/list/<str:role>/', views.list_employees_by_role, name='view_employees_by_role'),
    path('register-employee/<str:role>/', views.register_employee, name='register_employee'),
    path('edit-profile/<int:pk>/<str:role>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:pk>/<str:role>/', views.delete_employee, name='delete_employee'),

    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]


