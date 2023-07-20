from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q  # Import the Q object
from .models import NewsStory
from .forms import StoryForm
from taggit.models import Tag
# additional when adding tags
from django.shortcuts import get_object_or_404, redirect, render
from .models import NewsStory, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = "all_stories"
    

    def get_queryset(self):
        '''Return all news stories.'''
        query = self.request.GET.get('q')  # Get the search query from the URL parameters
        if query:
            # If a search query is provided, filter the news stories by author or tags
            return NewsStory.objects.filter(Q(author__username__icontains=query) | Q(tags__name__icontains=query))
        else:
            return NewsStory.objects.all()
        # return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.order_by('-pub_date')[:4]
        # print(NewsStory.object.all()[:4])
        return context
    
class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'author': self.request.user, 'news_story': self.object})
        return context

    def post(self, request, *args, **kwargs):
        news_story = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
        # Use set() method to associate the comment with the news_story
            comment.news_story.set([news_story])
            comment.save()
            return redirect('news:story', pk=news_story.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))



def add_comment(request, story_id):
    story = get_object_or_404(NewsStory, pk=story_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = story
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('news:story', story_id=story_id)

    else:
        form = CommentForm()

    return render(request, 'news/add_comment.html', {'form': form, 'story': story})


class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyform'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')

# Update story creation view - To replace that text field, we need to tell our view to insert the current user's info whenthey submit a new story. 
    def form_valid(self, form):
        form.instance.author = self.request.user
        # Save the form to get the instance with the primary key
        story = form.save()

        # Get the tags entered in the form and add them to the story
        tags_input = form.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        story.tags.add(*tag_list)

        return super().form_valid(form)

    # good place to add to project - take to other place, view of what you've written?




# use the print function to see what you are doing and help you debug