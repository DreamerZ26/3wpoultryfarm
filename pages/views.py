from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Testimonial
from .forms import ContactForm

def home(request):
    products = Product.objects.filter(is_available=True)[:3]  # top 3
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    context = {
        'products': products,
        'testimonials': testimonials,
    }
    return render(request, 'pages/home.html', context)

def about(request):
    return render(request, 'pages/about.html')

def product_list(request):
    products = Product.objects.filter(is_available=True)
    context = {'products': products}
    return render(request, 'pages/products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'pages/product_detail.html', {'product': product})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save message
            contact_msg = form.save()
            # Send email notification
            try:
                send_mail(
                    subject=f"New Contact Message: {contact_msg.subject}",
                    message=f"From: {contact_msg.name} ({contact_msg.email})\n\n{contact_msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER or 'admin@3wpoultry.com'],
                    fail_silently=True,
                )
            except:
                pass
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})