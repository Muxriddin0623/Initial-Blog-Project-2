from .models import Post, Comment, Category
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.utils.timezone import now, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post

def home(request):
    posts = Post.objects.filter(is_approved=True).order_by('-created_at')
    # Eng ko'p ko'rilgan postlar
    most_viewed = posts.order_by('-views')[:5]

    # Haftaning eng ommabop postlari
    week_ago = now() - timedelta(days=7)
    weekly_popular = posts.filter(is_approved=True, created_at__gte=week_ago).annotate(view_count=Count('views')).order_by('-views')[:5]

    # Oyning eng ommabop postlari
    month_ago = now() - timedelta(days=30)
    monthly_popular = posts.filter(is_approved=True, created_at__gte=month_ago).annotate(view_count=Count('views')).order_by('-views')[:5]

    # Tavsiya qilingan postlar
    recommended_posts = posts.filter(is_approved=True, recommended=True)[:5]

    latest_posts = Post.objects.filter(is_approved=True).order_by('-created_at')[:5]
    unapproved_count = Post.objects.filter(is_approved=False).count() if request.user.is_staff else 0

    context = {
        'posts': posts,
        'most_viewed': most_viewed,
        'weekly_popular': weekly_popular,
        'monthly_popular': monthly_popular,
        'recommended_posts': recommended_posts,
        'latest_posts': latest_posts,
        'unapproved_count': unapproved_count,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('image')
        tags = request.POST.get('tags')
        post = Post.objects.create(
            title=title, content=content, category=category,
            author=request.user, image=image, tags=tags
        )
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'blog/new_post.html', {'categories': categories})

@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', pk=post.pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Foydalanuvchini ro'yxatdan o'tgandan keyin avtomatik kirish
            return redirect('home')  # Bosh sahifaga qaytaradi
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

# Logout funksiyasi
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@staff_member_required
def pending_posts(request):
    posts = Post.objects.filter(is_approved=False)
    context = {'posts': posts}
    return render(request, 'blog/pending_posts.html', context)

@staff_member_required
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_approved = True
    post.save()
    messages.success(request, f'Post "{post.title}" has been approved.')
    return redirect('pending_posts')