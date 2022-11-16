from django.urls import path
from . import views

urlpatterns = [
    path('',views.userhome),
    path('signup/',views.signup),
    path('signupuser/',views.signupuser),
    path('wishlist/',views.Wishlist),
    path('wishlist/<int:productid>/',views.AddToWishlist),
    path('delwishlist/',views.DelWishlist),
    path('cart/<int:productid>/',views.AddToCart),
    path('cart/',views.Cart),
    path('delcart/',views.DelCart),
    path('updateqty/',views.updateqty),
    path('checkout/',views.checkout),
    path('cei/',views.cei),
    path('ordercreation/',views.userordercreation),
    path('myorders/',views.myorders),
    path('cancelorder/',views.cancelorder),
    path('returnpdt/',views.returnpdt),

    path('product/<int:pid>/',views.SinglePageProduct),
    #Address
    path('myaddress/',views.myaddress),
    path('addaddress/',views.addAddress),

    path('profile/',views.myprofile),
    path('changepassword/',views.changepassword),
    path('updateprofile/',views.updateprofile),


    #coupen
    path('applycoupen/',views.applycoupen),
    path('removecoupen/',views.removecoupen),


    #search
    path('query/',views.search),

    #Downloads
    path('downloadinvoice/',views.downloadinvoice),

    #2FA
    path('enable2fa/',views.enable2fa),
]
