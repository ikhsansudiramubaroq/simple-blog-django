from django.shortcuts import render
# import paginator
from django.core.paginator import Paginator
# import models
from .models import Category, Article, Comment
from . forms import CommentsForm
# import model taggit
from taggit.models import Tag

# Create your views here.
def index(request):
    list_articles = Article.objects.all().order_by('-publish')
    category_choices = Category.objects.all()

    # add paginator
    p = Paginator(list_articles, 2) # Show 6 articles per page
    page_number = request.GET.get('page') # get adalah fungsi dari paginator
    articles = p.get_page(page_number) # get_page adalah fungsi dari paginator
    context = {
        'title':'Blog',
        # 'list_articles': list_articles,
        'category_choices' : category_choices,
        'articles' : articles,
    }
    return render(request, 'blog/index.html', context)

def detail_article(request, slug_input):
    # Mengambil satu artikel berdasarkan slug yang diklik user.
    detail_article = Article.objects.get(slug=slug_input)
    
    # Ambil 3 artikel lain selain yang sedang dibuka (buat rekomendasi di bawah artikel).
    article_other = Article.objects.exclude(slug=slug_input).order_by('-publish')[:3]
    
    # ambil semua tag
    tags = Tag.objects.all()
    
    # Ambil semua komentar utama (bukan balasan).
    # Karena reply=None berarti komentar tersebut tidak punya “parent” alias komentar induk.
    # Mengambil list semua komentar yang merupakan komentar utama (bukan balasan) untuk artikel yang sedang dilihat.
    # reply=None adlaah memastikan yang diambil hanyalah komentar induk. 
        # Karena di model Comment, field reply merujuk ke dirinya sendiri. 
        # Jika nilainya None (null), berarti komentar itu tidak membalas siapa-siapa.
    comments_article = Comment.objects.filter(articles=detail_article,reply=None).order_by('-timestamp')

    # kode komentar
    if request.method == 'POST':
        # Buat instance form dari data yang dikirim user.
        form = CommentsForm(request.POST or None)
        if form.is_valid():
            # simpan data dari form ke database
            # Ambil isi teks komentar dari form.
            # ambil field dari field comment dengan field comments yang ada pada input 
            comment = request.POST.get('comments')
            
            # Ini mengambil ID komentar induk jika komentar yang dikirim adalah balasan.
            # Nilai ini berasal dari field tersembunyi (<input type="hidden" name="reply_slug" 
                # value="{{ comment.id }}">)
            reply = request.POST.get('reply_slug')
            
            # buat default reply dari komentar adalah none agar tidak error
            comments_reply = None
            
            if reply:
                comments_reply = Comment.objects.get(id=reply)
            
                
            # Buat record baru di database untuk komentar (baik komentar baru atau balasan).
            comment = Comment.objects.create(articles=detail_article, user=request.user,
                                            comments=comment, reply=comments_reply)
            form=CommentsForm()
    else :
        form = CommentsForm()


    context = {
        'title':'Detail Blog',
        'detail_article' : detail_article,
        'article_other' : article_other,
        'form' : form,
        'comments' : comments_article,
        'tags' : tags,
    }
    return render(request, 'blog/detail_article.html', context)

def category(request, category_input):
    # __ adalah lookup spanning relationships, dan fungsi iexact digunakan untuk membandingkan string tanpa memperhatikan huruf besar atau kecil.
    # melakukan filter pada model terkait dengan "melompat" ke model yang berhubungan.
    category_article = Article.objects.filter(categories__title__iexact=category_input)
    category_choices = Category.objects.order_by('id')
    context = {
        'title':'Artikel Berdasarkan Kategori', 
        'category_article': category_article,
        'category_choices' : category_choices,
    }
    return render(request, 'blog/category.html', context)

def tagged(request, tags_input):
    # tag diambil dari model taggit yang berelasi dengan Article
    tags = Tag.objects.get(slug=tags_input)
    common_tags = Article.tags.most_common()[:10] # menampilkan 10 tags yang paling banyak digunakan
    article_tags = Article.objects.filter(tags=tags)
    # kategorinya diambil dari model category
    category_choices = Category.objects.all()
    context = {
        'title' : 'Artikel Berdasarkan Tags',
        'tags' : tags,
        'article_tags' : article_tags,
        'common_tags' : common_tags,
        'category_choices' : category_choices,
    }
    return render(request, 'blog/article_tags.html', context)
