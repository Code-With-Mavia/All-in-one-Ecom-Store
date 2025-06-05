from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

# ----- Tag Model -----
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
# ----- Tag Model -----

# ----- BlogPost Model -----
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    excerpt = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug})
# ----- BlogPost Model -----

# ----- AboutRating Model -----
class AboutRating(models.Model):
    blog_post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='ratings',
        null=True, blank=True
    )
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        blog_post_title = self.blog_post.title if self.blog_post else "No Post"
        return f"Rating: {self.rating} for {blog_post_title}"
# ----- AboutRating Model -----

# ----- AboutComment Model -----
class AboutComment(models.Model):
    blog_post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments',
        null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='comments'
    )
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username} on {self.date_posted.strftime('%Y-%m-%d')}"
        return f"Comment by {self.name or 'Guest'} on {self.date_posted.strftime('%Y-%m-%d')}"
# ----- AboutComment Model -----

# ----- Customer Model -----
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"
# ----- Customer Model -----

# ----- Contact Model -----
class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"
# ----- Contact Model -----
