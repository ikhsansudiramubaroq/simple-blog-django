# import bawaan Django:
# UserCreationForm → digunakan untuk membuat user baru (registrasi)
# UserChangeForm   → digunakan untuk mengubah data user yang sudah ada
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# import model User custom (bukan bawaan django.contrib.auth.models.User)
from .models import User

# ===============================================
# FORM UNTUK UPDATE PROFIL USER
# ===============================================
# class UpdateUserForm mewarisi UserChangeForm bawaan Django
# Secara default, UserChangeForm memuat semua field user (termasuk password),
# tapi di sini kita override agar hanya field tertentu yang bisa diedit user.
class UpdateUserForm(UserChangeForm):
    class Meta: 
        model = User
        
        #overide dan pilih field tertentu untuk update user nya 
        #field yang boleh diubah user di halaman edit profil
        fields = ['nama','tempat_lahir','email','tgl_lahir' ,'no_hp' ,'img_user']

    # override __init__ untuk menambahkan atribut HTML (class, placeholder) pada tiap field
    # Tujuannya agar tampilan form lebih rapi dan sesuai dengan bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # menambahkan css pada setiap field di edit profile/ update user
        # Tambahkan atribut HTML ke masing-masing input
        self.fields['nama'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan Nama Lengkap'}) 
        self.fields['tempat_lahir'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan Tempat Lahir'}) 
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan Email anda'}) 
        self.fields['tgl_lahir'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan tanggal lahir'}) 
        self.fields['no_hp'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Masukkan No Hp anda'}) 
        self.fields['img_user'].widget.attrs.update({'class': 'form-control'}) 

# ===============================================
# FORM UNTUK REGISTRASI USER BARU
# ===============================================
# class RegisterUserForm mewarisi UserCreationForm bawaan Django
# Form ini secara otomatis sudah menyediakan validasi untuk password1 dan password2
# (misalnya: minimal panjang karakter, kesamaan password, dll)
class RegisterUserForm(UserCreationForm):
    class Meta:
        # model User diambil dari custom model (BUKAN bawaan auth.User)
        model = User
        
        # field yang akan ditampilkan di form registrasi
        # password1 & password2 otomatis ditangani oleh UserCreationForm
        fields = ['nama', 'no_hp' ,'email', 'password1', 'password2']