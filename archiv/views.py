import hashlib

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from archiv.models import UserInput


@login_required
def ask_a_question(request):
    template_name = "archiv/question.html"
    context = {"foo": "bar"}
    context = {"created": True}
    if request.method == "POST":
        content = request.POST.get("content")
        text_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        try:
            item = UserInput.objects.get(text_hash=text_hash)
            context["created"] = False
        except ObjectDoesNotExist:
            item = UserInput.objects.create(content=content)
        related_objects = item.find_similar(amount=10)
        context["object"] = item
        context["related_objects"] = related_objects

    return render(request, template_name, context=context)
