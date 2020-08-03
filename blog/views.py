from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from PIL import Image

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form 


	return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, slug):
	blog_post = get_object_or_404(BlogPost, slug=slug)
	#comments = Comment.objects.filter_by_instance(blog_post)
	
	initial_data = {
					"content_type": blog_post.get_content_type,
					'object_id': blog_post.id
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get_for_model(BlogPost)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
									user = request.user,
									content_type= content_type,
									object_id= obj_id,
									content = content_data									
								)
		


	comments = blog_post.comments
	context = {
		'comments': comments,
		'comment_form': form,
	}

	
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of this post,therefore, you cannot edit it.")
	if blog_post.image == None:
		blog_post.image == Image.open("static/logo.png")
	else:
		blog_post.image == blog_post.image
	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Thanks, your edits have been updated!"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,

			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)



def get_blog_queryset(query=None):
	queryset= []
	queries = query.split(" ") #[Bexley, Grammar. School]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))

