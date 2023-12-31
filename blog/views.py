from django.shortcuts import render,redirect
from django.views.generic import View
from api.models import Blog,Tag
from accounts.views import AccountClass
# 記事の投稿
class PostBlogView(View):
  def get(self,request):
    print("記事作成画面です")
    return render(request, "create_blog.html")

  def post(self,request):

    print(self.request.POST["title"])
    title = self.request.POST["title"]
    content = self.request.POST["content"]
    tag = self.request.POST["tag"]
    user = self.request.user

    accout = AccountClass()
    
    blog = BlogClass().post_blog(accout.get_profile(user),title,content,tag)
    print(blog,"を作成しました")
   # 記事が作成されたら記事の詳細画面に移動する
    return redirect('details_blog', pk=blog.id)  

# 記事の詳細
class DetailsBlogView(View):
  def get(self,request,pk):
    blog = Blog.objects.get(id=pk)
    return render(request, "details.html",{"blog":blog})


  def post(self,request,pk):
    # pkにコメントする
    print("コメントします")
    return redirect('details_blog', pk=pk)  

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.db.models import Count

# ブログの一覧表示
class BlogListView(View):

  def get(self,request):

    
    tag_id = request.GET.get('tag_id', '') 
    print("tag:",tag_id)
    if tag_id == "":
      blogs = Blog.objects.all()
      per_page = 12

      paginator = Paginator(blogs, per_page)
      page_number = request.GET.get('page', 1)
        #　選択ページの両側には3コ表示する
      onEachSide = 3
        #　左右両端には2コ表示する
      onEnds = 2 
      try:
          blog_page = paginator.page(page_number)
      except PageNotAnInteger:
          blog_page = paginator.page(1)
      except EmptyPage:
          blog_page = paginator.page(paginator.num_pages)

      page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)
    else:
      
      blogs = Blog.objects.filter(tag=tag_id)
      per_page = 12

      paginator = Paginator(blogs, per_page)
      page_number = request.GET.get('page', 1)
        #　選択ページの両側には3コ表示する
      onEachSide = 3
        #　左右両端には2コ表示する
      onEnds = 2 
      try:
          blog_page = paginator.page(page_number)
      except PageNotAnInteger:
          blog_page = paginator.page(1)
      except EmptyPage:
          blog_page = paginator.page(paginator.num_pages)

      page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)

    # タグの数が増えたらこれを使う
    # tag_list = Tag.objects.annotate(num_blogs=Count('blog')).order_by('-num_blogs')[:20]

    tag_list = Tag.objects.all() 
    print(tag_list)
    context = {
        'blog_page': blog_page,  
        'page_range': page_range,  
        "tag_list":tag_list
    }

    
    return render(request, 'blog_list.html', context)
  

class Show_Blog_Tag(View):
  def get(self,request,tag):
    print("呼ばれてますか？")

    tag_obj = Tag.objects.filter(title=tag).first()


    blogs = Blog.objects.filter(tag=tag_obj)
    per_page = 12

    paginator = Paginator(blogs, per_page)
    page_number = request.GET.get('page', 1)
        #　選択ページの両側には3コ表示する
    onEachSide = 3
        #　左右両端には2コ表示する
    onEnds = 2 
    try:
          blog_page = paginator.page(page_number)
    except PageNotAnInteger:
          blog_page = paginator.page(1)
    except EmptyPage:
          blog_page = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)

    # タグの数が増えたらこれを使う
    tag_list = Tag.objects.annotate(num_blogs=Count('blog')).order_by('-num_blogs')[:20]

    
    context = {
        'blog_page': blog_page,  
        'page_range': page_range,  
        "tag":tag,
        "tag_list":tag_list

    }
    

    return render(request, 'blog_list.html', context)
 
  

class ShowTagsView(View):
  def get(self,request):

    tags = Tag.objects.annotate(num_blogs=Count('blog')).order_by('-num_blogs')

    context = {
        'tags': tags,  
    }
    return render(request, 'show_all_tags.html', context)
 
  pass

class BlogClass():
  def post_blog(self,creator,title,content,tag):
    blog = Blog.objects.create(creator=creator,title=title,content=content,tag=self.get_tag(tag))
    return blog
  

 

  def delete_blog(self,creator,blog_id):
    pass

  def get_tag(self,tag_title):
    # タグを取得する
    # タグが登録されていなければ新しく作成する

    tag, created = Tag.objects.get_or_create(title=tag_title)
    return tag


