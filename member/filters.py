import django_filters
from member.models import Student, Lead
from django.db.models import Q


class StudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(lead__nickname__icontains=value) |
            Q(lead__first_name__icontains=value) |
            Q(lead__last_name__icontains=value)
        )

    class Meta:
        model = Student
        fields = []

class LeadFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nickname__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value)
        )

    class Meta:
        model = Lead
        fields = ["approve"]