from django.urls import path

from . import views

urlpatterns = [

    # path('', views.cell_list, name='cell_list'),

    path('cell_input/', views.cell_input, name='cell_input'),

#     path('cell_input_confirm/', views.cell_input_confirm, name='cell_input_confirm'),

#     path('<int:cell_id>/', views.cell_detail, name='cell_detail'),

#     path('<int:cell_id>/edit', views.cell_edit, name='cell_edit'),

]