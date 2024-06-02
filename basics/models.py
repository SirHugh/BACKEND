from django.db import models

def upload_to(instance, filename):
    return 'Logo/{filename}'.format(filename=filename)

class Organization(models.Model):
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=255)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True) 

    def save(self, *args, **kwargs):
        if not self.pk and Organization.objects.exists():
            raise ValueError("Only one organization can exist")
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()