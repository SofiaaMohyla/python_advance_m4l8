from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "slug", "content", "status", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }

class ArticleFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "пошук"}))
    status = forms.ChoiceField(required=False, choices=[("", "Будь-який")] + list(Article.Status.choices), widget=forms.Select(attrs={"class": "form-select"}))
    priority = forms.ChoiceField(required=False, choices=[("", "Будь-який")] + [(p.value, p.label) for p in Article.Priority], widget=forms.Select(attrs={"class": "form-select"}))
