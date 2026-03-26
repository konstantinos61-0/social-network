from django import forms

from .models import Post




class PartialPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        labels = {
            "text": ""
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "placeholder": "Post Text",
                "class": "form-control"
            })
        }