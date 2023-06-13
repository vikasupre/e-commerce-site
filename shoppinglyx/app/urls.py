from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import *

urlpatterns = [
    path('', views.productView.as_view(), name='home'),
    path('product_detail/<int:pk>',
         views.productDetailsView.as_view(), name='product-detail'),
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plusCart, name='pluscart'),
    path('minuscart/', views.minusCart, name='minuscart'),
    path('removeitem/', views.removeItem, name='removeitem'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentDone, name='paymentdone'),

    path('buy_item/', views.buyItem, name='buyitem'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    # authentication start
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
                                                        authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html',
                                                                 form_class=ChangePasswordForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='app/passwordresetform.html',
                                                                form_class=MyPasswordResetForm), name='passwordreset'),
    path('password_reset/done', auth_view.PasswordResetDoneView.as_view(
        template_name='app/passwordresetdone.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='app/passwordresetconfirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),
    path('registration/', views.CustomerRegistrationView.as_view(),
         name="customerregistration"),
    # authentication end


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
