from django.urls import path
from . import views
from . import matchingsubcategory
from . import chart

urlpatterns = [
    path('', views.adminhome),
    path('viewusers/', views.viewusers),
    path('blockuser/', views.blockuser),
    path('unblockuser/', views.unblockuser),
    #Category URL's
    path('category/', views.category),
    path('addcategory/', views.addcategory),
    path('delcategory/', views.delcategory),
    #Subcategory URL's
    path('subcategory/', views.subcategory),
    path('addsubcategory/', views.addsubcategory),
    path('delsubcategory/', views.delsubcategory),
    path('matchingsubcategory/<int:subcategoryid>',matchingsubcategory.subcat),
    #Product URL's
    path('products/', views.viewproducts),
    path('addproducts/', views.addproducts),
    path('editproducts/', views.editproduct),
    path('edit/', views.editpdt),
    #Banner Url's
    path('banner/',views.banners),
    path('uploadbanner/',views.uploadbanners),
    path('deletebanner/',views.deletebanners),

    path('myorders/',views.myorders),

    path('changeorderstatus/',views.changeorderstatus),

    #coupens

    path('coupens/',views.viewcoupens),
    path('addcoupens/',views.addcoupens),
    path('delcoupen/',views.delcoupen),

    #Offers

    path('offers/',views.viewoffers),
    path('addoffers/',views.addoffers),
    path('deloffers/',views.deloffers),
    path('catorpdt/',views.catorpdt),


    #report
    path('reports/',views.downloadsalesreport),
    path('salesreport/',views.salesreport),
    path('genreport/',views.genreport),





    #chart url's

    # path('catorderqty/<int:catid>/',chart.catorderqty)


]
