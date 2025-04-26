from pprint import pprint

from django.db import connection


def run():
    # Create a restaurant
    # restaurant = models.Restaurant()
    # restaurant.name = "The Italian Place"
    # restaurant.website = "https://www.italian.com"
    # restaurant.date_opened = timezone.now()
    # restaurant.latitude = 37.7749
    # restaurant.longitude = -122.4194
    # restaurant.restaurant_type = models.Restaurant.TypeChoices.ITALIAN
    # restaurant.save()

    # Anothe method to create a restaurant
    # models.Restaurant.objects.create(
    #     name="Pizza Palace",
    #     website="https://www.pizzapalace.com",
    #     date_opened=timezone.now(),
    #     latitude=50.2,
    #     longitude=50.5,
    #     restaurant_type=models.Restaurant.TypeChoices.ITALIAN,
    # )

    # Update a restaurant
    # restaurant = models.Restaurant.objects.first()
    # restaurant.name = "The Pasta Place"
    # restaurant.save(update_fields=["name"])

    # Delete a restaurant
    # restaurant = models.Restaurant.objects.first()
    # restaurant.delete()

    # Create a sales record
    # restaurant = models.Restaurant.objects.first()
    # sale = models.Sale.objects.create(
    #     restaurant=restaurant,
    #     income=9.99,
    #     datetime=timezone.now(),
    # )
    # sale = models.Sale.objects.create(
    #     restaurant=restaurant,
    #     income=5.33,
    #     datetime=timezone.now(),
    # )
    # sale = models.Sale.objects.create(
    #     restaurant=restaurant,
    #     income=2.25,
    #     datetime=timezone.now(),
    # )

    # Fetch all sales records of a restaurant
    # restaurant = models.Restaurant.objects.first()
    # sales = restaurant.sales.all()

    #  Create a rating
    # user = get_user_model().objects.first()
    # restaurant = models.Restaurant.objects.first()
    # rating, created = models.Rating.objects.get_or_create(
    #     user=user,
    #     restaurant=restaurant,
    #     rating=4,
    # )

    pprint(connection.queries)
