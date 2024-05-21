from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import *


def index(request):
    auctions = Auctions.objects.filter(active = 1)
    context = {
        'auctions': auctions,
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def new_list(request):
    if request.POST:
        form = AuctionsForm(request.POST,request.FILES)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            # form.save()
            return redirect("index")
        print(form.errors)
    else:
        return render(request,"auctions/new_list.html",{"form": AuctionsForm()})


@login_required(login_url='/login')
def listing_details(request, id):
    listing = Auctions.objects.get(pk=id)
    comments = Comment.objects.filter(auctions_id=id)
    user = request.user
    is_owner = Auctions.objects.filter(owner=request.user)
    BidForm = UpdatePriceForm()
    context = {
        'listing': listing,
        'user': user,
        'comments': comments,
        'form': BidForm,
        'is_owner': is_owner,
    }
    print(context)
    return render(request, "auctions/details.html", context)

@login_required(login_url='/login')
def commentView(request, id):
    auction = get_object_or_404(Auctions, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auctions = auction
            comment.user = request.user
            comment.save()
            return redirect(reverse('listing_details', args=[id]))
        else:
            return HttpResponse(f'{form.errors}')
    

@login_required(login_url='/login')
def update_price(request, auction_id):
    auction = get_object_or_404(Auctions, pk=auction_id)
    
    if request.method == 'POST':
        form = UpdatePriceForm(request.POST)
        
        if form.is_valid():
            new_price = form.cleaned_data['current_price']
            
            # Validar que el nuevo precio sea mayor que el precio actual
            if new_price > auction.current_price:
                # Actualizar el precio actual de la subasta
                auction.current_price = new_price
                auction.save()
                
                # Crear un objeto Bid para registrar la nueva oferta
                bid = Bid.objects.create(amount=new_price, auctions=auction, user=request.user)
                
                return redirect('listing_details', id=auction_id)
            else:
                return HttpResponse("El nuevo precio debe ser mayor que el precio actual.")
        else:
            return HttpResponse("Formulario no válido.")
    else:
        form = UpdatePriceForm()
    
    return redirect('listing_details', id=auction_id)

def closeAuction(request, id):
    #listingData = Auctions.objects.get(pk=id)
    listingData = Auctions.objects.filter(bid__user=id)
    print(listingData)
    listingData.active = False
    owner = Bid.objects.filter()
    listingData.save()
    # isOwner = request.user.username == listingData.owner.username 
    # isListingInWatchlist = request.user in listingData.watchlist.all()
    # allComments = Comment.objects.filter(auctions=listingData)
    return render(request, "auctions/details.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Your auction is closed."
    })