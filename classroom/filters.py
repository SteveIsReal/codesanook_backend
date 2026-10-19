from .models import Course, Schedule, TimeSlot
import django_filters

class CourseFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
  class Meta:
    model = Course
    fields = ["name"]

class ScheduleFilter(django_filters.FilterSet):
  weekdays = django_filters.BaseInFilter(field_name="weekday", lookup_expr="in")
  start_time = django_filters.TimeFilter(field_name="start_time", lookup_expr="gte")
  end_time = django_filters.TimeFilter(field_name="end_time", lookup_expr="lte")
  class Meta: 
    model = Schedule
    fields = ["weekdays", "start_time", "end_time"]

class TimeSlotFilter(django_filters.FilterSet):
  weekday = django_filters.BaseInFilter(field_name="schedule__weekday", lookup_expr="in")
  start_time = django_filters.TimeFilter(field_name="schedule__start_time", lookup_expr="gte")
  end_time = django_filters.TimeFilter(field_name="schedule__end_time", lookup_expr="lte")
  room = django_filters.BaseInFilter(field_name="room")
  class Meta:
    model = TimeSlot
    fields = ["weekday", "start_time", "end_time", "room"]