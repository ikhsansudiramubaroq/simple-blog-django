from django.contrib import admin
# Import modul admin bawaan Django untuk mengelola model di panel admin.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Import kelas UserAdmin bawaan Django, yang nantinya akan kita override untuk menyesuaikan model User kustom.

from .models import User
# Import model User kustom yang telah kita buat.

# Membuat class UserAdmin yang mewarisi BaseUserAdmin.
class UserAdmin(BaseUserAdmin):
    ordering = ['email']  
    # Mengatur urutan default data user di admin berdasarkan email.
    
    list_display = ['email', 'nama', 'is_active', 'is_admin']  
    # Menentukan kolom yang akan ditampilkan di daftar user pada panel admin.

    # fieldsets digunakan untuk mengatur tampilan form edit user di admin.
    fieldsets = (
        (None, {
            "fields": (
                ['email', 'password']  
                # Bagian pertama menampilkan field email & password.
            ),
        }),
        ("Personal Info", {
            "fields": (
                ['nama', 'tempat_lahir', 'tgl_lahir', 'no_hp', 'img_user']  
                # Bagian "Personal Info" menampilkan informasi pribadi user.
            ),
        }),
        ("Permission", {
            "fields": (
                ['groups', 'is_active', 'is_staff', 'is_superuser']  
                # Bagian "Permission" untuk mengatur hak akses user.
            ),
        }),
    )

    # add_fieldsets digunakan untuk mengatur form tambah user baru di admin.
    add_fieldsets = [
        (
            None,
            {
                'classes': ('wide',),  # Menambahkan class CSS bawaan untuk memperlebar form.
                'fields': ['nama', 'email', 'no_hp', 'password1', 'password2' ]  
                # Field yang diperlukan saat membuat user baru.
            }
        )
    ]
    
# Mendaftarkan model User dengan konfigurasi UserAdmin ke panel admin.
admin.site.register(User, UserAdmin)
