# coding: utf-8


from django.core.urlresolvers import reverse
from django.core.xheaders import populate_xheaders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader, RequestContext, Template
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import redirect_to_login
from django_quickstartup.quickstartup.forms import CustomPasswordResetForm

from .models import Page


DEFAULT_TEMPLATE = 'website/page.html'


@csrf_protect
def website_page(request, url):
    if not url.startswith('/'):
        url = '/' + url

    if not url.endswith('/'):
        url += "/"

    page = get_object_or_404(Page, url__exact=url)

    if page.registration_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    page_context = RequestContext(request, {'page': page})

    context = RequestContext(request, {
        'page': page,
        'title': Template(page.title).render(page_context),
        'content': Template(page.content).render(page_context),
    })

    if page.template_name:
        template = loader.select_template((page.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    response = HttpResponse(template.render(context))
    populate_xheaders(request, response, Page, page.id)
    return response


def boilerplate(request, *args, **kwargs):
    return render(request, "website/page.html", kwargs)


def dashboard(request, *args, **kwargs):
    return render(request, "app/dashboard.html", kwargs)


def profile(request, *args, **kwargs):
    return render(request, "app/profile.html", kwargs)


@csrf_protect
def password_reset(request, post_reset_redirect=None, form_class=CustomPasswordResetForm,
                   template_name="website/reset.html",
                   subject_template_name="website/password-reset-subject.txt",
                   email_template_name="website/password-reset-email.txt",
                   html_email_template_name="website/password-reset-email.html"):

    if post_reset_redirect is None:
        post_reset_redirect = reverse("password-reset-done")

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            context = RequestContext(request)
            form.notify(
                context=context,
                token_generator=default_token_generator,
                subject_template_name=subject_template_name,
                email_template_name=email_template_name,
                html_email_template_name=html_email_template_name,
                use_https=request.is_secure(),
            )
            return redirect(post_reset_redirect)
    else:
        form = form_class()

    return render(request, template_name, {'form': form})
