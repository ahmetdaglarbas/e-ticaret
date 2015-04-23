from django.db import models
from django.contrib.auth.models import User
from yonetim.models import *

class MusteriProfili(User):
	adresi = models.TextField()
	cep_telefonu = models.CharField(max_length=10, blank=True, verbose_name="Cep Telefonu")
	ev_telefonu = models.CharField(max_length=10, blank=True, verbose_name="Ev Telefonu")
	
class SepetUrunu(models.Model):
	urun = models.ForeignKey(Urun)
	miktar = models.PositiveIntegerField()
	
	def toplam(self):
		return self.miktar * self.urun.fiyati
	
	toplam = property(toplam)
	
	def __unicode__(self):
		return self.user.username
		
	def genel_toplam(self):
		gtoplam=0
		for urn in self.urunler.all():
			gtoplam = gtoplam + urn.toplam
		return gtoplam
		
	genel_toplam = property(genel_toplam)
	
	def __unicode__(self):
		return self.musteri.username
		
class Sepet(models.Model):
	musteri = models.ForeignKey(User)
	urunler = models.ManyToManyField(SepetUrunu)
	
	def __unicode__(self):
		return self.user.username
		
	def genel_toplam(self):
		gtoplam = 0
		for urn in self.urunler.all():
			gtoplam = gtoplam + urn.toplam
		return gtoplam
		
	genel_toplam = property(genel_toplam)
	
	def __unicode__(self):
		return self.musteri.username
		
