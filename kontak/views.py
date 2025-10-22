from django.shortcuts import render, redirect

# import core mail
from django.core.mail import send_mail
# import form kontak
from .forms import SendingEmailForm
# import setting
from django.conf import settings

# Create your views here.
def index(request):
    # Mengecek apakah request yang masuk adalah POST (form dikirim)
    if request.method == 'POST':
        # Membuat instance form dengan data yang dikirim (POST)
        form = SendingEmailForm(request.POST or None)
        
        # Memvalidasi form sesuai aturan di forms.py
        if form.is_valid():
            # Mengambil data subject dari form yang sudah divalidasi
            subjek = form.cleaned_data['subject']
            # Mengambil alamat email pengirim dari form
            email = form.cleaned_data['email']
            # Mengambil nama pengirim dari form
            nama = form.cleaned_data['name']
            # Mengambil isi pesan dari form
            pesan = form.cleaned_data['message']
            
            # Mengirim email menggunakan fungsi bawaan Django
            send_mail(
                subject=subjek,  # Judul email
                message=f"Pesan dari {nama}, dengan email: {email}\n\nIsi pesan:\n{pesan}",  # Isi email
                from_email=settings.EMAIL_HOST_USER,  # Email pengirim (harus sesuai pengaturan SMTP)
                recipient_list=['ikhsansudiramubaroq2910@gmail.com'],  # Ganti dengan list email tujuan
                fail_silently=False  # Jika terjadi error, jangan diam-diam, tapi munculkan error
            )
            
            # Redirect ke halaman 'kontak:index' setelah sukses kirim email
            return redirect('kontak:index')
    else:
        # Jika request bukan POST, buat form kosong
        form = SendingEmailForm()

    # Data yang dikirim ke template HTML
    context = {
        'title': 'Kontak',  # Judul halaman
        'form': form,       # Form kirim email
    }
    
    # Render template HTML 'kontak/index.html' dengan context di atas
    return render(request, 'kontak/index.html', context)
