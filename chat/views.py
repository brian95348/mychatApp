from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Profile, Message
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from .forms import ProfileModelForm
from django.http import HttpResponseRedirect
from django.db.models import Q
from guardian.mixins import PermissionRequiredMixin

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile-list'))
    return HttpResponseRedirect(reverse('login'))

@method_decorator(login_required,name='dispatch')
class ProfileListView(CreateView):
    model           = Profile
    form_class      = ProfileModelForm
    template_name   = 'chat/profile_form.html'
    
    def get(self,request,*args,**kwargs):
        profile_obj = self.model.objects.filter(user__email=request.user.email)
        chats = []
        if profile_obj:
            qs = self.model.objects.exclude(user__email=self.request.user.email)
            for p in qs:
                chats_msgs = []
                username = p.user.username
                lookups = Q(user=request.user) | Q(receiver=username) | Q(user=p.user) | Q(receiver=request.user.username)
                chat_msgs_qs = Message.objects.filter(lookups)
                for msg in chat_msgs_qs:
                    chats_msgs.append([msg.text,msg.user.username,msg.receiver,msg.created.strftime("%Y-%m-%d, %H:%M"),msg.id])
                chats.append([username,p.user.id,chats_msgs,p.status,p.profile_picture.url,p.get_absolute_url()])
            context = {'profile_list':qs,'chats':chats,'username':profile_obj[0].username,'profile_exists':True,'profile_obj':profile_obj[0]}
            return render(request,'chat/profile_list.html',context)
        else:
            form = self.form_class()
            return render(request,self.template_name,{'form':form,'profile_exists':False,'chats':chats})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        instance = form.save()
        return HttpResponseRedirect(instance.get_absolute_url())

@method_decorator(login_required,name='dispatch')   
class ProfileDetailView(DetailView):
    model = Profile

    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,username=self.kwargs['username'])

@method_decorator(login_required,name='dispatch') 
class ProfileUpdateView(PermissionRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileModelForm
    permission_required = 'chat.change_Profile'
    raise_exception = True
    template_name = 'chat/profile_updateform.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object())
        return render(request, self.template_name, {'form':form, 'object': self.get_object()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_object().get_absolute_url())

    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,username=self.kwargs['username'])

@method_decorator(login_required,name='dispatch')
class ProfileDeleteView(PermissionRequiredMixin, DeleteView):
    model = Profile
    permission_required = 'chat.add_Profile'
    raise_exception = True

    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,username=self.kwargs['username'])
   
    def get_success_url(self):
        return reverse_lazy('profile-list')

    
