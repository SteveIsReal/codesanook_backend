from .models import Course
import django_filters

class CourseFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
  class Meta:
    model = Course
    fields = ["name"]