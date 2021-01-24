from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404

# Create your views here.
from core.forms import SignUpForm
from .models import Product, Images, HeadSlider, SingleProduct, ContactForm, ContactMessage, CommentForm, Comment


def index(request):
    products_slider = Product.objects.all().order_by('id')[:4]  # First 4 product
    slider = Product.objects.all()  # First 4 product
    head_sliders = HeadSlider.objects.all()  # Head_Slider Special some  products
    products_latest = Product.objects.all().order_by('-id')[:1]  # Last 1 product
    single_product = SingleProduct.objects.all()  # random select all product
    products_all = Product.objects.all()  # random select all product
    paginator = Paginator(products_all, 8)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_all': products_all,
        'head_sliders': head_sliders,
        'single_product': single_product,
        'page_obj': page_obj,
        'slider': slider}
    return render(request, 'index.html', context)


def product_detail(request, id):  # Product Details manage query
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    context = {
        'product': product,
        'images': images,
        'comments': comments,
        'is_favourite': is_favourite,
    }
    return render(request, 'details.html', context)


def product(request):  # For all Product page manage query
    productall = Product.objects.all()
    paginator = Paginator(productall, 8)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'productall': productall,
        'page_obj': page_obj,
    }
    return render(request, 'products.html', context)


def contactus(request):  # For Contact forms manage query
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    form = ContactForm
    context = {'form': form}
    return render(request, 'contactus.html', context)


def login_form(request):  # User login Form
    if request.method == 'POST':  # check post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.success(request, " Username And Password is Incorrect !! ")
            return HttpResponseRedirect('/login')
    context = {}
    return render(request, 'login_form.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup_form(request):  # User signup Form
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            user.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'signup_form.html', context)


def addcomment(request, id):  # user addcomment last url
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


def favourite_post(request, id):  # user favourite_post
    post = get_object_or_404(Product, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect('/')


def post_favourite_list(request):  # user favourite list
    user = request.user
    favourite_posts = user.favourite.all()
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'post_favourite_list.html', context)


def user_comments(request):  # user_comments
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/comments')
