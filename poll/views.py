from django.shortcuts import render, redirect, get_object_or_404
from api.models import Poll,Vote,Book,Choice,Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 一覧表示
def poll_list(request):

    polls = Poll.objects.all() 

    paginator = Paginator(polls, 20)
    page_number = request.GET.get('page', 1)
    #　選択ページの両側には3コ表示する
    onEachSide = 3
    #　左右両端には2コ表示する
    onEnds = 2 
    try:
            poll_page = paginator.page(page_number)
    except PageNotAnInteger:
            poll_page = paginator.page(1)
    except EmptyPage:
            poll_page = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=onEachSide, on_ends=onEnds)

    context = {
        'polls': poll_page,  
        'page_range': page_range,  
    }

    
    return render(request, 'poll_list.html', context)

from django.contrib.auth.decorators import login_required

# 作成
@login_required
def create_poll(request):
    
    if request.method == 'POST':
        print("pollを作成します")

        question = request.POST.get('question')
        content = request.POST.get('content')
        print(question)
        # 選択肢を受け取る
        choices = request.POST.getlist('choice')
       
        if question:
            profile = Profile.objects.get(user=request.user)
            poll = Poll.objects.create(creator=profile, question=question,content=content)

            for choice_text in choices:
                print(choice_text)
                Choice.objects.create(poll=poll, text=choice_text)
            
            return redirect('poll_vote', poll_id=poll.id)  
    return render(request, 'create_poll.html')


# 投票do 

# ログインせずとも選択肢を見れるようにする
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    print("投票ページ")
    # 投票していれば投票結果に移動
    if request.user.is_anonymous:
        return render(request, 'poll_vote.html', {'poll': poll})

    if Vote.objects.filter(poll=poll, user=request.user).exists():
        return redirect('poll_results', poll_id=poll.id)


    if request.method == 'POST':
        # フォームから送信された選択肢のIDを取得
        chosen_choice_id = request.POST.get('choice')
        print(f"選択された選択肢のID: {chosen_choice_id}")

        # # TODO 匿名でも投票できるようにしたい
        # 選択された選択肢のIDが空でないことを確認
        if chosen_choice_id:
            chosen_choice = Choice.objects.get(id=chosen_choice_id)
            print(f"選択された選択肢: {chosen_choice.text}")
            Vote.objects.create(poll=poll, choice=chosen_choice, user=request.user)
            
            return redirect('poll_results', poll_id=poll.id)



    return render(request, 'poll_vote.html', {'poll': poll})


# 投票結果

def poll_results(request, poll_id):
    # 投票していなければpoll_voteにリダイレクトする
    # ログインしていなければログインページにリダイレクトする
    # 投票していなければpoll_voteにリダイレクトする

    # 自分が選択した選択肢に色をつける

    poll = get_object_or_404(Poll, pk=poll_id)

    if not Vote.objects.filter(poll=poll, user=request.user).exists():
        return redirect('poll_vote', poll_id=poll_id)

    votes = Vote.objects.filter(poll=poll).select_related('choice')
    total_votes = votes.count()

    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(poll=poll, user=request.user).first()

    results = {choice.text: 0 for choice in poll.choices.all()}  # 全ての選択肢を0で初期化
    for vote in votes:
        choice_text = vote.choice.text
        results[choice_text] = (results.get(choice_text, 0) + 1) / total_votes * 100
    
    results_list = [(key, results[key]) for key in results]
    
    return render(request, 'poll_results.html', {
        'poll': poll, 
        'results': results_list,
        'user_vote': user_vote 
    })

