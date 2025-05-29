from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoProducto
from .forms import ProductoForm, LoginForm, RegistroForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings



def pagina_inicio(request):
    return render(request, 'crud_app/inicio.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}!')
                if user.is_superuser:
                    return redirect('lista_productos')
                else:
                    return redirect('productos_para_usuario')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Información no válida')
    else:
        form = LoginForm()

    return render(request, 'crud_app/login.html', {'form': form})


@login_required
def vista_protegida(request):
    if request.user.is_superuser:
        return redirect('lista_productos')
    else:
        return redirect('productos_para_usuario')


def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Cuenta creada exitosamente para {user.username}!')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()

    return render(request, 'crud_app/register.html', {'form': form})


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'crud_app/lista_productos.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al crear el producto. Por favor, verifica los datos.')
    else:
        form = ProductoForm()
    return render(request, 'crud_app/crear_producto.html', {'form': form})


def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al actualizar el producto. Por favor, verifica los datos.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'crud_app/actualizar_producto.html', {'form': form})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '¡Producto eliminado exitosamente!')
        return redirect('lista_productos')
    return render(request, 'crud_app/eliminar_producto.html', {'producto': producto})


def productos_para_usuario(request):
    productos = Producto.objects.all()
    return render(request, 'crud_app/productos_para_usuario.html', {'productos': productos})


@login_required
def agregar_al_carrito(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        messages.error(request, "El producto no existe.")
        return redirect('productos_para_usuario')

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito, producto=producto
    )

    if not created:
        carrito_producto.cantidad += 1
        carrito_producto.save()
        messages.success(request, f"Se ha aumentado la cantidad de {producto.nombre}.")
    else:
        messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")

    return redirect('productos_para_usuario')


@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_items = CarritoProducto.objects.filter(carrito=carrito)
    total = sum(item.producto.precio * item.cantidad for item in carrito_items)

    return render(request, 'crud_app/carrito.html', {
        'carrito_items': carrito_items,
        'total': total,
    })


@login_required
def aumentar_cantidad(request, producto_id):
    carrito_producto = get_object_or_404(CarritoProducto, id=producto_id)
    carrito_producto.cantidad += 1
    carrito_producto.save()
    return redirect('carrito')


@login_required
def disminuir_cantidad(request, producto_id):
    carrito_producto = get_object_or_404(CarritoProducto, id=producto_id)
    if carrito_producto.cantidad > 1:
        carrito_producto.cantidad -= 1
        carrito_producto.save()
    return redirect('carrito')


@login_required
def eliminar_del_carrito(request, producto_id):
    try:
        carrito_producto = CarritoProducto.objects.get(id=producto_id)
        carrito_producto.delete()
    except CarritoProducto.DoesNotExist:
        pass
    return redirect('carrito')


@login_required

def realizar_compra(request, producto_id=None):
    carritos = Carrito.objects.filter(usuario=request.user)

    if carritos.exists():
        carrito = carritos.first()
    else:
        carrito = Carrito.objects.create(usuario=request.user)

    producto = Producto.objects.get(id=producto_id) if producto_id else None

    if producto:
        carrito_producto = CarritoProducto.objects.filter(carrito=carrito, producto=producto).first()
        if carrito_producto:
            carrito_producto.delete()
        CarritoProducto.objects.create(carrito=carrito, producto=producto, cantidad=1)
        messages.success(request, f"Producto {producto.nombre} añadido al carrito.")

    carrito_items = CarritoProducto.objects.filter(carrito=carrito)
    subtotal = sum(item.producto.precio * item.cantidad for item in carrito_items)
    envio = 1000  # Puedes ajustar esto
    total = subtotal + envio

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        nombres = request.POST.get('nombres')
        correo_cliente = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        descripcion = request.POST.get('descripcion')
        barrio = request.POST.get('barrio')

        # Validar stock
        for item in carrito_items:
            if item.cantidad > item.producto.stock:
                messages.error(request, f"No hay suficiente stock para {item.producto.nombre}.")
                return redirect('carrito')

        # Actualizar stock
        for item in carrito_items:
            producto = item.producto
            producto.stock -= item.cantidad
            producto.save()

        # Marcar compra como completada
        carrito.completado = True
        carrito.save()

        # Guardar items para mostrar y enviar
        carrito_compra = list(carrito_items)

        # Vaciar carrito
        carrito_items.delete()

        contexto_email = {
            'descripcion': descripcion, 
            'nombres': nombres,            
            'telefono': telefono,
            'barrio': barrio,
            'correo': correo_cliente,
            'direccion': direccion,
            'subtotal': subtotal,
            'envio': envio,
            'total': total,
            'carrito_items': carrito_compra,
            'usuario': request.user,
        }

        html_content = render_to_string('crud_app/email_compra.html', contexto_email)

        text_content = f"Gracias por tu compra en espina de rosa.\n\nDetalles:\nTeléfono: {telefono}\nBarrio: {barrio}\nNombre y apellido: {nombres}\nCorreo: {correo_cliente}\nDirección: {direccion}\nSubtotal: ${subtotal}\nEnvío: ${envio}\nTotal: ${total}\n\nProductos:\n"
        for item in carrito_compra:
            text_content += f"- {item.producto.nombre} x{item.cantidad} = ${item.producto.precio * item.cantidad}\n"

        email = EmailMultiAlternatives(
            subject='Detalles de tu compra en Espina de rosa',
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[correo_cliente],
            bcc=['aespinaderosas@gmail.com'],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, '¡Compra realizada con éxito! Gracias por tu compra.')

        return render(request, 'crud_app/compra_exitosa.html', contexto_email)

    return render(request, 'crud_app/realizar_compra.html', {
        'carrito_items': carrito_items,
        'subtotal': subtotal,
        'envio': envio,
        'total': total,
    })

def compra_exitosa(request):
    carrito = Carrito.objects.filter(usuario=request.user, completado=False).first()
    if carrito:
        carrito_items = CarritoProducto.objects.filter(carrito=carrito)
    else:
        carrito_items = []

    subtotal = sum(item.producto.precio * item.cantidad for item in carrito_items)
    envio = 1000  # Envío fijo
    total = subtotal + envio

    return render(request, 'crud_app/compra_exitosa.html', {
        'carrito_items': carrito_items,
        'subtotal': subtotal,
        'envio': envio,
        'total': total,
        'telefono': request.POST.get('telefono', ''),
        'barrio': request.POST.get('barrio', ''),
        'nombre_y_apellido': request.POST.get('nombres', ''),
        'direccion': request.POST.get('direccion', ''),
    })


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'crud_app/detalle_producto.html', {'producto': producto})


def cerrar_sesion(request):
    logout(request)
    return redirect('login')
