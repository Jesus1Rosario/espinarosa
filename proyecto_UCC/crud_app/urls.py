from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('inicio/', views.pagina_inicio, name='pagina_inicio'),
    path('login/', login_view, name='login'),
    path('vista_protegida/', views.vista_protegida, name='vista_protegida'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/aumentar/<int:producto_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('comprar/', views.realizar_compra, name='realizar_compra'),
    path('comprar/<int:producto_id>/', views.realizar_compra, name='realizar_compra'),
    path('realizar_compra/<int:producto_id>/', views.realizar_compra, name='realizar_compra_con_producto'),
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('productos/', views.productos_para_usuario, name='productos_para_usuario'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('register/', views.register_view, name='register'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('producto/eliminar/<int:pk>', views.eliminar_producto, name='eliminar_producto'),
    path('listaproductos/', views.lista_productos, name='lista_productos')

]
