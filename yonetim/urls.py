from django.conf.urls import patterns, url, include

urlpatterns = patterns('yonetim.views',
	url(r'^$', 'baslangic'),
	url(r'^reyon_ekle/$', 'reyon_ekle'),
	url(r'^reyon_sil/$', 'reyon_sil'),
	url(r'^reyon/(\d+)*', 'reyon_goster'),
	url(r'^urun_ekle/$', 'urun_ekle'),
	url(r'^urun_sil/', 'urun_sil'),
	url(r'^resimler/(\d+)*$', 'resimler'),
)
