# -*- coding: utf-8 -*-

from django import template

register = template.Library()

from apps.syjon.templatetags.params import get_parameters_string

LEADING_PAGE_RANGE_DISPLAYED = 8  # Liczba stron wyświetalnych na początku listy jeżeli aktywna strona znajduje się w początkowym zasięgu.
TRAILING_PAGE_RANGE_DISPLAYED = 8  # Liczba stron wyświetalnych na końcu listy jeżeli aktywna strona znajduje się w końcowym zasięgu.
LEADING_PAGE_RANGE = 8  # Liczba stron na początku listy po przekroczeniu których paginacja zaczyna wyświetlać się w trzech częściach.
TRAILING_PAGE_RANGE = 8  # Liczba stron na końcu listy po przekroczeniu których paginacja zaczyna wyświetlać się w trzech częściach.
NUM_PAGES_OUTSIDE_RANGE = 2 # Liczba stron wyświetlanych poza zasięgiem aktywnej strony.
ADJACENT_PAGES = 4  # Liczba stron wyświetlanych w sąsiedztwie aktywnej strony.

@register.inclusion_tag('metacortex/templatetags/paginator.html')
def paginator(request, page):
    
    in_leading_range = False # Czy aktywna strona znajduje się na początku listy.
    in_trailing_range = False # Czy aktywna strona znajduje się na końcu listy.
    pages_outside_leading_range = range(0) # Zakres stron wyświetalnych na początku listy.
    pages_outside_trailing_range = range(0) # Zakres stron wyświetalnych na końcu listy.
    
    pages = page.paginator.num_pages # Liczba wszystkich stron.
    if pages <= LEADING_PAGE_RANGE_DISPLAYED: # Wszystkich stron jest mniej niż stron wyświetlanych na początku.
        in_leading_range = in_trailing_range = True
        page_numbers = [n for n in range(1, pages + 1) if n > 0 and n <= pages]
    elif page.number <= LEADING_PAGE_RANGE: # Aktywna strona znajduje się w stronach wyświetlanych na poczatku.
        in_leading_range = True
        page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= pages]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif page.number > pages - TRAILING_PAGE_RANGE: # Aktywna strona znajduje się w stronach wyświetlanych na końcu.
        in_trailing_range = True
        page_numbers = [n for n in range(pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, pages + 1) if n > 0 and n <= pages]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: # Aktywna strona znajduje się poza stronami wyswietlanymi na początku i końcu.
        page_numbers = [n for n in range(page.number - ADJACENT_PAGES, page.number + ADJACENT_PAGES + 1) if n > 0 and n <= pages]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

    params = get_parameters_string(request, 'page')
    return {'page': page,
            'in_leading_range' : in_leading_range,
            'in_trailing_range' : in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'pages_outside_trailing_range': pages_outside_trailing_range,
            'page_numbers': page_numbers,
            'params': params
            }