# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.lock.forms import SearchForm
from apps.lock.models import Item, LockAdmin
from apps.syjon.lib.functions import utf2ascii
from apps.syjon.lib.pdf import render_to_pdf
from apps.trainman.models import Department, UserProfile

TEMPLATE_ROOT = "lock/"

@login_required
def index(request):
    institute_of_computer_science = get_object_or_404(Department, name__iexact = 'Instytut Informatyki')
    if request.user.userprofile.is_in_department(institute_of_computer_science):
        # Pobranie danych do wyszukiwania z sesji
        query_string = request.session.get('query_string','')
        user_initial = request.session.get('user_initial', request.user.userprofile) # Jeżeli w formularzu wyszukiwania nie został wybrany użytkownik zostaną wyświetlone wszystkie przedmioty zalogowanego użytkownika
        
        # Ustalenie listy pozycji w polu użytkowników formularza wyszukiwania
        try: # Użytkownik jest administratorem
            departments = []
            for department in request.user.userprofile.lockadmin.departments.all():
                departments += department.children()
            user_list = UserProfile.objects.filter(department__in = departments)
        except LockAdmin.DoesNotExist: # Użytkownik nie jest administratorem
            user_list = UserProfile.objects.filter(id = request.user.userprofile.id)
        
        # Formularz wyszukiwania        
        form = SearchForm(request.POST or None, initial={'query': query_string, 'user': user_initial}, queryset=user_list)
        
        # Zawężenie wyświetlanych przedmiotów do opcjami wyszukiwania
        if request.method == "POST":
            if form.is_valid():
                
                query_string = form.cleaned_data['query']
                request.session['query_string'] = query_string
                user_initial = form.cleaned_data['user']
                request.session['user_initial'] = user_initial
      
                messages.success(request, "Wyszukiwanie zostało zakończone.")
            else:
                messages.error(request, "Wystąpił błąd podczas wyszukiwania.")
        
        # Zbudowanie zapytania pobierającego przedmioty do wyświetlenia
        if query_string != '':
            query_set = Q(name__istartswith = query_string) | Q(serial_number__istartswith = query_string) | Q(inventory_number__istartswith = query_string) | Q(type__name__istartswith = query_string) | Q(room__name__istartswith = query_string)
        else:
            query_set = Q()
        query_set &= Q(users = user_initial) if user_initial else Q(users__in = user_list)
        
        # Popbranie przedmiotów do wyświetlenia
        items = Item.objects.filter(query_set).distinct()
        
        # Paginacja
        paginator = Paginator(items, 20)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
            
        try:
            items = paginator.page(page)
        except (EmptyPage, InvalidPage):
            items = paginator.page(paginator.num_pages) 
        
        kwargs = {'items': items, 'form': form}
    else:
        kwargs = {}
    return render(request, TEMPLATE_ROOT+'base.html', kwargs)

@login_required
def show_item(request, id_item):
    item = get_object_or_404(Item, id = id_item)
    kwargs = {'item': item}
    return render(request, TEMPLATE_ROOT+'show_item.html', kwargs)

@login_required
def print_receipt(request, id_item):
    item = get_object_or_404(Item, id = id_item)
    template_path = TEMPLATE_ROOT+'print_receipt.html'
    file_name = utf2ascii(str(item.name))
    template_context = {'item': item}
    return render_to_pdf(request, template_path, template_context, file_name)
