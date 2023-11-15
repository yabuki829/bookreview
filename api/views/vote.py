
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import PollForm,VoteForm
from ..models import Poll,Vote
def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.creator = request.user  # ログインユーザーを投票の作成者として設定
            new_poll.save()
            form.save_m2m()  # ManyToManyフィールドの保存
            return redirect('poll_vote',poll_id=new_poll.id)  # 投票作成後のリダイレクト先
    else:
        form = PollForm()
    return render(request, 'create_poll.html', {'form': form})


def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.poll = poll
            vote.save()
            return redirect('poll_results', poll_id=poll.id)
    else:
        form = VoteForm()
    return render(request, 'poll_vote.html', {'form': form, 'poll': poll})

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    # 投票していなければpoll_voteにリダイレクトする
    # ログインしていなければログインページにリダイレクトする
    if not Vote.objects.filter(poll=poll, user=request.user).exists():
      return redirect('poll_vote',poll_id=poll_id)
    books_votes = []
    for book in poll.books.all():
        vote_count = Vote.objects.filter(poll=poll, book=book).count()
        books_votes.append((book, vote_count))

    return render(request, 'poll_results.html', {'poll': poll, 'books_votes': books_votes})