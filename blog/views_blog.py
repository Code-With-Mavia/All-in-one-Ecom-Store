from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.views.decorators.http import require_POST
from .models import BlogPost, Tag, AboutRating, AboutComment
from .forms import BlogPostForm, AboutRatingForm, AboutCommentForm

# ----- blog_home -----
def blog_home(request):
    posts = BlogPost.objects.all()
    return render(request, "blog/index.html", {"posts": posts})
# ----- blog_home -----

# ----- blog_post_detail -----
def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    comments = post.comments.all()
    rating_form = AboutRatingForm()
    comment_form = AboutCommentForm()
    context = {
        "post": post,
        "avg_rating": round(avg_rating, 2),
        "comments": comments,
        "rating_form": rating_form,
        "comment_form": comment_form,
    }
    return render(request, "blog/detail.html", context)
# ----- blog_post_detail -----

# ----- blog_posts_by_tag -----
def blog_posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.blog_posts.all()
    return render(request, "blog/index.html", {"posts": posts, "tag": tag})
# ----- blog_posts_by_tag -----

# ----- blog_about -----
def blog_about(request):
    ratings = AboutRating.objects.all()
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    comments = AboutComment.objects.all()

    rating_form = AboutRatingForm()
    comment_form = AboutCommentForm()

    if request.method == 'POST':
        if 'rating_submit' in request.POST:
            rating_form = AboutRatingForm(request.POST)
            if rating_form.is_valid():
                rating_form.save()
                return redirect('blog_about')
        elif 'comment_submit' in request.POST:
            comment_form = AboutCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.save()
                return redirect('blog_about')

    context = {
        'avg_rating': round(avg_rating, 2),
        'rating_form': rating_form,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'blog/about.html', context)
# ----- blog_about -----

# ----- blog_post_create -----
def blog_post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect("blog_post_detail", slug=post.slug)
    else:
        form = BlogPostForm()
    return render(request, "blog/create.html", {"form": form})
# ----- blog_post_create -----

# ----- blog_post_edit -----
def blog_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if 'image_delete' in request.POST and post.image:
                post.image.delete(save=False)
                post.image = None
            post = form.save()
            return redirect("blog_post_detail", slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    return render(request, "blog/edit.html", {"form": form, "post": post})
# ----- blog_post_edit -----

# ----- blog_post_delete -----
def blog_post_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.delete()
    return redirect("blog_home")
# ----- blog_post_delete -----

# ----- blog_contact -----
def blog_contact(request):
    return render(request, "blog/contact.html")
# ----- blog_contact -----

# ----- add_rating -----
@require_POST
def add_rating(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    form = AboutRatingForm(request.POST)
    if form.is_valid():
        rating = form.save(commit=False)
        rating.blog_post = post
        rating.save()
    return redirect('blog_post_detail', slug=slug)
# ----- add_rating -----

# ----- add_comment -----
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    form = AboutCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.blog_post = post
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = request.user.get_full_name() or request.user.username
            comment.email = request.user.email
        comment.save()
    return redirect('blog_post_detail', slug=slug)
# ----- add_comment -----
