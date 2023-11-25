from django.shortcuts import render, redirect, get_object_or_404
from api.models import Poll,Vote,Book,Choice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

@login_required
def create_poll(request):
    
    if request.method == 'POST':
        print("pollを作成します")

        question = request.POST.get('question')
        print(question)
        # 選択肢の処理（例: 'choices' というフィールド名で受け取る）
        choices = request.POST.getlist('choice')

        if question:
            poll = Poll.objects.create(creator=request.user, question=question)

            for choice_text in choices:
                print(choice_text)
                Choice.objects.create(poll=poll, text=choice_text)
            
            return redirect('poll_vote', poll_id=poll.id)  
    return render(request, 'create_poll.html')

def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if Vote.objects.filter(poll=poll, user=request.user).exists():
        return redirect('poll_results', poll_id=poll.id)

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        selected_choice = get_object_or_404(Choice, pk=choice_id)
        # TODO 匿名でも投票できるようにしたい
        Vote.objects.create(poll=poll, choice=selected_choice, user=request.user)
        return redirect('poll_results', poll_id=poll.id)

    return render(request, 'poll_vote.html', {'poll': poll})



def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    # 投票していなければpoll_voteにリダイレクトする
    # ログインしていなければログインページにリダイレクトする
    # 投票していなければpoll_voteにリダイレクトする

    if not Vote.objects.filter(poll=poll, user=request.user).exists():
        return redirect('poll_vote', poll_id=poll_id)

    poll = get_object_or_404(Poll, pk=poll_id)
    votes = Vote.objects.filter(poll=poll).select_related('choice')

    results = {}
    for vote in votes:
        choice_text = vote.choice.text
        results[choice_text] = results.get(choice_text, 0) + 1
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'poll_results.html', {'poll': poll, 'results': sorted_results})