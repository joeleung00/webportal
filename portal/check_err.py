from urllib import request
def check_no_repeat_name(request, categories):
    new_category_title = request.POST['new_cate_title']
    for category in categories:
        if (new_category_title == category.title):
            return False
    return True

def check_input_error(url, msg_title, crawltag, add_to_calendar, user):
    if (msg_title == ''):
        return  0

    try:
        request.urlopen(url)
        print("sucess")
    except:
        print("url error")
        return 2

    if (crawltag == ''):
        return 3

    if (add_to_calendar == '1' and user.profile.google_auth == False):
        return 4
    return 100
