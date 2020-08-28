from django.shortcuts import render, redirect, get_object_or_404
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import random
from blog.views import get_blog_queryset
from blog.models import BlogPost
from userads.models import ad

from django.template import RequestContext
# Create your views here.

BLOG_POSTS_PER_PAGE = 6

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
	thequery = "issue"
	posts = list(get_blog_queryset(thequery))
	#print(posts)
	#print(ads)
	random_ad1 = random.choice(ads)
	random_ad2 = random.choice(ads)
	random_ad3 = random.choice(ads)
	random_ad4 = random.choice(ads)
	random_ad5 = random.choice(ads)
	random_ad6 = random.choice(ads)
	random_ad7 = random.choice(ads)
	random_ad8 = random.choice(ads)
	random_ad9 = random.choice(ads)
	random_ad10 = random.choice(ads)
	random_random_ad = random.choice(ads)
	random_post = random.choice(posts)

	context['random_post'] = random_post
	context['blog_posts'] = blog_posts
	context['random_ad1'] = random_ad1
	context['random_ad2'] = random_ad2
	context['random_ad3'] = random_ad3
	context['random_ad4'] = random_ad4
	context['random_ad5'] = random_ad5
	context['random_ad6'] = random_ad6
	context['random_ad7'] = random_ad7
	context['random_ad8'] = random_ad8
	context['random_ad9'] = random_ad9
	context['random_ad10'] = random_ad10
	context['random_random_ad'] = random_random_ad
	

	return render(request, "personal/home.html", context)

	#return render(request,"personal/home.html", {'ads': random_ad})
def handler404(request, exception):
    return render(request, '404.html')
def handler500(request, *args, **argv):
	return render(request, '500.html')

	

	
