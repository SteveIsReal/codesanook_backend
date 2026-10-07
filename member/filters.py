import django_filters
from member.models import Student
from django.db.models import Q


class StudentFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(field_name="nickname", lookup_expr='icontains')
    search = django_filters.CharFilter(method="filter_search")
    is_student = django_filters.BooleanFilter()

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nickname__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value)
        )

    class Meta:
        model = Student
        fields = ['is_student']