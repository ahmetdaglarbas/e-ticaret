# -*- coding: utf-8 -*-

from django.contrib.auth.forms import *
from captcha.fields import CaptchaField
from e_ticaret.models import *
from datetime import datetime

class KullaniciKayitFormu(UserCreationForm):
	captcha = CaptchaField()
	captcha.help_text = 'Lütfen resimde gördüğünüz harfleri yazınız.'
	captcha.label='Doğrulama kodu'
	
	class Meta:
		model = MusteriProfili
		fields = ('first_name', 'last_name', 'username', 'email')
		
	def clean_mail(self):
		if not self.cleaned_data['email']:
			raise forms.ValidationError(u'E-posta adresi girmelisiniz')
			
		if User.objects.filter(email_iexact=self.cleaned_data['email']):
			raise forms.ValidationError(
				u'''Bu e-posta adresine sahip kullanıcı mecvut.
				Başka bir e-posta adresi kullanın.''')
		return self.cleaned_data['email']
		
class MusteriProfiliFormu(forms.ModelForm):
	class Meta:
		model = MusteriProfili
		fields = ('first_name', 'last_name', 'email', 'adresi', 'ev_telefonu', 'cep_telefonu')
		
	def save(self, commit=True):
		instance = super(MusteriProfiliFormu, self).save(commit=False)
		if commit:
			instance.save()
		return instance

		
class KrediKartiFormu(forms.Form):
	kart_adi = forms.CharField(label="Kart üzerindeki isim")
	kart_soyadi = forms.CharField(label="Kart üzerindeki soyisim")
	kart_no = forms.CharField(label="Kart numarası", help_text="<i>Sayilar arasına boşluk koymadan</i>")
	kart_skk = forms.CharField(label="Son kullanma tarihi", help_text="<i>ay/yıl örn: 06/2014</i>")
	guvenlik_no = forms.IntegerField(label="Güvenlik numarası", help_text="<i>Kartınızın arkasındaki son üç rakam</i>")
	
	def clean_kart_no(self):
		kart_no = self.cleaned_data['kart_no']
		
		if not kart_no.isdigit():
			raise forms.ValidationError('Kart numarası sayılardan oluşmalıdır.')
		if not 13 <= len(kart_no) <=16:
			raise forms.ValidationError('Kart numarası geçersiz.')
		
		return kart_no
		
	def clean_kart_skk(self):
		kart_skk = self.cleaned_data['kart_skk']
		
		if not kart_skk.count('/')==1:
			raise forms.ValidationError('son kullanma tarihi hatalı.')
		
		ay,yil = kart_skk.split('/')
		
		if not (ay.isdigit() and yil.isdigit()):
			raise forms.ValidationError('ay ve yıl değerleri sayısal olmalı.')

		if not 1 <= int(ay) <= 12:
			raise forms.ValidationError('ay 1-12 arasında olmalı.')

		skk = datetime(int(yil), int(ay),1)
		if skk < datetime.now():
			raise forms.ValidationError('Girdiğiniz tarih eski.')
			
		return kart_skk
		