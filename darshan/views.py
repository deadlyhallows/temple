from django.contrib.auth.decorators import login_required
from temple.decorators import user_is_temple_manager
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from darshan.models import Picture, Profile, Temples, Darshans, TempleManager
from django.template.loader import render_to_string
from darshan.forms import TempleForm, TempleManagerForm, TempleAddForm, PictureAddForm,DarshanAddForm, PrasadAddForm
from accountregistrations.forms import SignUpForm, contactInspireForm,MobileForm
from django.contrib.auth.forms import AuthenticationForm
from accountregistrations.models import Mobile
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from shop.models import Product
from cart.models import CartItem, Carts
from notify.signals import notify


def home(request):
    temples = Temples.objects.all()

    # arr=[]
    # for prod in totalProduct:
    #     #print("Product ID", prod.id)
    #     arr.append(prod.id)
    # #print(arr)
    # random.shuffle(arr)
    # #print(arr)
    # product_num_entities = Product.objects.all().count()
    # #print("product_num_entities",product_num_entities)
    # product_rand_entities = random.sample(arr, 1)[:1]
    # #print("product_rand_entities", product_rand_entities)
    # product = Product.objects.filter(id__in=product_rand_entities)[:1]
    # #print("product", product)
    product = Product.objects.all()
    paginator = Paginator(temples, 4)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    # print(type(page))
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    # print("queryset", paginator)
    contact_form = contactInspireForm(request.POST or None)
    if contact_form.is_valid():
        messages.success(request, "Successfully Send")
        return render(request, 'darshan/home.html')
    context = {'temples': temples,
               'form': AuthenticationForm,
               'Mobile_form': MobileForm,
               'user_form': SignUpForm,
               'object_list': queryset,
               'page_change_var': page_change_var,
               'product': product,
               'contact_form': contact_form
               }
    return render(request, 'darshan/home.html', context)


def allDarshan(request):
    temples = Temples.objects.all()
    paginator = Paginator(temples, 64)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    # print(type(page))
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {'temples': temples,
               'object_list': queryset,
               'page_change_var': page_change_var
               }
    return render(request, 'darshan/alldarshan.html', context)


def all_Prasad(request, pk):
    # print("jvn")
    # print("PK",pk)
    prasad = Product.objects.filter(Temple_Name_id=pk, is_Prasad=True)
    temple = Temples.objects.get(id=pk)
    context = {
        'prasad': prasad,
        'temple': temple.temple2
    }
    return render(request, 'darshan/allPrasad.html', context)



@login_required
def user_profile(request):
    b = []
    temp = Temples.objects.all()

    user = request.user
    profile = Profile.objects.get(user_id=user.id)

    if user.is_superuser:
        cart = Cart(request)
        if cart is not None:
            try:
                get_cart = Carts.objects.get(user_id=user.id)
            except Carts.DoesNotExist:
                get_cart = Carts.objects.create(active=True, user_id=user.id)
                get_cart.save()

            for item in cart:
                cart_product = get_object_or_404(Product, Product_Name=item['product'])
                cart_item = CartItem.objects.create(quantity=item['quantity'],
                                                    active=True, cart_id=get_cart.id, product_id=cart_product.id)
                cart_item.save()

    # --------For Authenticated user who is not superuser-------------
    cart = Cart(request)
    # print("a")
    if cart is not None:
        try:
            get_cart = Carts.objects.get(user_id=user.id)
        except Carts.DoesNotExist:
            get_cart = Carts.objects.create(active=True, user_id=user.id)
            get_cart.save()

        for item in cart:
            cart_product = get_object_or_404(Product, id=item['product_id'])

            cart_item = CartItem.objects.create(quantity=item['quantity'],
                                                active=True, cart_id=get_cart.id, product_id=cart_product.id)
            cart_item.save()
    # print(cart)
    if request.method == "POST" and "Select_Temple" in request.POST:

        selected_temple = profile.Select_Temple

        form = TempleForm(request.POST, instance=profile)
        if form.is_valid():

            profile = form.save(commit=False)
            for temple in selected_temple:
                profile.Select_Temple.append(temple)

            profile.save()

            return redirect('darshan:user_profile')
        else:
            messages.error(request, "not created at all")
    else:
        form = TempleForm(instance=profile)
    # print("e")

    query_list = get_object_or_404(Profile, user_id=user.id)
    get_user = User.objects.get(id=user.id)
    user_mobile = get_object_or_404(Mobile,user=user)


    if request.method=='POST':
        profile.selected = []

        profile.save()
        for x in query_list.Select_Temple:
            templeTime_pk_list = request.POST.getlist(x, None)
            for z in templeTime_pk_list:
                pic = Picture.objects.get(id=z)
                profile.selected.append(pic.id)
                profile.save()
        messages.success(request, "Time is added")

    for m in query_list.Select_Temple:
        b.append(m)
    paginator = Paginator(b, 5)
    page_change_var = 'page'  # change=request
    page = request.GET.get(page_change_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {'set': user,
               'temples': temp,
               "object_list": queryset,
               'query_list': query_list,
               'form': form,
               'u': get_user,
               'v': user_mobile,
               'page_change_var': page_change_var
               }
    return render(request, 'darshan/user_profile.html', context)



@login_required
def selectedDharshan(request):
    # set = Profile.objects.all()
    user = request.user
    profile = Profile.objects.filter(user_id=user.id)
    for i in profile:
        # print(i)
        for j in i.Select_Temple:
            # print(j)
            temple = Temples.objects.filter(temple2=j)
            # print(temple)
    context = {'set': user,
               'pro': profile}
    return render(request, 'darshan/selectedDharshan.html', context)


@login_required
def delete(request, value):
    # print(value)
    user = request.user
    # print(user)
    query_l = Profile.objects.get(user_id=user.id)
    # print("b")
    for i in query_l.Select_Temple:
        if i == value:
            query_l.Select_Temple.remove(i)
            query_l.save()
    temple = get_object_or_404(Temples, temple2=value)
    img = Picture.objects.filter(Temple_id=temple.id)
    for j in img:
        for k in query_l.selected:
            if k == j.id:
                query_l.selected.remove(k)
                query_l.save()

    return redirect('darshan:user_profile')


@login_required
def details(request, temp):
    # m = localtime().time()
    # FMT = '%H:%M:%S'
    # user = request.user
    # pro = Profile.objects.get(user_id=user.id)
    user = request.user
    temple = get_object_or_404(Temples, temple2=temp)
    darshan = Darshans.objects.filter(temple_id=temple.id)
    # b = Picture.objects.filter(Temple_id=q.id)
    context = {
        'user': user,
        's': darshan,
        'q': temple,
    }
    return render(request, 'darshan/detail.html', context)


def detail(request, temp1):  # ----------------For Anonymous User-----------------------
    # m = localtime().time()
    # FMT = '%H:%M:%S'

    temple = get_object_or_404(Temples, temple2=temp1)
    darshan = Darshans.objects.filter(temple_id=temple.id)
    context = {
        's': darshan,
        'q': temple,


    }
    return render(request, 'darshan/detail.html', context)


def selectedTemple(request, pk):
    # print("jvn")
    # print("PK",pk)
    picture = Picture.objects.filter(Temple_id=pk)
    temple = Temples.objects.get(id=pk)
    context = {
        'picture': picture,
        'temple': temple.temple2
    }
    return render(request, 'darshan/selectedTemple.html', context)




@login_required
@user_is_temple_manager
def manager_profile(request):
    # t = get_object_or_404(TempleManager, user=request.user)
    darshan = Darshans.objects.filter(user=request.user)
    picture = Picture.objects.filter(user=request.user)
    temples = Temples.objects.filter(user=request.user)
    prasad = Product.objects.filter(seller=request.user, is_Prasad=True)
    context = {
        'temples': temples,
        'pictures': picture,
        'darshans': darshan,
        'prasad': prasad
    }
    return render(request, 'darshan/manager_profile.html', context)


# --------------For Temples----------------
@login_required
@user_is_temple_manager
def temple_add(request):
    temple_manager = get_object_or_404(TempleManager, user=request.user)

    add_form = TempleAddForm(request.POST or None, request.FILES or None)

    # print("e")

    if add_form.is_valid():
        # print("r")

        instance = add_form.save(commit=False)
        # print("f")
        instance.user = request.user
        instance.temple2 = temple_manager.Temple_Name
        instance.save()

        return redirect('darshan:manager_profile')
    else:
        # print(add_form.errors)
        arr = []
        for field in add_form:
            arr.append(field.errors)
            # print(field.errors)
            # print("\n")
        messages.error(request, add_form.errors)
        add_form = TempleAddForm(request.POST or None, request.FILES or None)

    context = {'add_form': add_form, }

    return render(request, 'darshan/temple_add.html', context)


@login_required
@user_is_temple_manager
def temple_update(request, s=None):
    instance = get_object_or_404(Temples, temple2=s)
    # print(instance)
    add_form = TempleAddForm(request.POST or None, request.FILES or None, instance=instance)
    # print(add_form.instance.Display_image)
    if add_form.is_valid() == True:
        instance = add_form.save(commit=False)
        instance.save()
        # print("o")
        return redirect('darshan:manager_profile')
    else:
        # print(add_form.errors)
        arr = []
        for field in add_form:
            arr.append(field.errors)
            # print(field.errors)
            # print("\n")
        messages.error(request, add_form.errors)

    context = {
        'add_form': add_form
    }

    return render(request, 'darshan/temple_add.html', context)


@login_required
@user_is_temple_manager
def temple_remove(request, s):
    instance = get_object_or_404(Temples, temple2=s)
    profiles = User.objects.filter(is_superuser=False)

    for prof in profiles:  # -----deleting temple from all profiles and also from their selected -----------------
        # print(prof)
        for x in prof.profile.Select_Temple:
            # print(x)
            temp = Temples.objects.get(temple2=x)
            if (temp.id == instance.id):
                prof.profile.Select_Temple.remove(x)
                # print("d")
                prof.profile.save()
    img = Picture.objects.filter(Temple_id=instance.id)
    for m in profiles:
        for y in m.profile.selected:
            for j in img:
                if y == j.id:
                    m.profile.selected.remove(y)
                    m.profile.save()

    instance.delete()
    return redirect('darshan:manager_profile')


# ---------For Pictures-----------------

@login_required
@user_is_temple_manager
def picture_add(request):
    arr = []
    user = request.user
    temple_manager = get_object_or_404(TempleManager, user=request.user)
    temples = get_object_or_404(Temples, temple2=temple_manager.Temple_Name)
    pic_add_form = PictureAddForm(request.user, request.POST or None, request.FILES or None)
    # print("a")
    if pic_add_form.is_valid():
        instance = pic_add_form.save(commit=False)
        instance.user = request.user
        instance.Temple = temples
        instance.save()

        return redirect('darshan:manager_profile')
    else:
        # print("S")
        # print(pic_add_form.errors)
        for field in pic_add_form:
            arr.append(field.errors)
            # print(field.errors)
            # print("\n")
        messages.error(request, pic_add_form.errors)
        pic_add_form = PictureAddForm(request.user, request.POST or None, request.FILES or None)

    context = {'pic_add_form': pic_add_form, }

    return render(request, 'darshan/Picture_add.html', context)


@login_required
@user_is_temple_manager
def picture_update(request, s1=None):
    u = []
    sender = get_object_or_404(TempleManager, user=request.user)
    instance = get_object_or_404(Picture, id=s1)
    pic_add_form = PictureAddForm(request.user, request.POST or None, request.FILES or None, instance=instance)
    # print(pic_add_form.instance.Ritual)

    if pic_add_form.is_valid() == True:
        instances = pic_add_form.save(commit=False)
        if instance.is_dirty():  # -----------For Notifying of the update--------------
            dirty_fields = instance.get_dirty_fields()
            # print(dirty_fields)
            for field in dirty_fields:
                if field == "image":
                    user = User.objects.filter(is_superuser=False)
                    for x in user:
                        for y in x.profile.selected:
                            if y == instance.id:
                                u.append(x)
                    # print(u)
                    if not u:
                        recipient = user
                    else:
                        recipient = u
                    notify.send(sender=sender, target=instance, recipient_list=list(recipient), verb="updated")
                    for person in recipient:
                        subject = 'Notification of update'
                        verb = "updated"
                        message = render_to_string('darshan/notification_email.html', {
                            'target': instance, 'verb': verb})
                        person.email_user(subject, message)

        instances.save()
        # print("o")
        return redirect('darshan:manager_profile')
    context = {
        'pic_add_form': pic_add_form,
    }

    return render(request, 'darshan/Picture_add.html', context)


@login_required
@user_is_temple_manager
def picture_remove(request, s1):
    instance = get_object_or_404(Picture, id=s1)
    instance.delete()

    return redirect('darshan:manager_profile')


# --------------For Darshans----------------
@login_required
@user_is_temple_manager
def darshan_add(request):
    temple_manager = get_object_or_404(TempleManager, user=request.user)
    temples = get_object_or_404(Temples, temple2=temple_manager.Temple_Name)
    dar_add_form = DarshanAddForm(request.POST or None)
    if dar_add_form.is_valid():
        instance = dar_add_form.save(commit=False)
        instance.user = request.user
        instance.temple = temples
        instance.save()

        return redirect('darshan:manager_profile')
    else:

        arr = []
        for field in dar_add_form:
            arr.append(field.errors)
            # print(field.errors)
            # print("\n")
        messages.error(request, dar_add_form.errors)
        dar_add_form = DarshanAddForm(request.POST or None)

    context = {'dar_add_form': dar_add_form, }
    return render(request, 'darshan/darshan_add.html', context)


@login_required
@user_is_temple_manager
def darshan_update(request, s2=None):
    instance = get_object_or_404(Darshans, id=s2)
    dar_add_form = DarshanAddForm(request.POST or None, instance=instance)

    if dar_add_form.is_valid() == True:
        instance = dar_add_form.save(commit=False)
        instance.save()
        # print("o")
        return redirect('darshan:manager_profile')

    context = {
        'dar_add_form': dar_add_form, }
    return render(request, 'darshan/darshan_add.html', context)


@login_required
@user_is_temple_manager
def darshan_remove(request, s2):
    instance = get_object_or_404(Darshans, id=s2)
    instance.delete()

    return redirect('darshan:manager_profile')


# ------------FOR PRASAD--------------------------
@login_required
@user_is_temple_manager
def prasad_add(request):
    user = request.user
    temple_manager = get_object_or_404(User, id=user.id)
    manager = get_object_or_404(TempleManager, user=user)
    temples = get_object_or_404(Temples, temple2=manager.Temple_Name)
    item_add_form = PrasadAddForm(request.POST or None, request.FILES or None)
    if item_add_form.is_valid():
        instance = item_add_form.save(commit=False)
        instance.seller = temple_manager
        instance.Temple_Name = temples
        instance.save()

        return redirect('darshan:manager_profile')
    else:
        item_add_form = PrasadAddForm(request.POST or None, request.FILES or None)
        messages.error(request, item_add_form.errors)

    context = {'item_add_form': item_add_form, }

    return render(request, 'shop/item_add.html', context)


@login_required
@user_is_temple_manager
def prasad_update(request, p=None):
    manager = get_object_or_404(TempleManager, user=request.user)
    instance = Product.objects.get(id=p)
    # print(instance.Price)
    item_add_form = PrasadAddForm(request.POST or None, request.FILES or None, instance=instance)

    if item_add_form.is_valid() == True:
        # print("j")
        instances = item_add_form.save(commit=False)

        if instance.is_dirty():
            dirty_fields = instance.get_dirty_fields()
            # print(dirty_fields)
            for field in dirty_fields:
                if field == 'Out_of_Stock' and instance.Out_of_Stock == True:
                    us = []
                    user1 = User.objects.filter(is_superuser=False)
                    user = CartItem.objects.filter(product_id=instance.id)
                    for x in user:
                        users = get_object_or_404(Carts, id=x.cart_id)
                        c = get_object_or_404(User, id=users.user_id)
                        us.append(c)

                    if not us:
                        recipient = user1
                    else:
                        recipient = us
                    notify.send(sender=manager, target=instance, recipient_list=list(recipient), verb="Out of stock")
                    for person in recipient:
                        subject = 'Notification from Divya Kripa:Your Order'
                        verb = "Out of Stock"
                        message = render_to_string('darshan/notification_email.html', {
                            'target': instance, 'verb': verb})
                        person.email_user(subject, message)
                        # send_verification_mail(person.email, message, subject)
                if field == 'Out_of_Stock' and instance.Out_of_Stock == False:
                    us = []
                    user1 = User.objects.filter(is_superuser=False)
                    user = CartItem.objects.filter(product_id=instance.id)
                    for x in user:
                        users = get_object_or_404(Carts, id=x.cart_id)
                        c = get_object_or_404(User, id=users.user_id)
                        us.append(c)

                    if not us:
                        recipient = user1
                    else:
                        recipient = us
                    notify.send(sender=manager, target=instance, recipient_list=list(recipient), verb="Available")
                    for person in recipient:
                        subject = 'Notification from Divya Kripa:Your Order'
                        verb = "Available"
                        message = render_to_string('darshan/notification_email.html', {
                            'target': instance, 'verb': verb})
                        person.email_user(subject, message)
                        #send_verification_mail(person.email, message, subject)

        instances.save()

        # print("o")
        return redirect('darshan:manager_profile')

    context = {
        'item_add_form': item_add_form,
    }

    return render(request, 'shop/item_add.html', context)


@login_required
@user_is_temple_manager
def prasad_remove(request, p):
    # print("fbvbf")
    instance = get_object_or_404(Product, id=p)
    # print(instance)
    instance.delete()

    return redirect('darshan:manager_profile')
