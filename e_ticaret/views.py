# -*- coding: utf-8 -*-

from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test

from yonetim.models import *
from e_ticaret.forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import *
from django.http import *
from django.core.mail import EmailMultiAlternatives
import random


def musteri_kontrol(user):
	if user and user.is_authenticated():
		if user.groups.filter(name='musteri').count() > 0:
			return True
		return False
		
def anasayfa_vitrin(request, rynId):
	sayfa = request.GET.get('sayfa')
	if musteri_kontrol(request.user):
		sepet = Sepet.objects.get_or_create(musteri=request.user)[0]
	if not sayfa: sayfa=1
	
	baslik = 'Reyonlar:'
	reyonlar = Reyon.objects.all()
	
	if rynId:
		urunler_tumu = Urun.objects.filter(reyon=rynId)
	else:
		urunler_tumu = Urun.objects.filter(vitrin=True)
	
	urunler_sayfalari = Paginator(urunler_tumu, 5)
	urunler = urunler_sayfalari.page(int(sayfa))
	
	return render_to_response('e_ticaret_baslangic.html', locals(), context_instance=RequestContext(request))

	
def kayit(request):
	next = request.GET.get('next')
	baslik = 'Mağazam : Müşteri kayıt formu'
	
	if request.method == 'POST':
		form = KullaniciKayitFormu(request.POST)
		if form.is_valid():
			form.save()
			kullanici = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			
			if kullanici.is_authenticated():
				grp = Group.objects.get_or_create(name='musteri')
				kullanici.groups.add(grp[0])
				kullanici.save()
				login(request, kullanici)
			return HttpResponseRedirect(next)
		else:
			form = KullaniciKayitFormu()
		
		return render_to_response('genel.html', locals(), context_instance=RequestContext(request))
		
@user_passes_test(musteri_kontrol)
def musteri_profili(request):
	next = request.GET.get('next')
	baslik = 'Mağazam: Müşteri profili'
	kullanici = MusteriProfili.objects.get(id=request.user.pk)
	
	if request.method == 'POST':
		form = MusteriProfiliFormu(request.POST, instance=kullanici)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(next)
		else:
			form = MusteriProfiliFormu(instance=kullanici)
			
		return render_to_response('genel.html', locals(), context_instance=RequestContext(request))
		
		
def urun_ekle(sepet, urnId):
	urn = Urun.objects.get(pk=urnId)
	urn_var = sepet.urunler.filter(urun=urn)
	if urun_var:
		sepet_urunu = urun_var[0]
		sepet_urunu.miktar = sepet_urunu.miktar+1
		sepet_urunu.save()
	else:
		sepet_urunu = SepetUrunu(urun=urn, miktar=1)
		sepet_urunu.save()
		sepet.urunler.add(sepet_urunu)
		sepet.save()
	
def urun_cikart(sepet, urn):
	urun_var = sepet.urunler.filter(urun=urn)
	
	if urun_var:
		sepet_urunu = urun_var[0]
		sepet.urunler.remove(sepet_uyumu)
		sepet.save()

def urun_guncelle(sepet, miktar, urunId):
	urn = Urun.objects.get(pk=urnId)
	
	if int(miktar) == 0:
		urun_cikart(sepet, urn)
	else:
		sepet_urunu = sepet.urunler.get(urun=urn)
		sepet_urunu.miktar = miktar
		sepet_urunu.save()

@user_passes_test(musteri_kontrol)
def sepet(request):
	sepet = Sepet.objects.get(musteri=request.user)
	
	if request.GET.get('ekle'):
		urun_ekle(sepet, request.GET.get('ekle'))
	
	if request.GET.get('cikart'):
		urunId = request.GET.get('cikart')
		urn = Urun.objects.get(pk=urnId)
		urun_cikart(sepet, urn)
		
	if request.GET.get('miktarGuncelle'):
		yeniMiktar = request.GET.get('miktarGuncelle')
		urnId = request.GET.get('urun')
		urun_guncelle(sepet, yeniMiktar, urnId)
		
	return render_to_response('sepet.html', locals(), context_instance=RequestContext(request))
	
@user_passes_test(musteri_kontrol)
def kart_bilgileri_al(request):
	kullanici = MusteriProfili.objects.get(id=request.user.pk)
	
	if not (kullanici.adresi and (kullanici.cep_telefonu or kullanici.ev_telefonu)):
		return HttpResponseRedirect('/accounts/profil?next=/sepet')

	form = KrediKartiFormu()
	if request.method == 'POST':
		form = KrediKartiFormu(request.POST)
		
		if form.is_valid():
			
			if not sepet.urunler.all():
				return HttpResponseRedirect('/sepet')
			
			kart_bilgileri = form.cleaned_data
			siparis_kodu = random.randrange(10000, 99999)
			
			kart_bilgileri = render_to_response('kart_bilgileri.html', locals(), context_instance=RequestContext(request))
			
			siparis_bilgileri = render_to_response('siparis_bilgileri.html', locals(), context_instance=RequestContext(request))
			
			konu = '%d kodlu sipariş' % siparis_kodu
			
			ileti = EmailMultiAlternatives(konu, '', 'satici@ahmetdaglarbas.com', ['tedarikci@ahmetdaglarbas.com'])
			ileti.attach_alternative(kart_bilgileri.content+siparis_bilgileri.content, "text/html")
			ileti.send()
	
			ileti = EmailMultiAlternatives(konu, '', 'tedarikci@ahmetdaglarbas.com', [request.user.email])
			ileti.attach_alternative(siparis_bilgileri.content, "text/html")
			ileti.send()
			
			sepet.urunler.clear()
			return HttpResponse(siparis_bilgileri.content)
			
		baslik = 'Kredi kartı bilgileri'
		return render_to_response('genel.html', locals(), context_instance=RequestContext(request))
