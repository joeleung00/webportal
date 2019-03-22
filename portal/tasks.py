from background_task import background
from .netgrep import parsehtml
from .models import Category

#@background(schedule=1)
def process_grep_requests():
    grep_requests = Category.objects.all()
    for request in grep_requests:
        request.title = "Nope"
        request.save()
