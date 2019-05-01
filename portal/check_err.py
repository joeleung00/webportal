# It will detect error base on the grep attribute provided by the user
from urllib import request

# Since no two category which belongs to the same user can share the same name,
# So we check if there exist repeated name when new category is created.
def check_no_repeat_name(request, categories):
    new_category_title = request.POST['new_cate_title']
    for category in categories:
        if (new_category_title == category.title):
            return False
    return True

# Check invalid attribute of a grep request
def check_input_error(url, msg_title, crawltag, add_to_calendar, user):
    # the message title is empty
    if (msg_title == ''):
        return  0

    # the url cannot be visited
    try:
        request.urlopen(url)
        print("sucess")
    except:
        print("url error")
        return 2

    # the xpath is invalid
    if (crawltag == ''):
        return 3

    # user has not authorize us to access their google calendar
    if (add_to_calendar == '1' and user.profile.google_auth == False):
        return 4
    return 100
