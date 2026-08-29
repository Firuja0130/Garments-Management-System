from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        'admin/',
        views.custom_admin_login,
        name='admin_login'
    ),

    path(
        'admin/login/',
        views.custom_admin_login,
        name='admin_login'
    ),

    path(
        'admin/employee-list/',
        views.admin_redirect,
        name='employee_list'
    ),

    path(
        'admin-redirect/',
        views.admin_redirect,
        name='admin_redirect'
    ),

    path(
        'admin/logout/',
        views.admin_logout,
        name='admin_logout'
    ),


    # =========================
    # HOME / GENERAL
    # =========================

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'login/',
        views.login_page,
        name='login_page'
    ),


    # =========================
    # EMPLOYEE REGISTRATION
    # =========================

    path(
        'employee-register/',
        views.employee_register_page,
        name='employee_register_page'
    ),

    path(
        'employee/register/',
        views.employee_register,
        name='employee_register'
    ),

    path(
        'employees/add/',
        views.employee_add,
        name='employee_add'
    ),

    path(
        'employees/edit/<int:sl>/',
        views.employee_edit,
        name='employee_edit'
    ),

    path(
        'employees/delete/<int:sl>/',
        views.employee_delete,
        name='employee_delete'
    ),


    # =========================
    # SUPPLIER
    # =========================

    path(
        'supplier-register/',
        views.supplier_register_page,
        name='supplier_register_page'
    ),

    path(
        'supplier/register/',
        views.supplier_register,
        name='supplier_register'
    ),

    path(
        'supplier/add/',
        views.supplier_add,
        name='supplier_add'
    ),

    path(
        'supplier/edit/<int:sl>/',
        views.supplier_edit,
        name='supplier_edit'
    ),

    path(
        'supplier/delete/<int:sl>/',
        views.supplier_delete,
        name='supplier_delete'
    ),

    path(
        'supplier/dashboard/',
        views.supplier_dashboard,
        name='supplier_dashboard'
    ),

    path(
        'supplier/logout/',
        views.supplier_logout,
        name='supplier_logout'
    ),


    # =========================
    # PRODUCTS
    # =========================

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    path(
        'products/add/',
        views.product_add,
        name='product_add'
    ),

    path(
        'products/edit/<int:sl>/',
        views.product_edit,
        name='product_edit'
    ),

    path(
        'products/delete/<int:sl>/',
        views.product_delete,
        name='product_delete'
    ),


    # =========================
    # FACE RECOGNITION ATTENDANCE
    # =========================

    path(
        'attendance/',
        include('attendance.urls')
    ),


    # =========================
    # OTHER ATTENDANCE PAGES
    # =========================

    path(
        'attendance/all/',
        views.attendance_list,
        name='attendance_list'
    ),

    path(
        'attendance/edit/<int:pk>/',
        views.attendance_edit,
        name='attendance_edit'
    ),

    path(
        'attendanceE/',
        views.attendance_history,
        name='attendance_history'
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),


    # =========================
    # BONUS
    # =========================

    path(
        'employee/bonus/',
        views.employee_bonus,
        name='employee_bonus'
    ),
]