from django import forms
from django.core.exceptions import ValidationError
from .models import BlogPost, AboutRating, AboutComment, Contact
from django.core.files.uploadedfile import UploadedFile

# ----- BlogPostForm -----
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'image', 'excerpt', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if isinstance(image, UploadedFile):
                max_size = 2 * 1024 * 1024  # 2MB limit
                if image.size > max_size:
                    raise ValidationError("Image file too large ( > 2MB )")

                valid_mime_types = ['image/jpeg', 'image/png']
                if image.content_type not in valid_mime_types:
                    raise ValidationError("Unsupported image type. Only JPEG and PNG are allowed.")
            else:
                raise ValidationError("Invalid image upload.")
        return image
# ----- BlogPostForm -----

# ----- AboutRatingForm -----
class AboutRatingForm(forms.ModelForm):
    class Meta:
        model = AboutRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'class': 'form-control'}),
        }
# ----- AboutRatingForm -----

# ----- AboutCommentForm -----
class AboutCommentForm(forms.ModelForm):
    class Meta:
        model = AboutComment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment'}),
        }
# ----- AboutCommentForm -----

# ----- ContactForm -----
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
# ----- ContactForm -----
