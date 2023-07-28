from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path(route='about', view=views.about, name='about'),
    path(route='contact', view=views.contact, name='contact'),
    path(route='registration', view=views.registration, name='registration'),
    path(route='login', view=views.login, name='login'),
    path(route='logout', view=views.login, name='logout'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
    path(route='car_make', view=views.car_make, name='car_make'),
    path(route='car_model', view=views.car_model, name='car_model'),
    path(route='get_Reviews', view=views.get_Reviews, name='get_Reviews'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)