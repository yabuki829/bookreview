from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import User,Profile,Book,Review,Poll,Vote,Choice,Category,Blog,Tag,BlogComment

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ()}),
        (
            ('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(BlogComment)
admin.site.register(Vote)


