from django.contrib import admin
from app.detective.models import QuoteRequest, Topic, RelationshipSearch, Article

class QuoteRequestAdmin(admin.ModelAdmin):
    list_filter = ("employer", "records", "users", "public", )
    search_fields = ("name", "employer", "domain", "email", "comment",)

admin.site.register(QuoteRequest, QuoteRequestAdmin)

class RelationshipSearchInline(admin.TabularInline):
    model = RelationshipSearch
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "link", "public", )

    def save_model(self, request, obj, form, change):
        super(TopicAdmin, self).save_model(request, obj, form, change)
        if obj.author is None: obj.author = request.user
        obj.save()

admin.site.register(Topic, TopicAdmin)

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "link", "created_at", "public", )

admin.site.register(Article, ArticleAdmin)