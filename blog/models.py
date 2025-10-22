from django.db import models

# import setting untuk import user
from django.conf import settings
# import slugify
from django.utils.text import slugify
# import taggit
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug_cat = models.SlugField(blank=True, editable=False)
    icons = models.ImageField(blank=True, default='category.jpg',upload_to='category/')

    # args = argument, kwargs = keyword argument
    def save(self, *args, **kwargs):
        self.slug_cat = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    # foreign key ke category
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    fil = models.TextField()
    images = models.ImageField(blank=True, default='articles.jpg', upload_to='articles/')
    tags = TaggableManager()
    slug = models.SlugField(blank=True, editable=False)
    publish = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    # args = argument, kwargs = keyword argument
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # setiap komentar harus dimiliki oleh satu user (penulis komentar).
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE, default=0) # default 0 untuk user yg tidak terdaftar
    
    # jadi relasinya: 1 artikel bisa punya banyak comment.
    # kalau artikelnya dihapus → semua comment di artikel itu juga ikut hilang (CASCADE).
    articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    comments = models.TextField()
    
    # satu komentar bisa menjadi balasan dari komentar lain.
    # related_name='replies' digunakan agar kamu bisa akses dari komentar utama ke semua balasannya
    reply = models.ForeignKey('self',related_name='replies',max_length=250 ,
                            on_delete=models.CASCADE, blank=True, null=True) #mengambil relasi dari dirinya sendiri
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.articles.title} - {self.comments} - {self.user.nama}"