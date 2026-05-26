from django.urls import path

from contacts.views import ContactListView

app_name = "contacts"

urlpatterns = [
    path("", ContactListView.as_view(), name="list"),
]
