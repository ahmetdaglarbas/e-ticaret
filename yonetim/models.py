# -*- coding: utf-8 -*-

from django.db import models

class Reyon(models.Model):
	adi = models.CharField(max_length=50, verbose_name='Adı')
	aciklama = models.CharField(max_length=50, blank=True, verbose_name='Açıklama')
	
	def __unicode__(self):
		return self.adi

		
class Urun(models.Model):
	adi = models.CharField(max_length=50, verbose_name='Adı')
	aciklama = models.CharField(max_length=50, blank=True, verbose_name='Açıklama')
	fiyati = models.FloatField(verbose_name='Fiyatı')
	vitrin = models.BooleanField(verbose_name='Vitrin Ürünü')
	reyon = models.ForeignKey(Reyon, verbose_name='Reyon')
	
	def __unicode__(self):
		return self.adi

	def resimleriAl(self):
		resimler=Resim.objects.filter(urun=self.pk)
		return resimler
		
	class Meta:
		ordering = ['adi']
	
def upload_to(instance, filename):
	return u'urunler/%s/%s' % (instance.urun.id, filename)

class Resim(models.Model):
	urun = models.ForeignKey(Urun)
	resim = models.ImageField(upload_to=upload_to, blank=True)
	
	def __unicode__(self):
		return u'%s: %s' % (self.urun.adi, self.resim.file.name)
