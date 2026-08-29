from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Employee(models.Model):
    sl = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    position = models.CharField(max_length=10, default='Worker')
    phone = models.IntegerField()
    salary = models.IntegerField(default=10000)
    password = models.CharField(max_length=128, null=True, blank=True)
    bonus_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )


class Supplier(models.Model):
    sl = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default="changeme123")
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, default="Unknown")
    Raw_Material = models.CharField(
        default="Unknown",
        max_length=50
    )
    Quantity = models.IntegerField(
        null=True,
        blank=True,
        default=0
    )
    Price = models.IntegerField(default=0)


class Product(models.Model):
    sl = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=1000)


class EmployeeProfile(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    public_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = (
                'EMP-' +
                uuid.uuid4().hex[:8].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} ({self.public_id})'


class Production(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    employee_profile = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='productions',
        null=True
    )

    date = models.DateField(auto_now_add=True)

    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            'employee_profile',
            'date'
        )

    def __str__(self):
        return (
            f"Employee: {self.employee.name}, "
            f"Date: {self.date}, "
            f"Quantity: {self.quantity}"
        )


class Attendance(models.Model):

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    date = models.DateField(
    default=timezone.localdate
)

    clock_in = models.DateTimeField(
        null=True,
        blank=True
    )

    clock_out = models.DateTimeField(
        null=True,
        blank=True
    )

    total_working_time = models.DurationField(
        null=True,
        blank=True
    )

    marked_by_admin = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['-date', '-clock_in']

    def __str__(self):
        return (
            f"{self.employee.public_id} - {self.date}"
        )


class DailyWork(models.Model):

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='daily_works'
    )

    date = models.DateField()

    product_count = models.PositiveIntegerField(
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:
        unique_together = (
            'employee',
            'date'
        )

        ordering = ['-date']

    def __str__(self):
        return (
            f'{self.employee.public_id} - '
            f'{self.date} -> '
            f'{self.product_count}'
        )