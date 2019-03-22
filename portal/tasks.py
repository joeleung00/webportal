from background_task import background
from .netgrep import parsehtml
from . import models as db

#@background(schedule=1)
def process_grep_requests():
    # Currently just directly update the target message on trigger
    # TODO: add grep_requests to queue and process them sequentially in background process
    grep_requests = db.GrepRequest.objects.all()
    for request in grep_requests:
        # Parse and get target content
        target_tags = [request.selected_content]
        target_content = "Target not found, please consider refeshing your request."
        multiple = ParseHtml.retrieve_first_tags_matches(target_tags, request.url)
        for tag in multiple:
            if tag is not None:
                target_content = ParseHtml.convert_tag_to_string(tag)

        # Find corresponding message to update
        message = request.message
        message.content = target_content
        message.save()
