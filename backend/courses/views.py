from django.http import JsonResponse
from django.views import View
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


class CoursesListView(View):
    def get(self, request):
        data_file = BASE / 'data' / 'courses.json'
        if not data_file.exists():
            return JsonResponse({'results': []})
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse({'results': data})
