from django.shortcuts import render


def art_list(request):
    return render(request, 'mobile_list.html', {})
