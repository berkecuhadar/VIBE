from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

# 404 Error Handler (Redirects all broken links back to the landing page)
def handler404(request, exception=None):
    return redirect('home_page')

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Authentication Security Layer: Redirect standard registration/login pages to home portal
    path('vibe/accounts/login/', lambda r: redirect('home_page')),
    path('vibe/accounts/signup/', lambda r: redirect('home_page')),
    
    # Discord OAuth2 Authentication System
    path('vibe/accounts/', include('allauth.urls')),

    # Core Application (All Voting, Rankings, and Codex endpoints)
    path('', include('vibe.urls')),
]

# Development-only static file serving (Production assets are securely handled by WhiteNoise)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    ]