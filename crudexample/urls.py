"""crudexample URL Configuration"""

from django.contrib import admin
from django.urls import path
from employee import views
import employee.views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('', employee.views.main),
    path('check_employee_id/', views.check_employee_id, name='check_employee_id'),
    path('emp/',views.emp),
    path('show/',employee.views.show),
    # path('main/',employee.views.main),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.destroy),
]
