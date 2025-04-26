from django.urls import path

from sandbox import views

urlpatterns = [
    path("contacts/", views.contacts_index, name="contacts-index"),
    path("contacts-search/", views.contacts_search, name="contacts-search"),
    path("restaurants/", views.restaurants_index, name="restaurants-index"),
    path("restaurants-form/", views.restaurants_form, name="restaurants-form"),
    path("ratings/", views.ratings_index, name="ratings-index"),
]
