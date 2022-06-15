from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from customer.models import Profile
from twilio.rest import Client
from .forms import CreatePostForm
from .models import Product, Buyerdetail


# Create your views here.
def HomeDecor(request):
    homedecor = Product.objects.filter(category='H')
    return render(request, 'home_decor.html', {'home': homedecor})


class CreatePostView(View):
    def get(self, request):
        form = CreatePostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if request.method == 'POST':
            user = request.user
            title = request.POST['title']
            category = request.POST['category']
            description = request.POST['description']
            price = request.POST['price']
            city = request.POST['city']
            state = request.POST['state']
            product_image = request.FILES['product_image']
            product = Product(user=user, title=title, category=category, description=description, price=price,
                              city=city, state=state, product_image=product_image)
            product.save()
            messages.success(request, "Posted Successfully")
            return redirect('create-post')
        return redirect('/home')


class MyPostView(View):
    def get(self, request):
        product = Product.objects.filter(user=request.user)
        return render(request, 'product_list.html', {'products': product})


class MyDeleteView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        messages.info(request, "product  deleted Successfully")
        return redirect('my-post')


class MyEditView(View, ):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        form = CreatePostForm(instance=product)
        return render(request, 'create_post.html', {'form': form, 'product': product})

    def post(self, request, id):
        form = CreatePostForm(request.POST, request.FILES)
        if request.method == 'POST':
            title = request.POST['title']
            category = request.POST['category']
            description = request.POST['description']
            price = request.POST['price']
            city = request.POST['city']
            state = request.POST['state']
            product_image = request.FILES['product_image']
            Product.objects.filter(id=id).update(title=title, category=category, description=description, price=price,
                                                 city=city, state=state, product_image=product_image)
            messages.info(request, "changes added  Successfully")
            return redirect('create-post')
        return redirect('/home')


def search_page(request):
    search = request.GET.get('search')
    product = Product.objects.filter(title__icontains=search)
    return render(request, 'search.html', {'product': product})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'product_detail.html', {'product': product})


class BuyNowView(View):
    def post(self, request, id):
        print('in', id)
        product = Product.objects.get(id=id)
        print(product.user.email)
        buyer_price = request.POST['buyer_price']
        print(buyer_price)
        if request.user.is_authenticated:
            buyer_username = request.user
            print(buyer_username)
            product_name = product.title
            user_obj = User.objects.get(username=request.user)
            buyer = Buyerdetail(buyer_id=user_obj.id, seller_id=product.user.id,product=product, buyer_username=buyer_username,
                                Product_name=product_name, buyer_price=buyer_price)
            buyer.save()
            buyers = Buyerdetail.objects.all()
            name = product.user
            email = product.user.email
            print(email)

            subject = 'Buyer interest'
            message = f'Hi, {name}  your Product  {product_name} got a interest by a customer named {buyer_username}  interested   at Rs {buyer_price} .'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = email
            send_mail(subject, message, from_email, [recipient_list], fail_silently=False,)
            messages.info(request,'An inquiry has sent to the owner showing  your interest.Owner will be get back to you as soon as possible,if he interested in your maximum payable amount')
            return render(request, 'buy_now.html', {'buyer': buyers})


class MyOrderView(View):
    def get(self, request):
        try:
            user_obj = User.objects.get(username=request.user)
            order_list = Buyerdetail.objects.filter(seller=user_obj)
        except:
            context = {
                'order': '',
                'price': '',

            }
        context = {
            'order': order_list,
        }
        print(context)
        return render(request, 'my_order.html', context)


class MyOrderAcceptView(View):
    def post(self, request):
        id = request.POST['prod_id']
        print(id)
        detail = Buyerdetail.objects.get(id=id)
        product_obj = Product.objects.get(id=detail.product.id)
        print(product_obj)
        product_obj.sale_status = 'sold'
        product_obj.save()
        name = detail.buyer_username
        product = detail.Product_name
        price = detail.buyer_price
        buyer_user_obj = User.objects.get(id=detail.buyer_id)
        buyer_email = buyer_user_obj.email
        buyer_user_profile_obj = Profile.objects.get(user=buyer_user_obj)
        phone = buyer_user_profile_obj.phone
        print(phone)
        print(name)
        print(product)
        print(price)
        seller_phone = Profile.objects.get(user=request.user).phone
        print(seller_phone)

        #status check
        purchase = get_object_or_404(Buyerdetail, id=id)
        purchase.status = True
        purchase.save()

        # sending mail to buyer  request response
        subject = 'Accepted Your request'
        message = f'Hi, {buyer_user_obj}  your interest  has accepted  for the product {product}  at Rs {price} .Here i share my details \n My contact Number:{seller_phone}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = buyer_email
        send_mail(subject, message, from_email, [recipient_list], fail_silently=False,)

        # sending sms to seller
        account_sid = 'AC5276dcdd4bb9da5590a5b1e7a63c1965'
        auth_token = 'd49e9ae6dd13585e6df37a69887931c2'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f' Buyer Information: \n Name:{name}\n email :{buyer_email}Contact Number:{phone}',
            from_='+16784987942',
            to=f'+91{seller_phone}'

        )
        print(message.sid)
        messages.info(request,
                      'An email has sent to buyer showing interest to sell the product.afterthat  the buyer will send contact details through sms')
        return render(request, 'my_order.html')


def my_purchase(request):
    buyer = Buyerdetail.objects.all()
    return render(request, 'buy_now.html', {'buyer': buyer})
