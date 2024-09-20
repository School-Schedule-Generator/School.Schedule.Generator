import os
import markdown
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    return render(request, 'generatorApp/home.html')


class DocsView(View):
    docs_path = os.path.join(settings.BASE_DIR, 'generatorApp/DOCS')

    def get(self, request, lang, file):
        selected_language = request.GET.get('language', lang)

        file_path = os.path.join(self.docs_path, lang, file + '.md')
        file_context = open(file_path, mode="r", encoding="utf-8").read()
        file_context = markdown.markdown(file_context)

        if lang != selected_language:
            return HttpResponseRedirect(
                reverse('generatorApp:docs', kwargs={'lang': selected_language, 'file': 'intro'}))
        return render(request, 'generatorApp/docs.html', {'lang': selected_language, 'file_content': file_context})


@csrf_exempt
def remove_message(request):
    if not settings.DEBUG:
        # Return 404 if not in DEBUG mode
        return HttpResponseNotFound("This endpoint is only available in DEBUG mode.")

    if request.method == 'POST':
        data = json.loads(request.body)
        msg_type = data.get('msg_type')
        if msg_type and msg_type in request.session:
            del request.session[msg_type]
            request.session.modified = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
