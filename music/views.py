from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .forms import UserForm


def index(request):
    all_albums = Album.objects.all()

    # template = loader.get_template('music/index.html')
    context = {
        'all_albums': all_albums,
    }
    # return HttpResponse(template.render(context,request))

    return render(request, 'music/index.html', context)


def detail(request, album_id):
    # return HttpResponse("<h2>Details for Album id :"+str(album_id) + "</h2>")
    # try:
    # album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    # raise Http404("Album does not exist")
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})

def favourite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except(KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html',{
            'album': album,
            'error_message': "You did not select a valid song!",
        })
    else:
        selected_song.is_favourite = True;
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})

class UserFormView(View):
    form_class = UserForm
    template_name = 'music_registration_form.html'

    #display a blank form to the user
    def get(self, request):
        form  = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit = False)