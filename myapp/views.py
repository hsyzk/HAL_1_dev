from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import AccountForm, AddAccountForm

from .models import Post
from .models import Post_Mu

from .forms import SearchForm

from django.shortcuts import render, redirect
# from . forms import UserCreateForm
# from . forms import LoginForm
# from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

class Views_index(TemplateView):
    template_name = "index.html"
    
class Views_createac(TemplateView):
    template_name = "createac.html"

class Views_home(TemplateView):
    template_name = "home.html"
    
class Views_home_mu(TemplateView):
    template_name = "home_mu.html"

class Views_post(TemplateView):
    template_name = "post.html"
    
class Views_post_mu(TemplateView):
    template_name = "post_mu.html"
    
class Views_notice(TemplateView):
    template_name = "notice.html"
    
    
class Views_shop(TemplateView):
    template_name = "shop.html"
    
class Views_search(TemplateView):
    template_name = "search.html"
    
class Views_search_mu(TemplateView):
    template_name = "search_mu.html"
    
class Views_message(TemplateView):
    template_name = "message.html"
    
class Views_ri_ru(TemplateView):
    template_name = "ri_ru.html"
    
class Views_mylist(TemplateView):
    template_name = "mylist.html"



#ログイン

def Login(request):
    if request.method == 'POST':
        
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')
        
        user = authenticate(username=ID, password=Pass)
        
        if user:
            
            if user.is_active:
                
                login(request,user)
                
                return HttpResponseRedirect(reverse('myapp:home'))
            else:
                
                return HttpResponse("アカウントが有効ではありません")
            
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    
    else:
        return render(request, 'index.html')
    
@login_required
def Logout(request):
    logout(request)
    # ログインページへ遷移
    return HttpResponseRedirect(reverse('myapp:Login'))
    
# @login_required
# def home(request):
#     params = {"UserID":request.user,}
#     return render(request, "home.html",context=params)

#アカウント作成

class AccountRegistration(TemplateView):
    
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form":AccountForm(),
        "add_account_form":AddAccountForm(),
        }
        
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"createac.html",context=self.params)
    
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)
        
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            
            account = self.params["account_form"].save()

            account.set_password(account.password)
            
            account.save()
            
            
            add_account = self.params["add_account_form"].save(commit=False)
            
            add_account.user = account

            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES["account_image"]
            else:
                add_account.account_image = 'profile_default/defaultkun.jpg'
                
            add_account.save()

            self.params["AccountCreate"] = True
            
        else:
            
            print(self.params["account_form"].errors)
            
        return render(request,"createac.html",context=self.params)


#投稿機能

    #画像
class CreatePost(CreateView):
    
   model = Post
   template_name = 'post.html'
   fields = ['title','post_image', 'content']
   success_url = reverse_lazy('myapp:home')

   def form_valid(self, form):
       """投稿ユーザーをリクエストユーザーと紐付け"""
       form.instance.user = self.request.user
       return super().form_valid(form)

    #オーディオ
class CreatePost_Mu(CreateView):
    
   model = Post_Mu
   template_name = 'post_mu.html'
   fields = ['title','post_audio', 'content']
   success_url = reverse_lazy('myapp:home_mu')

   def form_valid(self, form):
       """投稿ユーザーをリクエストユーザーと紐付け"""
       form.instance.user = self.request.user
       return super().form_valid(form)
   
    #いいね
class LikeBase(LoginRequiredMixin, View):
   """いいねのベース。リダイレクト先を以降で継承先で設定"""
   def get(self, request, *args, **kwargs):
       #記事の特定
       pk = self.kwargs['pk']
       related_post = Post_Mu.objects.get(pk=pk)
       
       #いいねテーブル内にすでにユーザーが存在する場合   
       if self.request.user in related_post.like.all(): 
           #テーブルからユーザーを削除 
           obj = related_post.like.remove(self.request.user)
       #いいねテーブル内にすでにユーザーが存在しない場合
       else:
           #テーブルにユーザーを追加                           
           obj = related_post.like.add(self.request.user)  
       return obj
   
class LikeHome_Mu(LikeBase):
   def get(self, request, *args, **kwargs):
       #LikeBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       #home_muにリダイレクト
       return redirect('myapp:home_mu')
   
    #いいね
class LikeBase2(LoginRequiredMixin, View):
   """いいねのベース。リダイレクト先を以降で継承先で設定"""
   def get(self, request, *args, **kwargs):
       #記事の特定
       pk = self.kwargs['pk']
       related_posts = Post.objects.get(pk=pk)
       
       #いいねテーブル内にすでにユーザーが存在する場合   
       if self.request.user in related_posts.like2.all(): 
           #テーブルからユーザーを削除 
           obj = related_posts.like2.remove(self.request.user)
       #いいねテーブル内にすでにユーザーが存在しない場合
       else:
           #テーブルにユーザーを追加                           
           obj = related_posts.like2.add(self.request.user)  
       return obj
   
class LikeHome(LikeBase2):
   def get(self, request, *args, **kwargs):
       #LikeBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       #home_muにリダイレクト
       return redirect('myapp:home')
   
# class LikeSearch(LikeBase2):

#    def get(self, request, *args, **kwargs):
#        #LikeBase2でリターンしたobj情報を継承
#        super().get(request, *args, **kwargs)
#        pk = self.kwargs['pk'] 

#        return redirect('myapp:search', pk)
   
# マイリスト機能
class MylistBase(LoginRequiredMixin, View):
   """いいねのベース。リダイレクト先を以降で継承先で設定"""
   def get(self, request, *args, **kwargs):
       #記事の特定
       pk = self.kwargs['pk']
       mylist_post = Post_Mu.objects.get(pk=pk)
       
       #いいねテーブル内にすでにユーザーが存在する場合   
       if self.request.user in mylist_post.mylist.all(): 
           #テーブルからユーザーを削除 
           obj = mylist_post.mylist.remove(self.request.user)
       #いいねテーブル内にすでにユーザーが存在しない場合
       else:
           #テーブルにユーザーを追加                           
           obj = mylist_post.mylist.add(self.request.user)  
       return obj
   
class MylistHome(MylistBase):
   def get(self, request, *args, **kwargs):
       #LikeBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       #home_muにリダイレクト
       return redirect('myapp:home_mu')

# マイリスト一覧表示
def mylist(request):
    user = request.user
    posts = user.mylist_post.all()
    return render(request, 'mylist.html', {'posts':posts})
   
# class LikeProfile(LikeBase2):
#     def get(self, request, *args, **kwargs):
        
#         super().get(request, *args, **kwargs)
#         pk = self.kwargs['pk']
        
#         return redirect('myapp:profile', pk)

#投稿表示

class Home(LoginRequiredMixin, ListView,):
    
    model = Post
    template_name = 'home.html'
    
    def get_object2(self):
        return self.request.user.account
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object2()
        return context
    
class Home_Mu(LoginRequiredMixin, ListView,):
    
    model = Post_Mu
    template_name = 'home_mu.html'
    
    def get_object2(self):
        return self.request.user.account
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object2()
        return context

      
class MyPost(LoginRequiredMixin, ListView):
    
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'profile.html'

    def get_queryset(self):
     #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)
    
    def get_object2(self):
        return self.request.user.account
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object2()
        return context
        

# 検索機能 
def search(request):
    searchForm = SearchForm(request.GET)
    # searchForm変数に正常なデータがあれば
    if searchForm.is_valid():
        keyword = searchForm.cleaned_data['keyword'] # keyword変数にフォームのキーワードを代入
        post = Post.objects.filter(Q(title=keyword) | Q(content=keyword)) # キーワードを含むレコードをfilterメソッドで取り出し
    # それ以外の場合
    else:
        searchForm = SearchForm() # searchForm変数をSearchFormオブジェクトで上書き
        post = Post.objects.all() # すべてのレコードを取得
 
    context = {
    'post': post,
    'searchForm': searchForm, # テンプレートに渡すために追記
    }
    return render(request, "search.html", context)

def search_mu(request):
    searchForm = SearchForm(request.GET)
    # searchForm変数に正常なデータがあれば
    if searchForm.is_valid():
        keyword = searchForm.cleaned_data['keyword'] # keyword変数にフォームのキーワードを代入
        post_mu = Post_Mu.objects.filter(Q(title=keyword) | Q(content=keyword)) # キーワードを含むレコードをfilterメソッドで取り出し
    # それ以外の場合
    else:
        searchForm = SearchForm() # searchForm変数をSearchFormオブジェクトで上書き
        post_mu = Post_Mu.objects.all() # すべてのレコードを取得
 
    context = {
    'post_mu': post_mu,
    'searchForm': searchForm, # テンプレートに渡すために追記
    }
    return render(request, "search_mu.html", context)