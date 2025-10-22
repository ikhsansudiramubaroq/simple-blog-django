from django.db import models
# Mengimpor kelas model Django untuk membuat tabel database

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# AbstractBaseUser -> digunakan untuk membuat model user kustom
# BaseUserManager -> untuk mengelola pembuatan user & superuser
# PermissionsMixin -> untuk menambahkan fitur izin dan grup

from django.utils import timezone
# timezone -> untuk mengatur default tanggal sesuai zona waktu

# Manajer kustom untuk mengelola model User Admin dan user Biasa
# Manajer ini mengelola pembuatan user dan superuser
# usercreationform -> form bawaan Django untuk registrasi user memanggil usermanager fungsi def create_user
# createsuperuser -> membuat user diterminal untuk membuat superuser memanggil def create_superuser

# default-nya, Django memakai model User dari django.contrib.auth.models.User, yang pakai username sebagai identitas utama.
# kalau kamu ingin pakai email sebagai login utama, kamu harus override model bawaan Django dengan membuat model sendiri yang mewarisi AbstractBaseUser dan PermissionsMixin.
# nah, model baru ini butuh manager custom — yaitu UserManager — supaya Django tahu cara membuat user dan superuser.
# bikin model User custom, harus beri tahu Django lewat:settings.py pada fungsi AUTH_USER_MODEL = 'account.User'

class UserManager(BaseUserManager):
    def create_user(self, email, nama, password):
        # Membuat user biasa (bukan admin) dengan email & nama
        
        # Pastikan email diisi
        if not email:
            raise ValueError('Pengguna harus memiliki alamat Email')
        
        # Pastikan nama diisi
        if not nama:
            raise ValueError('Nama harus diisi')
        
        # Buat instance user berdasarkan class User
        # dipakai buat bikin instance awal dari model user yang merupakan field inti dari membuat user
        # model User yang akan di definisikan karna terdapat objects=UserManager di class user
        # belum disimpan ke database — baru “dipegang di memori”.
        user = self.model(
            email=self.normalize_email(email), # Normalisasi email (misal huruf kecil semua)
            nama=nama
        )
        
        # Simpan password dalam bentuk hash (bukan teks asli)
        user.set_password(password)
        
        # Simpan user ke database menggunakan koneksi otomatis menunjuk ke database default Django
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, nama, password):
        # Membuat superuser (admin penuh) berdasarkan create_user
        # dipanggil otomatis saat kamu buat superuser di terminal
        
        # memanggil create_user() biar tidak duplikasi kode.
        # Buat user biasa dulu
        user = self.create_user(
            email, 
            password=password,
            nama=nama, 
        )
        
        # Tambahkan hak akses admin
        user.is_admin = True       # Menandakan user adalah admin (custom field)
        user.is_staff = True       # Agar bisa akses Django Admin
        user.is_superuser = True   # Semua hak tanpa batas
        
        # Simpan perubahan hak akses ke database menggunakan koneksi otomatis menunjuk ke database default Django
        user.save(using=self._db)
        
        return user


# Model User kustom mewarisi abstractuser
class User(AbstractBaseUser, PermissionsMixin):
    nama = models.CharField(max_length=75)
    tempat_lahir = models.CharField(max_length=75)
    tgl_lahir = models.DateField(blank=True, default=timezone.now)
    email = models.EmailField(unique=True, blank=True)
    no_hp = models.IntegerField(blank=True, null=True)
    img_user = models.ImageField(upload_to='user/', default='profile.jpg', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # objects = UserManager() artinya: model ini dikontrol oleh manager kustom tadi.
    objects = UserManager() # Gunakan manager kustom

    # memberitahu Django bahwa login pakai email, bukan username
    USERNAME_FIELD = 'email' # Login pakai email
    
    # dipakai saat bikin superuser dari terminal (biar minta input nama juga).
    REQUIRED_FIELDS = ['nama'] # Field wajib saat membuat superuser

    def __str__(self):
        return self.email

    # fungsi bawaan django permissionmixin
    def has_perm(self, perm, obj=None):
        """cek apakah user punya permission tertentu"""
        # Semua user punya permission (disederhanakan)
        return True

    # User aktif (bukan superuser) cek izin spesifik di tabel permission
        # return self.is_active and super().has_perm(perm, obj)
    
    # fungsi bawaan django permissionmixin
    def has_module_perms(self, app_label):
        # Semua user bisa akses semua modul (disederhanakan)
        return True
        # Kalau bukan superuser, izinkan hanya kalau aktif dan staff
        # return self.is_active and self.is_staff