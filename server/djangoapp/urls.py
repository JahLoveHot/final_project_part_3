from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # User authentication paths
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration, name='register'),

    # Cars info
    path('get_cars', views.get_cars, name='getcars'),

    # Dealer related paths
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),

    # Add review path (if needed)

    path('add_review', views.add_review, name='add_review'),
    #path(route='add_review', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

