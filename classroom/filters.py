from .models import Course, Schedule
import django_filters

class CourseFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
  class Meta:
    model = Course
    fields = ["name"]

class ScheduleFilter(django_filters.FilterSet):
  weekdays = django_filters.BaseInFilter(field_name="weekday", lookup_expr="in")
  class Meta:
    model = Schedule
    fields = ["weekdays"]