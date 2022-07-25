import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from api.models import Address


class AddressFilter(django_filters.FilterSet):
    contact_name = django_filters.CharFilter(lookup_expr="icontains")
    road = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")
    house_number = django_filters.CharFilter(lookup_expr="iexact")
    postcode = django_filters.CharFilter(lookup_expr="iexact")
    id = django_filters.NumberFilter(lookup_expr="exact")

    class Meta:
        model = Address
        fields = {"id": ["in"]}


class IsOwnerFilterBackend(DjangoFilterBackend):
    """ "
    Filter that only allows users to get their own objects
    """

    def filter_queryset(self, request, queryset, view):
        if not request.user.id:
            return Address.objects.none()

        # TODO I am not sure if this is the best implementation
        return (
            super().filter_queryset(request, queryset, view).filter(owner=request.user)
        )
