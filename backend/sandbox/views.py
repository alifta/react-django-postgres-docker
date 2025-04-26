from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from sandbox.forms import ContactForm, RatingForm, RestaurantForm
from sandbox.models import Restaurant
from sandbox.serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    """View for listing and creating restaurants."""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a restaurant."""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


def restaurants_index(request):
    restaurants = Restaurant.objects.all()
    context = {"restaurants": restaurants}
    return render(request, "restaurants.html", context)


def restaurants_form(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            return render(request, "restaurants.html", {"form": form})
    else:
        form = RestaurantForm()

    context = {"form": form}
    return render(request, "restaurants-form.html", context)


def ratings_index(request):
    if request.method == "POST":
        form = RatingForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            return render(request, "ratings.html", {"form": form})
    else:
        form = RatingForm()

    context = {"form": form}
    return render(request, "ratings.html", context)


@login_required
def contacts_index(request):
    contacts = request.user.contacts.all().order_by("-created_at")
    context = {"contacts": contacts, "form": ContactForm()}
    return render(request, "contacts.html", context)


@login_required
def contacts_search(request):
    import time

    time.sleep(2)
    query = request.GET.get("search", "")
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )
    return render(request, "partials/contacts-list.html", {"contacts": contacts})
