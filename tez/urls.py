from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()



urlpatterns = [
    # Examples:
    # url(r'^$', 'tez.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
	url(r'^yonetim/', include('yonetim.urls')),
	url(r'', include('e_ticaret.urls')),
]
