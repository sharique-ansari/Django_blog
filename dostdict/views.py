from .models import Word
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import WordForm


def word_list(request):
    return render(request,'dostdict/word_list.html')


def starts_with(request,pk):
    words= Word.objects.order_by('-created_date').filter(word_title__startswith=pk)[:5]
    return render(request, 'dostdict/word_starts.html', {'words': words})


def all_startswith(request,pk):
    words=Word.objects.filter(word_title__startswith=pk)
    return render(request,'dostdict/word_starts_all.html',{'words':words})



def word_detail(request,pk):
    print(pk)
    word = get_object_or_404(Word,pk=pk)
    print(word.meaning)
    return render(request, 'dostdict/word_detail.html', {'word':word})

@login_required
def add_word(request):
    if request.method =="POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.author=request.user
            word.save()
            return redirect('word_detail', pk=word.pk)
    else:
        form = WordForm()
    return render(request, 'dostdict/add_word.html',{'form':form})


@login_required
def word_edit(request,pk):
    word=get_object_or_404(Word,pk=pk)
    if request.method=="POST":
        form =WordForm(request.POST, instance=word)
        if form.is_valid():
            word = form.save(commit=False)
            word.author = request.user
            word.save()
            return redirect('word_detail',pk=word.pk)
    else:
        form= WordForm(instance=word)
    return render(request,'dostdict/add_word.html',{'form':form})


@login_required
def word_delete(request,pk):
    word=get_object_or_404(Word ,pk=pk)
    word.delete()
    return redirect('word_list')





# Create your views here.
