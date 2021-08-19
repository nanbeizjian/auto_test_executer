from django.http import HttpResponse
from basePage.common.basepage import *


def open_url(request):
    method = request.method
    current_url = ''
    try:
        if request.method=='GET':
            request_url=request.GET.get("request_url",None)
            print('start open url')
            my_base_page = BasePage(request_url)
            current_url = my_base_page.get_current_url()

    except:
        log_public('fail to open url')

    finally:
        my_base_page.quit_browser()
        return HttpResponse(current_url)
