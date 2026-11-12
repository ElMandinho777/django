from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'telefono')

class ChangeUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    list_display = ('email', 'username', 'telefono', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'telefono')
    fieldsets = UserAdmin.fieldsets + (('Contacto', {'fields': ('telefono',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Contacto', {'fields': ('email', 'telefono')}),)
