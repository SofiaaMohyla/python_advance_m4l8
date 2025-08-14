from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Article
from .forms import ArticleForm, ArticleFilterForm
from .mixins import UserIsOwnerMixin

class ArticleListView(ListView):
    model = Article
    template_name = "news/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        qs = Article.objects.all()
        q = self.request.GET.get("q") or ""
        status = self.request.GET.get("status") or ""
        priority = self.request.GET.get("priority") or ""
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs.select_related("author")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = ArticleFilterForm(self.request.GET or None)
        return ctx

class ArticleDetailView(DetailView):
    model = Article
    template_name = "news/article_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "news/article_form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("news:article_detail", kwargs={"slug": self.object.slug})

class ArticleUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "news/article_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get_success_url(self):
        return reverse_lazy("news:article_detail", kwargs={"slug": self.object.slug})

class ArticleDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Article
    template_name = "news/article_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("news:article_list")
