# -*- coding: utf-8 -*-

from django.forms import *
from yonetim.models import *

class ReyonFormu(ModelForm):
	class Meta:
		model = Reyon
		exclude = []

class UrunFormu(ModelForm):
	class Meta:
		model = Urun
		widgets = { 'reyon': HiddenInput() }
		exclude = []
		
class ResimFormu(ModelForm):
	class Meta:
		model = Resim
		widgets = { 'urun': HiddenInput() }
		exclude = []