from django.contrib import admin
from django.urls import path
from app import views as app_views
from nedmin import views as nedmin_views
from django.conf.urls.static import static
from django.conf import settings
from nedmin.views import AdminGiris

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_info/<int:id>', nedmin_views.user_info_view, name='user_info_url_name'),
    path('contact/', nedmin_views.contact_view, name='contact_url_name'),
    path('add_post/', nedmin_views.add_post_view, name='add_post_url_name'),
    path('new_page/', nedmin_views.new_page_view, name='new_page_url_name'),
    path('nedmin', nedmin_views.AdminGiris),
    path('admin_login/', nedmin_views.AdminLogin, name='admin_login'),
    path('admin_homepage/<int:id>/', nedmin_views.AdminHomePage, name='admin_homepage'),
    path('edit',nedmin_views.Edit,name="edit"),
    path('sifreyenile',nedmin_views.sifreyenile,name='sifreyenile'),
    path('asilsifreyenile/<int:id>',nedmin_views.asilsifreyenile,name='asilsifreyenile'),
    path('update/<int:id>',nedmin_views.update,name="update"),
    path('', app_views.SignupPage, name='signup'),
    path('login/', app_views.LoginPage, name='login'),
    path('home/', app_views.HomePage, name='home'),
    path('logout/', app_views.LogoutPage, name='logout'),
    path('logoutadmin/', nedmin_views.AdminLogout, name='logoutadmin'),
    path('ekle/', app_views.ekleme, name='ekle'),
    path('search/', app_views.search_view, name='search'),
    path('filter/', app_views.filter_results, name='filter_results'),
    path('admin_giris/', nedmin_views.AdminGiris, name='admin_giris'),
    path('show/', app_views.filter_results, name='show_all'),
    path('delete/<int:id>/', app_views.delete_iha, name='delete_iha'),
    path('yazisil/<int:id>/', nedmin_views.yazisil, name='yazisil'),
    path('duzenle/<int:id>/', app_views.duzenle_iha, name='duzenle_iha'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)