from django.db import models
#Iha için kullanacağım database modeli tanımlama
class Ihas(models.Model):
    adi = models.CharField(max_length=100)
    renk = models.CharField(max_length=100)
    yıl= models.CharField(max_length=4)
    ozellikler = models.TextField()
    dosya_yolu = models.FileField(upload_to='static/img')

    def __str__(self):
        return self.adi
    class Meta:
        app_label = 'app'
# Create your models here.
        