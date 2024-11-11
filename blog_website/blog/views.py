from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User


# Use the @login_required decorator to restrict access to authenticated users
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Category

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        photo = request.FILES.get('photo')  # Get the uploaded file
        category_id = request.POST.get('category')  # Get the selected category ID

        # Handle the case where the category ID is not valid
        try:
            category = Category.objects.get(id=category_id) if category_id else None
        except ObjectDoesNotExist:
            category = None  # Or you can redirect with an error message

        # Create a new blog post with the current user as the author, and assign photo and category
        blog = Blog.objects.create(
            title=title,
            content=content,
            author=request.user,
            photo=photo,
            category=category
        )

        return redirect('index')  # Redirect to the homepage or blog list page
    else:
        categories = Category.objects.all()  # Get all categories for the dropdown
        return render(request, 'create_blog.html', {'categories': categories})




@login_required
def edit_blog(request, blog_id):
    # Fetch the blog by ID, or return 404 if not found
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    
    if request.method == 'POST':
        # Update blog fields with new data from the form
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        photo = request.FILES.get('photo')  # Get the uploaded photo (if any)
        category_id = request.POST.get('category')  # Get the selected category ID
        
        # Get the category object if category ID exists
        category = Category.objects.get(id=category_id) if category_id else None
        
        # Update the fields, including the photo and category if available
        blog.photo = photo if photo else blog.photo  # Keep the current photo if no new one is uploaded
        blog.category = category if category else blog.category  # Keep the current category if no new one is selected
        blog.save()
        
        return redirect('index')  # Redirect to the homepage or blog list page after updating the blog
    else:
        # Fetch all categories for the dropdown
        categories = Category.objects.all()
        
        return render(request, 'update_blog.html', {'blog': blog, 'categories': categories})
    

@login_required
def my_blog(request):
    # Fetch all blog posts by the current user
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'myblog.html', {'blogs': blogs})


def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == "POST" and request.user.is_authenticated:
        # Ensure the user is authenticated before allowing comment submission
        comment_text = request.POST.get('comment_text')
        if comment_text:
            # Create a new comment with the current user's username
            Comment.objects.create(
                blog=blog,
                username=request.user.username,  # Store the logged-in user's username
                text=comment_text
            )
        return redirect('view_blog', blog_id=blog.id)

    # Fetch all comments for the blog
    comments = blog.comments.all()
    
    return render(request, 'view_blog.html', {'blog': blog, 'comments': comments})



@login_required
def delete_blog(request, blog_id):

    author = request.user
    if(not author):
        return redirect('index')

    # Fetch blog by ID or return 404 if not found
    blog = get_object_or_404(Blog, id=blog_id,author=author)
    
    # Ensure that the logged-in user is the author of the blog
    if blog.author != request.user:
        return redirect('index')  # Redirect to index if the user is not the author
    
    # Delete the blog entry
    blog.delete()
    
    return redirect('index')  # Redirect to the homepage


def index(request):
    # Get all blog posts
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Get the username and email from the form
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error("username", "Username is already taken.")

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Email is already registered.")

            # If there are no errors, save the user and log them in
            if not form.errors:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])  # This is crucial
                user.save()  # Save the user to the database
                return redirect('index')  # Redirect to the homepage or another page

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Try to fetch the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            # If user exists, authenticate with password
            if user and user.check_password(password):
                login(request, user)
                return redirect('index')  # Redirect to the homepage after successful login
            else:
                form.add_error(None, "Invalid credentials")  # Add error if authentication fails

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_comment(request, blog_id):
    blog = Blog.objects.get(id=blog_id)  # Get the specific blog for which the comment is being added
    if request.method == 'POST':
        text = request.POST.get('text')  # Get the comment text from the form
        # Create the comment and associate it with the logged-in user
        Comment.objects.create(
            blog=blog,
            user=request.user,  # Store the currently logged-in user
            text=text
        )
        return redirect('view_blog', blog_id=blog.id)  # Redirect to the blog detail page after commenting
    return render(request, 'add_comment.html', {'blog': blog})  # Show the comment form
