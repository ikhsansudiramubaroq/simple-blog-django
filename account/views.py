from django.shortcuts import render, redirect  # Untuk render template & redirect halaman
from django.contrib.auth import logout         # Fungsi bawaan Django untuk logout user
from .forms import RegisterUserForm, UpdateUserForm            # Form kustom untuk registrasi user
from django.contrib.auth.decorators import login_required


def index_profile(request):
    context = {
        'title': 'User Profile',
    }
    return render(request, 'account/profile.html', context)

@login_required(login_url='accounts:login')
def update_profiles(request):
    if request.method == 'POST':
        
        # fungsi instance adalah Gunakan data milik user yang sedang login sebagai objek yang sedang diedit.
        # saat form dikirim (POST request) → data di-update ke user login itu juga.
        form = UpdateUserForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    
    # jika data get maka field terisi otomatis dengan data user login
    else:
        form = UpdateUserForm(instance=request.user)
    context = {
        'title': 'Edit User Profile',
        'form': form
    }
    return render(request, 'account/edit_profile.html', context)

# View untuk logout user
def LogoutView(request):
    # Logout user yang sedang login
    logout(request)
    # Setelah logout, arahkan user ke halaman index blog
    return redirect('blog:blog_index')

# View untuk registrasi user baru
def register_users(request):
    # Jika request berasal dari form POST (form dikirimkan)
    if request.method == 'POST':
        # Ambil data dari form
        form = RegisterUserForm(request.POST or None)
        # Validasi data form
        if form.is_valid():
            # Simpan user baru ke database
            form.save()
            # Arahkan ke halaman login setelah registrasi berhasil
            return redirect('accounts:login')
    else:
        # Jika request GET, buat form kosong
        form = RegisterUserForm()

    # Data yang akan dikirim ke template
    context = {
        'title': 'Register User',  # Judul halaman
        'form': form,              # Instance form yang akan ditampilkan di template
    }

    # Tampilkan halaman registrasi dengan form
    return render(request, 'registration/daftar.html', context)
