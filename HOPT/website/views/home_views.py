from django.shortcuts import render

# Trang chủ
def Home(request):
    return render(request, 'index.html')
