import os
import markdown
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.conf import settings


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

# generic views
