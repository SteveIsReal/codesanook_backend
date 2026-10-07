import django_filters
from member.models import Student


class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="nickname", lookup_expr='icontains')
    is_student = django_filters.BooleanFilter()

    class Meta:
        model = Student
        fields = ['name', 'is_student']