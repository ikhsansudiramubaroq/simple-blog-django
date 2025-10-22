# Catatan Model User Kustom Django

## Deskripsi
Model ini digunakan untuk membuat sistem login menggunakan email sebagai username.  
Menggunakan `AbstractBaseUser` untuk fleksibilitas dan `PermissionsMixin` untuk dukungan izin.

---

## Struktur
- **UserManager**
  - untuk mengelola user biasa dan admin
  - `create_user()` → Membuat user biasa.
    - tidak ada password karna user mengisi form, dan fungsi form.save() itu menyimpan password
  - `create_superuser()` → Membuat user dengan semua hak akses. (user admin)
    - ada password karena create_user memerlukan password yang sudah diisi di terminal
  
- **User**
  - Class User : untuk field utama user biasa dan admin (custom)
  - Field utama:
    - `nama` → Nama lengkap user.
    - `email` → Digunakan sebagai username.
    - `tgl_lahir` → Default ke tanggal saat ini.
    - `img_user` → Foto profil user.
  - `USERNAME_FIELD` → Mengatur login menggunakan email.
  - `REQUIRED_FIELDS` → Field wajib selain `USERNAME_FIELD`.

---

## Dokumentasi & Pencarian di Django Docs
| Fungsi / Bagian      | Link Dokumentasi | Kata Kunci Pencarian |
|----------------------|------------------|----------------------|
| AbstractBaseUser     | https://docs.djangoproject.com/en/stable/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project | "django custom user model" |
| BaseUserManager      | https://docs.djangoproject.com/en/stable/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model | "django baseusermanager" |
| PermissionsMixin     | https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.PermissionsMixin | "django permissionsmixin" |
| models.Model         | https://docs.djangoproject.com/en/stable/ref/models/class/ | "django model field types" |
| ImageField           | https://docs.djangoproject.com/en/stable/ref/models/fields/#imagefield | "django imagefield upload_to" |
| timezone.now         | https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.timezone.now | "django timezone.now default" |

---

## Tips
- Dokumentasi detail simpan di file `.md` untuk memudahkan tim.
- Pastikan `AUTH_USER_MODEL` di `settings.py` diarahkan ke model ini.

# Catatan Views

## 1. LogoutView
**Tujuan**  
Melakukan logout user yang sedang login dan mengarahkan kembali ke halaman index blog.

**Alur**  
1. Panggil fungsi `logout(request)` dari Django untuk menghapus session user.
2. Redirect user ke URL bernama `blog:index`.

---

## 2. register_users
**Tujuan**  
Mendaftarkan user baru menggunakan form kustom `RegisterUserForm`.

**Alur**  
1. **Jika request POST:**
   - Ambil data dari `RegisterUserForm` menggunakan `request.POST`.
   - Validasi form (`form.is_valid()`).
   - Jika valid, simpan user baru ke database (`form.save()`).
   - Redirect ke halaman login (`account:login`).
2. **Jika request GET:**
   - Tampilkan form kosong untuk registrasi.
3. Kirim `form` dan `title` ke template `registration/daftar.html`.

---

## Catatan Tambahan
- `redirect()` digunakan untuk mengarahkan ke URL berdasarkan **name** di `urls.py`.
- Semua user yang mendaftar lewat `register_users` akan menggunakan model user yang terhubung di `settings.AUTH_USER_MODEL`.
- `logout()` adalah fungsi bawaan Django yang tidak memerlukan parameter tambahan selain `request`.

# Catatan Konfigurasi Admin Django

## 1. Import
- `admin` → Modul untuk mengelola model di Django Admin.
- `BaseUserAdmin` → Kelas bawaan Django yang digunakan sebagai dasar untuk mengelola user.
- `User` → Model kustom yang menggantikan model user bawaan Django.

## 2. Kelas `UserAdmin`
- **ordering**: Mengatur urutan data berdasarkan `email`.
- **list_display**: Menentukan kolom yang muncul di tabel daftar user.

## 3. Fieldsets
- **(None)**: Menampilkan `email` dan `password`.
- **"Personal Info"**: Menampilkan data pribadi user (`nama`, `tempat_lahir`, `tgl_lahir`, `no_hp`, `img_user`).
- **"Permission"**: Mengatur hak akses user (`groups`, `is_active`, `is_staff`, `is_superuser`).

## 4. Add Fieldsets
- Digunakan untuk form penambahan user baru.
- `classes = ('wide',)`: Membuat form lebih lebar.
- Field yang digunakan: `nama`, `email`, `no_hp`, `password1`, `password2`.

## 5. Registrasi Model
- `admin.site.register(User, UserAdmin)`: Mendaftarkan model ke admin dengan konfigurasi yang sudah dibuat.


# Catatan Penjelasan View Account (Logout & Register)


- render = untuk menampilkan template HTML, redirect = untuk memindahkan user ke halaman lain
- from django.contrib.auth import logout         # Fungsi bawaan Django untuk menghapus sesi login (logout user)
- from .forms import RegisterUserForm            # Mengimpor form registrasi kustom dari file forms.py

## View untuk logout user
def LogoutView(request):                       # Membuat fungsi view bernama LogoutView yang menerima request
    logout(request)                            # Menghapus sesi login pengguna yang sedang aktif
    return redirect('blog:index')              # Setelah logout, pengguna diarahkan ke halaman index dari aplikasi blog

# View untuk registrasi user baru
def register_users(request):                   # Membuat fungsi view bernama register_users untuk menangani registrasi
    if request.method == 'POST':               # Mengecek apakah permintaan dari form menggunakan metode POST (form dikirimkan)
        form = RegisterUserForm(request.POST or None)  # Membuat objek form dengan data yang dikirim user, atau None jika tidak ada
        if form.is_valid():                    # Mengecek apakah semua input dari form valid sesuai aturan yang sudah dibuat
            form.save()                        # Menyimpan data user baru ke dalam database
            return redirect('account:login')   # Setelah registrasi berhasil, arahkan user ke halaman login
    else:                                       # Jika request bukan POST (misalnya GET)
        form = RegisterUserForm()              # Membuat objek form kosong untuk ditampilkan di halaman

    context = {                                # Membuat dictionary untuk data yang akan dikirim ke template HTML
        'title': 'Register User',              # Judul halaman
        'form': form,                          # Objek form yang akan ditampilkan di template
    }

    return render(request, 'registration/daftar.html', context)  # Menampilkan template daftar.html dengan data context

