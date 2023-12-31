from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="base.html")),  
    path('nfts/', include('nfts.urls')),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^(?P<path>.*)/$', TemplateView.as_view(template_name='base.html'))]
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]