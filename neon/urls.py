"""neon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . import views
from neonuser import urls as u
from neonadmin import urls as ad
from django.conf import settings
from django.conf.urls.static import static
from . import otpvalidation
from RazorpayIntegration import urls as R

urlpatterns = [
    path('',views.landingpage),
    path('admin/', include(ad)),
    path('login/',views.myloginfn),
    path('lotp/',views.lotp),
    path('sendotp/',otpvalidation.sendotp),
    path('valadatingotp/',otpvalidation.valadatingotp),
    path('logout/',views.logoutusr),
    path('loginv/',views.loginv),
    path('user/',include(u)),
    path('razorpay/',include(R)),
    path('validatetotp/',views.validatetotp),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'neon.views.error_404_view'