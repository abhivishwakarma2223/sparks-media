from .views import *

from django.urls import path

urlpatterns = [
    path('', index, name ='index'),
    path('base/', base, name ='base.html'),
    path('learnmore/', learnmore, name ='learnmore.html'),
    path('contact/', contact, name='contact'),
    
]
