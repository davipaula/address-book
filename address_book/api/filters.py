import django_filters

from api.models import Address


class AddressFilter(django_filters.FilterSet):
    contact_name = django_filters.CharFilter(lookup_expr="icontains")
    road = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")
    house_number = django_filters.CharFilter(lookup_expr="iexact")
    postcode = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Address
        fields = ["contact_name", "road", "house_number", "postcode", "city", "state", "country"]
