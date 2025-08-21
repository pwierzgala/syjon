from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _


def index(request):
    return redirect('merovingian:course:list')


@login_required
def management(request):
    return redirect('merovingian:management-list')


@login_required
def delete_confirm(request):
    if request.method == 'POST':
        if request.POST.get('action', '') == 'yes':
            return redirect(request.session.pop('confirm_yes', ''))
        elif request.POST.get('action', '') == 'no':
            return redirect(request.session.pop('confirm_no', ''))
    else:
        request.session['confirm_yes'] = request.GET.get('yes', '')
        request.session['confirm_no'] = request.GET.get('no', '')
        kwargs = {'text': _(u'Selected item will be removed. Are you sure?')}
        return render(request, 'merovingian/confirm.html', kwargs)
