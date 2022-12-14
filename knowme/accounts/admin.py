from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from knowme.accounts.models import KnowMeUser, Profile


@admin.register(KnowMeUser)
class AppUserAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = KnowMeUser
    list_display = ('username', 'email', 'is_staff')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('email',)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','first_name', 'last_name', 'picture', 'gender']

