from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

# 管理サイト設定
admin.site.site_header = 'BeginnersCTF'
admin.site.index_title = 'BeginnersCTF'
admin.site.site_title = '管理サイト'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ctf.urls')),
    path('accounts/', include('allauth.urls')),
]

# メディアに入ってるファイルにアクセスできるようにする
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
