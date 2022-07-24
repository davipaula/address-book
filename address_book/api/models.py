from django.db import models


class Address(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="addresses", on_delete=models.CASCADE
    )
    contact_name = models.TextField(max_length=255)
    road = models.TextField(max_length=255)
    house_number = models.TextField(max_length=20)
    postcode = models.TextField(max_length=20, blank=True)
    city = models.TextField(max_length=255, blank=True)
    state = models.TextField(max_length=255, blank=True)
    country = models.TextField(max_length=255, blank=True)

    class Meta:
        ordering = ["contact_name"]
