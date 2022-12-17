from django.http import HttpResponseRedirect


def add_or_remove_favourite(request, prod_slug):

    if 'favourite' not in request.session:
        request.session['favourite'] = {}

    favourite = request.session.get('favourite')

    if prod_slug in favourite:
        del favourite[prod_slug]
    else:
        favourite[prod_slug] = 1

    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))