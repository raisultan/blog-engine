from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_object': obj, 'detail': True})

class ObjectCreateMixin:
    form = None
    template = None

    def get(self, request):
        obj = self.form()
        return render(request, self.template, context={'form': obj})

    def post(self, request):
        obj = self.form(request.POST)

        if obj.is_valid():
            new_obj = obj.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': obj})

class ObjectUpdateMixin:
    model = None
    form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        # passing to form already existing object is done by 'inctance'
        obj_form = self.form(instance=obj)
        return render(request, self.template, context={'form': obj_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj_form = self.form(request.POST, instance=obj)

        if obj_form.is_valid():
            new_obj = obj_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': obj_form, self.model.__name__.lower(): obj})

class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))