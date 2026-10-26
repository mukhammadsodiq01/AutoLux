from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.cache import never_cache
from .models import Category, Car, Order


def home(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    cars = Car.objects.all().order_by("id")
    active_category = 0

    if category_id.isdigit():
        cars = cars.filter(category_id=category_id)
        active_category = int(category_id)

    if query:
        cars = cars.filter(name__icontains=query) | cars.filter(brand__icontains=query)

    categories = Category.objects.all()
    paginator = Paginator(cars, 3)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "home.html", {
        "cars": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "active_category": active_category,
    })


@never_cache
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


@never_cache
def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form, "next": next_url})


def logout_view(request):
    auth_logout(request)
    return redirect("home")


def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    return render(request, "detail.html", {"car": car})


@login_required
def payment(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == "POST":
        full_name = " ".join(request.POST.get("full_name", "").split())
        phone = request.POST.get("phone", "").strip()
        card_number = request.POST.get("card_number", "").strip()
        errors = []

        clean_name = full_name.replace(" ", "").replace("'", "").replace("-", "")

        if not clean_name.isalpha():
            errors.append("Ism va familiya faqat harflardan iborat bo'lishi kerak.")

        if not (phone.isdigit() and len(phone) == 13):
            errors.append("Telefon raqami 13 ta raqamdan iborat bo'lishi kerak.")

        if not (card_number.isdigit() and len(card_number) == 16):
            errors.append("Karta raqami 16 ta raqamdan iborat bo'lishi kerak.")

        if errors:
            return render(request, "payment.html", {
                "car": car,
                "errors": errors,
                "full_name": full_name,
                "phone": phone,
                "card_number": card_number,
            })

        order = Order.objects.create(
            car=car,
            full_name=full_name,
            phone=phone,
            card_number=card_number,
        )
        return redirect("success", order_id=order.id)

    return render(request, "payment.html", {"car": car})


@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "success.html", {"order": order})
