from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import * 
from django.contrib import messages
from ORDER.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from RECOMMENDATION_SYSTEM.views import *
def shoe_page_view(request, pk):
    shoe = get_object_or_404(Shoes, id=pk)
    form = AddToCartForm(request.POST or None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login') 

        if form.is_valid():
            size = form.cleaned_data['size']
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                shoe=shoe,
                size=size,
            )
            if not created:
                cart_item.save()
            messages.success(request, 'The item has been added to your Cart')
    return render(request, 'HomePage/shoe_view.html', {'shoe': shoe, 'form': form})



def tag_view(request, tag):
    shoes = Shoes.objects.filter(tag__slug=tag)
    tags = Tag.objects.all()
    brands = Brand.objects.all()
    form = SearchForm(request.GET)
    
    paginator = Paginator(shoes, 9)  
    page = request.GET.get('page')
    try:
        shoes = paginator.page(page)
    except PageNotAnInteger:
        shoes = paginator.page(1)
    except EmptyPage:
        shoes = paginator.page(paginator.num_pages)
    context = {
        'shoes': shoes,
        'tags': tags,
        'brands': brands,
        'form': form
    }
    return render(request, 'HomePage/home.html', context)


def home_view(request):
    form = SearchForm(request.GET)
    shoes = Shoes.objects.all()
    #
    user = request.user
    user_item_matrix = prepare_data()
    recommended_shoes = []
    if user.is_authenticated:
        if not user_item_matrix.empty:
            recommended_shoes = recommend_shoes(user.id, user_item_matrix)
    #
    

    if form.is_valid():
        name = form.cleaned_data.get('name')
        brand = form.cleaned_data.get('brand')
        tag = form.cleaned_data.get('tag')
        if name:
            shoes = shoes.filter(name__icontains=name)
        if brand:
            shoes = shoes.filter(brand=brand)
        if tag:
            shoes = shoes.filter(tag=tag)

    
    paginator = Paginator(shoes, 9)  
    page = request.GET.get('page')
    try:
        shoes = paginator.page(page)
    except PageNotAnInteger:
        shoes = paginator.page(1)
    except EmptyPage:
        shoes = paginator.page(paginator.num_pages)

    context = {
        'shoes': shoes,
        'form': form,
        'recommended_shoes': recommended_shoes
    }

    return render(request, 'HomePage/home.html', context)










    

    



    
    
