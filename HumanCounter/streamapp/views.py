
from django.shortcuts import render
from .models import EntryExitCount

def live_count(request):
    entry_count = EntryExitCount.objects.filter(type='Entry').count()
    exit_count = EntryExitCount.objects.filter(type='Exit').count()
    context = {
        'entry_count': entry_count,
        'exit_count': exit_count,
    }
    
    return render(request, 'live_count.html',context)