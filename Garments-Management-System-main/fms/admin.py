from django.contrib import admin

from .models import (
    Employee,
    Supplier,
    Product,
    Attendance,
    EmployeeProfile,
    DailyWork
)


admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Product)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        'public_id',
        'user',
        'phone',
        'designation'
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'date',
        'clock_in',
        'clock_out',
        'total_working_time',
        'marked_by_admin'
    )

    list_filter = (
        'date',
        'marked_by_admin'
    )


@admin.register(DailyWork)
class DailyWorkAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'date',
        'product_count'
    )

    list_filter = (
        'date',
    )