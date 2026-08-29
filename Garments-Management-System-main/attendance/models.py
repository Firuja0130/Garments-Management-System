from django.db import models
from fms.models import EmployeeProfile


class RegisteredFace(models.Model):
    employee = models.OneToOneField(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='registered_face'
    )

    face_image = models.ImageField(
        upload_to='registered_faces/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Face of {self.employee.employee.name}"