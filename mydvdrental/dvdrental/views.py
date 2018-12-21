import os
import string

from django.shortcuts import render

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import connection
cursor = connection.cursor()


# Create your views here.

def index(request):
    cursor.execute("""SELECT count(film_id)
        FROM public.film WHERE description iLIKE '%croc%' AND description iLIKE '%shark%'; """)
    count = cursor.fetchall()
    print("====", count)
    cursor.execute(
        """select custor.first_name, custor.last_name
        from (select first_name, last_name
            from public.customer as cust
            union
            select first_name, last_name
            from public.actor as act) custor
        where custor.first_name = (select first_name from actor where actor_id=8)
        """
    )
    users = cursor.fetchall()
    print("====", users)
    cursor.execute("""select cat.name, count(film_cat.film_id)
        from public.film_category as film_cat
        inner join public.category as cat
        ON film_cat.category_id = cat.category_id
        inner join public.film as fil
        ON film_cat.film_id = fil.film_id
        group by cat.name having count(*) BETWEEN 55 AND 65
        order by count(film_cat.film_id) """)
    films = cursor.fetchall()
    print("====", films)
    page = request.GET.get('page', 1)
    paginator = Paginator(films, 4)
    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        films = paginator.page(1)
    except EmptyPage:
        films = paginator.page(paginator.num_pages)

    return render(request, '../templates/index.html', {'users': users, 'films': films,
                                                        'count': count})

def add_film(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        year = request.POST.get('year')
        language = request.POST.get('language')
        language_value = cur.execute("select language_id from public.language where name = (%s)", [language])
        language_id = cur.fetchall()
        duration = request.POST.get('duration')
        rate = request.POST.get('rate')
        length = request.POST.get('length')
        cost = request.POST.get('cost')
        rating = request.POST.get('rating')
        cursor.execute(
            """INSERT INTO public.film (
        title, description ,release_year ,language_id, rental_duration, rental_rate, length,replacement_cost,rating)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
            title, description, year, language_id[0], duration, rate, length, cost, rating)
        )
        connection.commit()
    csrf_token = generate_token()
    print("----------", csrf_token)
    return render(request, '../templates/films.html', {'csrf_token': csrf_token})


def generate_token():
    alphabet = string.ascii_lowercase + string.digits
    alphabet_len = len(alphabet)
    return ''.join(alphabet[b % alphabet_len] for b in os.urandom(7))

