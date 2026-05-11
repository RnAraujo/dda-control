from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Participant
from .forms import ParticipantForm, ParticipantSearchForm

class ParticipantListView(ListView):
    model = Participant
    template_name = 'participants/list.html'
    context_object_name = 'participants'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = ParticipantSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            if search:
                queryset = queryset.filter(
                    Q(dni_number__icontains=search) |
                    Q(names__icontains=search) |
                    Q(father_lastname__icontains=search) |
                    Q(mother_lastname__icontains=search) |
                    Q(email__icontains=search)
                )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ParticipantSearchForm(self.request.GET)
        return context

class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'participants/detail.html'
    context_object_name = 'participant'

class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/form.html'
    success_url = reverse_lazy('participants:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Participante registrado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al registrar el participante. Verifique los datos.')
        return super().form_invalid(form)

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'participants/form.html'
    success_url = reverse_lazy('participants:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Participante actualizado exitosamente')
        return super().form_valid(form)

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'participants/confirm_delete.html'
    success_url = reverse_lazy('participants:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Participante eliminado exitosamente')
        return super().delete(request, *args, **kwargs)