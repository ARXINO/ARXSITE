from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import transaction

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=100,default='')
    city = models.CharField(default='', max_length=32,)
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    karakter_durum = models.CharField(default='Boş Bekliyor', max_length=128)
    karakter_gorunus = models.CharField(default='x', max_length=3)
    arpa_tohumu = models.IntegerField(default=0)
    elma_tohumu = models.IntegerField(default=0)
    arpa_tohumu_sure = models.IntegerField(default=0)
    elma_tohumu_sure = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username




def create_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)




