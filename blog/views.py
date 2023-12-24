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
