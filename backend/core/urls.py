from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListAPIView.as_view()),
    path("products/info/", views.product_info),
    path("products/<int:product_id>", views.ProductDetailAPIView.as_view()),
    path("orders/", views.OrderListAPIView.as_view()),
    #
    # path("numbers/", views.display_even_numbers),
    # path("homes/", views.homes),
    # path("articles", views.articles),
    # # path("articles/<int:pk>", views.article),
    # path("orders/", views.Orders.listOfOrders),
    # path("papers", views.PaperList.as_view()),
    # path("papers/<int:pk>", views.Paper.as_view()),
    # path(
    #     "books",
    #     views.BookView.as_view(
    #         {
    #             "get": "list",
    #             "post": "create",
    #         }
    #     ),
    # ),
    # path(
    #     "books/<int:pk>",
    #     views.BookView.as_view(
    #         {
    #             "get": "retrieve",
    #             "put": "update",
    #             "patch": "partial_update",
    #             "delete": "destroy",
    #         }
    #     ),
    # ),
]
