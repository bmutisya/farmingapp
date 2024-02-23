from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView,DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse_lazy
from . models import Animal, AnimalHealth,MilkRecord
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth import login
from django import forms
from django.views.generic import TemplateView
from django.db.models import Count
from django.db.models import Sum, F
from datetime import date


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('animals')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('animals')
    
    def form_valid(self, form):
        farmer = form.save()
        if farmer is not None:
            login(self.request, farmer)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('animals')     
        return super(RegisterPage,self).get(*args, **kwargs)

#  If the built-in LogoutView is not behaving as expected, consider creating a custom logout view where you can override the get method to handle the logout process and redirect to the login page.
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login')) 
    
class AnimalList(LoginRequiredMixin, ListView):
    model = Animal
    context_object_name = 'animals'
    template_name = 'base/animals.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals'] = context['animals'].filter(farmer=self.request.user) # Helpsin making sure that a farmer only sees their animals.. we overide the main listView
        context['count'] = context['animals'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['animals'] = context['animals'].filter(animal_name__startswith = search_input)
            context['search_input'] = search_input
        return context

class AnimalDetail(LoginRequiredMixin, DetailView):
    model = Animal
    context_object_name = 'animal'

class AnimalCreate(LoginRequiredMixin, CreateView):
    model = Animal
    fields =  ['animal_id', 'animal_name', 'ear_tag', 'sire_id', 'dam_id', 'animal_type', 'color', 'breed', 'description', 'date_of_birth', 'current_age', 'weight_at_birth', 'age_at_first_service', 'weight_at_first_service', 'complete']
    success_url = reverse_lazy('animals')
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super(AnimalCreate, self).form_valid(form)
    

class AnimalUpdate(LoginRequiredMixin, UpdateView):
    model = Animal
    fields =  ['animal_id', 'animal_name', 'ear_tag', 'sire_id', 'dam_id', 'animal_type', 'color', 'breed', 'description', 'date_of_birth', 'current_age', 'weight_at_birth', 'age_at_first_service', 'weight_at_first_service', 'complete']
    success_url = reverse_lazy('animals')

class AnimalDelete(LoginRequiredMixin, DeleteView):
    model = Animal
    context_object_name = 'animal'
    success_url = reverse_lazy('animals')
    
    #start with register 1:20...
    
    
    
# ANIMAL HEALTH VIEWS


class AnimalHealthForm(forms.ModelForm):
    class Meta:
        model = AnimalHealth
        fields = ['animal', 'date', 'symptoms', 'diagnosis', 'treatment', 'cost', 'vet_name']
    
  
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Check if the instance already exists (i.e., form is used for editing)
            # Exclude the currently selected animal from the queryset
            self.fields['animal'].queryset = Animal.objects.filter(farmer=user).exclude(pk=self.instance.animal.pk)
        else:
            # Filter animals belonging to the logged-in user
            self.fields['animal'].queryset = Animal.objects.filter(farmer=user)


class AnimalHealthCreate(LoginRequiredMixin,CreateView):
    model = AnimalHealth
    form_class =AnimalHealthForm
    template_name = 'base/animal_health_add.html'
    success_url = reverse_lazy('animal-health-records')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
# We create a custom form AnimalHealthForm that inherits from forms.ModelForm. In the form's __init__ method, we override the queryset of the animal field to filter animals belonging to the logged-in user.
# We pass the user object to the form's __init__ method through the get_form_kwargs method in the view.
# In the view, we specify the form_class as AnimalHealthForm to use our custom form for creating health records.
    
    
class AnimalHealthRecords(LoginRequiredMixin,ListView):
    model = AnimalHealth
    context_object_name = 'health'
    template_name = 'base/animalhealth.html'
    
    def get_queryset(self):
        # Retrieve the currently logged-in farmer
        farmer = self.request.user
        # Filter the AnimalHealth records based on the animals belonging to the logged-in farmer
        queryset = super().get_queryset().filter(animal__farmer=farmer)
        queryset = queryset.select_related('animal')
        return queryset
    
 

class AnimalHealthDetail(LoginRequiredMixin,DetailView):
    model = AnimalHealth
    context_object_name = 'animalhealth'
    template_name = 'base/animalhealthdetail.html'


class AnimalHealthUpdate(LoginRequiredMixin, UpdateView):
    model = AnimalHealth
    # form_class = HealthUpdateForm 
    fields = ['date', 'symptoms', 'diagnosis', 'treatment', 'cost', 'vet_name']
    template_name = 'base/animal_health_add.html'
    success_url = reverse_lazy('animal-health-records')
    
   
  
   
   
class AnimalHealthDelete(LoginRequiredMixin,DeleteView):
    model = AnimalHealth
    context_object_name = 'animalhealth'
    success_url = reverse_lazy('animal-health-records')
    
    
    
    
    
#    MIlk Records Views

class MilkRecordForm(forms.ModelForm):
    class Meta:
        model = MilkRecord
        fields = ['animal', 'milking_date', 'morning_milk', 'afternoon_milk','evening_milk'] 
        widgets = {
            'milking_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
        # Add other fields as needed

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter animals by type cow and belonging to the logged-in user
        self.fields['animal'].queryset = Animal.objects.filter(farmer=user, animal_type='cow')
        
class MilkCreate(LoginRequiredMixin,CreateView):
    model = MilkRecord
    form_class = MilkRecordForm
    template_name = 'base/milk_create.html'
    context_object_name ="milk"
    success_url = reverse_lazy('milk-records')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs
    
class MilkList(LoginRequiredMixin,ListView):
    model = MilkRecord
    context_object_name = 'milkrecords'
    template_name = 'base/milk_records.html'
    
    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user

        # Filter milk records for the logged-in user
        queryset = MilkRecord.objects.filter(animal__farmer=user)

        return queryset
    
class MilkUpdate(LoginRequiredMixin,UpdateView):
    model = MilkRecord
    fields = ['milking_date', 'morning_milk', 'afternoon_milk','evening_milk']
    template_name = 'base/milk_create.html'
    context_object_name ="milk"
    success_url = reverse_lazy('milk-records')
    
    
class MilkDelete(LoginRequiredMixin,DeleteView):
    model = MilkRecord
    context_object_name = 'milk'
    success_url = reverse_lazy('milk-records')
    template_name = 'base/milk_confirm_delete.html'
    
    
    
    
    
    
    
    
    # dashboard
@login_required
def DashboardView(request):
    user= request.user
    cow_no = Animal.objects.filter(farmer=user, animal_type='cow').count()
    bull_no = Animal.objects.filter(farmer=user, animal_type='bull').count()
    heifer_no = Animal.objects.filter(farmer=user, animal_type='heifer').count()
    calf_no = Animal.objects.filter(farmer=user, animal_type='calf').count()
    animal_counts = Animal.objects.filter(farmer=user).values('animal_type').annotate(count=Count('animal_type'))
    total_animals = sum(item['count'] for item in animal_counts)
    
    animal_type =['cow','bull','heifer','calf']
    animal_type_no =[cow_no,bull_no, heifer_no, calf_no]
    
      # Fetch all milk records belonging to the logged-in user's animals
    milk_records = MilkRecord.objects.filter(animal__farmer=user)
    total_milk = 0
    
    # # Iterate over each milk record and sum the milk produced
    # for record in milk_records:
    #     total_milk += record.morning_milk + record.afternoon_milk + record.evening_milk
    
    current_date = date.today()
    milk_records = MilkRecord.objects.filter(milking_date=current_date, animal__farmer=user)
    total_milk = sum(record.morning_milk + record.afternoon_milk + record.evening_milk for record in milk_records)
    
    # Query all animals for the logged-in user
    animals = Animal.objects.filter(farmer=user)
    
    milk_records = MilkRecord.objects.filter(animal__farmer=user, milking_date=date.today())
    animal_milk_records = {}
    for record in milk_records:
        # Assuming you have a field 'animal_name' in your Animal model
        animal_name = record.animal.animal_name
        if animal_name in animal_milk_records:
            # If the animal name already exists in the dictionary, add the milk production
            animal_milk_records[animal_name] += record.morning_milk + record.afternoon_milk + record.evening_milk
        else:
            # If the animal name doesn't exist, initialize it with the milk production
            animal_milk_records[animal_name] = record.morning_milk + record.afternoon_milk + record.evening_milk

    
    
    context={'animal_type':animal_type, 'animal_type_no':animal_type_no, 'total_animals':total_animals, 'total_milk':total_milk, 'animal_milk_records': animal_milk_records }
    
    
    return render(request,'base/dashboard.html',context)
    
    
    
    
    
#     my search html omited
# <form method="Get">
#   <input type="text" name="search-area" value="{{ search_input }}" />
#   <input type="submit" value="Search" />
# </form>

#Notes
# in classed based viws for a list view the  templates expect a model_list.html template  to change this define template name
# to display the list in class based views the list  is store in objevct_list to change this variable declear your context_object_name
#In detailView the data is return as an object