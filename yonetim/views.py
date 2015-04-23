# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.http import *
from django.template import RequestContext
from django.core.paginator import Paginator

from yonetim.forms import *
from yonetim.models import *

def yonetici_kontrol(user):
	if user:
		if user.is_superuser:
			return True
		if user.groups.filter(name='yoneticiler').count() > 0:
			return True
	return False

@user_passes_test(yonetici_kontrol)
def baslangic(request):
	baslik = 'Reyonlar'
	reyonlar = Reyon.objects.all()
	return render_to_response('baslangic.html', locals())
	

@user_passes_test(yonetici_kontrol)
def reyon_sil(request):
	rynId=request.GET.get('id')
	ryn=Reyon.objects.get(pk=rynId)
	ryn.delete()
	return HttpResponseRedirect('/yonetim/')

@user_passes_test(yonetici_kontrol)
def reyon_ekle(request):
	baslik = 'Reyon Ekleme'
	rynId = request.GET.get('id')

	if rynId:
		ryn = Reyon.objects.get(pk=rynId)
		form = ReyonFormu(instance=ryn)
	else:
		form = ReyonFormu()

	if request.method=='POST':
		if rynId: form=ReyonFormu(request.POST, instance=ryn)
		else: form=ReyonFormu(request.POST)
		if form.is_valid():
			form.save()
			return render_to_response('kapat.html')

	return render_to_response('genel.html',
				locals(),
				context_instance=RequestContext(request))

@user_passes_test(yonetici_kontrol)
def reyon_goster(request, rynId):
	sayfa = request.GET.get('sayfa')
	siralama = request.GET.get('siralama')
	siralama_secenekleri = {'1':'adi', '2':'fiyati'}

	if not sayfa: sayfa=1
	if not siralama in siralama_secenekleri: siralama='1'
	
	ryn=Reyon.objects.get(pk=rynId)
	urunler_tumu = Urun.objects.order_by(siralama_secenekleri[siralama]).filter(reyon=rynId)
	
	baslik = u'%s Reyonundaki Ürünler' % ryn.adi
	
	urunler_sayfalari = Paginator(urunler_tumu, 5)
	urunler = urunler_sayfalari.page(int(sayfa))
	
	return render_to_response('reyon_goster.html', locals(), context_instance=RequestContext(request))

	
@user_passes_test(yonetici_kontrol)
def urun_ekle(request):
	rynId = request.GET.get('ryn')
	ryn = Reyon.objects.get(pk=rynId)
	urnId = request.GET.get('urn')
	
	baslik = 'Urun Ekleme (%s)' % ryn.adi
	
	if urnId:
		urn=Urun.objects.get(pk=urnId)
		form=UrunFormu(instance=urn)
	else:
		form=UrunFormu()
		form.fields["reyon"].initial=rynId
		
	if request.method=='POST':
		if urnId:
			form = UrunFormu(request.POST, instance=urn)
		else: 
			form = UrunFormu(request.POST)
		if form.is_valid():
			form.save()
			return render_to_response('kapat.html')
			
	return render_to_response('genel.html', locals(), context_instance=RequestContext(request))

@user_passes_test(yonetici_kontrol)
def urun_sil(request):
	rynId = request.GET.get('ryn')
	urnId = request.GET.get('urn')
	urn = Urun.objects.get(pk=urnId)
	urn.delete()
	
	return HttpResponseRedirect('/yonetim/reyon/%s' % rynId)

@user_passes_test(yonetici_kontrol)
def resimler(request, urnId):
	resimler = Resim.objects.filter(urun=urnId)
	form = ResimFormu(initial={'urun':urnId})
	urn = Urun.objects.get(pk=urnId)
	baslik = urn.adi
	
	if request.GET.get('sil'):
		resim = Resim.objects.get(pk=request.GET.get('sil'))
		resim.delete()
		return HttpResponseRedirect('/yonetim/resimler/%s' % urnId)
	
	if request.method == 'POST':
		form = ResimFormu(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		
	return render_to_response('resim.html', locals(), context_instance=RequestContext(request))
	
	