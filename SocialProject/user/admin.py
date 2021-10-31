from django.contrib import admin
from .models import User,Profile,Post
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserAdminCreationForm

    list_display = ('phone','name','email','admin',)
    list_filter = ('staff','active' ,'admin', )
    fieldsets = (
        (None, {'fields': ('phone','name','email', 'password')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','name','email', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone','name')
    ordering = ('phone','name')
    filter_horizontal = ()


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Post)