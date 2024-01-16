from django.contrib import admin
from .models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # You can customize these forms if you have added additional fields to CustomUser
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birth_date', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overrides get_fieldsets to use this attribute
    # when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'birth_date')}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_preferences', 'get_wishlist', 'get_shopping_history')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('wishlist', 'shopping_history')

    def get_preferences(self, obj):
        return obj.preferences

    get_preferences.short_description = 'Preferences'

    def get_wishlist(self, obj):
        return ", ".join([product.name for product in obj.wishlist.all()])

    get_wishlist.short_description = 'Wishlist'

    def get_shopping_history(self, obj):
        return ", ".join([f"Order {order.id}" for order in obj.shopping_history.all()])

    get_shopping_history.short_description = 'Shopping History'
