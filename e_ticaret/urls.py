# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns('e_ticaret.views',
	url(r'^(\d)*/?$', 'anasayfa_vitrin'),
	url(r'^accounts/register/$', 'kayit'),
	url(r'^accounts/profil/$', 'musteri_profili'),
	url(r'^sepet/$', 'sepet'),
	url(r'^satinal/kart_bilgileri/$', 'kart_bilgileri_al'),
)