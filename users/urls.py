from django.urls import path
from .views import SignUp, ProfileCompletionView, logout_view, LoginView,ChangePasswordView
#from users.views import DirectActivationView
from djoser.views import UserViewSet

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileCompletionView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', logout_view, name='logout'),
   # path('auth/direct-activate/', DirectActivationView.as_view(), name='direct-activate'),
    path('auth/users/activate/', 
         UserViewSet.as_view({'post': 'activation'}), 
         name='user-activate'),
    path('auth/users/reset_password/', 
         UserViewSet.as_view({'post': 'reset_password'}), 
         name='reset-password'),
    path('auth/users/reset_password_confirm/', 
         UserViewSet.as_view({'post': 'reset_password_confirm'}), 
         name='reset-password-confirm'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
]