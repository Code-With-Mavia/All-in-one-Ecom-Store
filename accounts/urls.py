from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from MyEcomStoreNew.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login', redirect_field_name=None), name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('change-email/', views.change_email_view, name='change_email'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
