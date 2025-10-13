import django_filters
from .models import Department, User, Role, DictItem

class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='部门名称')

    class Meta:
        model = Department
        fields = ['status', 'name']

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['status', 'name', 'phone']

class RoleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = django_filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['status', 'name', 'code']

class DictFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type', lookup_expr='icontains')

    class Meta:
        model = DictItem
        fields = ['status', 'name', 'type']
