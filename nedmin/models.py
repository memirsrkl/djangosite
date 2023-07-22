from django.db import models

class admins(models.Model):
    admin_name = models.TextField(max_length=100,default='Belirtilmemiş')
    admin_pass = models.TextField(max_length=100,default='Belirtilmemiş')
    admin_adress=models.TextField(max_length=400,default='Belirtilmemiş')
    admin_insta=models.TextField(max_length=400,default='Belirtilmemiş')
    admin_twitter=models.TextField(max_length=400,default='Belirtilmemiş')
    admin_email=models.TextField(max_length=400,default='Belirtilmemiş')
    admin_phone=models.IntegerField()
    admin_realname=models.TextField(max_length=400,default='Belirtilmemiş')
    admin_surname=models.TextField(max_length=400,default='Belirtilmemiş')

    
    def __str__(self):
        return self.admin_name
    class Meta:
        db_table = 'app_admin'
class yazilar(models.Model):
    yazi_baslik=models.TextField(max_length=100)
    yazi_icerik=models.TextField(max_length=400)
    yazi_resim = models.FileField(upload_to='static/img')
    def __str__(self):
        return self.yazi_baslik
    class Meta:
        db_table='app_yazilar'