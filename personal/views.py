from django.shortcuts import render, redirect, get_object_or_404
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import random
from blog.views import get_blog_queryset
from blog.models import BlogPost
from userads.models import ad
# Create your views here.

BLOG_POSTS_PER_PAGE = 10

def home_screen_view(request):

	context = {}

	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	

	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
		
	ads = list(ad.objects.all())
	#print(ads)
	random_ad = random.choice(ads)
	random_random_ad = random.choice(ads)
	context['blog_posts'] = blog_posts
	context['random_ad'] = random_ad
	context['random_random_ad'] = random_random_ad
	

	return render(request, "personal/home.html", context)

	#return render(request,"personal/home.html", {'ads': random_ad})
	

	