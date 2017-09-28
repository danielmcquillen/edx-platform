# View for semi-static templatized content.
#
# List of valid templates is explicitly managed for (short-term)
# security reasons.

import mimetypes

from edxmako.shortcuts import render_to_response, render_to_string
from mako.exceptions import TopLevelLookupException
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.views.decorators.csrf import ensure_csrf_cookie

from util.cache import cache_if_anonymous

valid_templates = []

# iBio:
# Temporary location of iBio Speakers until I'm able to create
# a proper Django app

ibio_speaker_arr = [

    {
        "name": "Uri Alon",
        "videoURL": "https://youtube.com/embed/1nDOrWetd6s",
        "speaker_slug": "uri-alon",
        "suffix": "Ph.D.",
        "title": "Professor, Molecular Cell Biology",
        "university": "Weizmann Institute of Science"
    },
    {
        "name": "Angela DePace",
        "videoURL": "https://youtube.com/embed/_pZl7pofC9s",
        "speaker_slug": "angela-depace",
        "suffix": "Ph.D.",
        "title": "Associate Professor, Systems Biology",
        "university": "Harvard Medical School"
    },
    {
        "name": "Tejal Desai",
        "videoURL": "https://youtube.com/embed/XD2IxKd1PT0",
        "speaker_slug": "tejal-desai",
        "suffix": "Ph.D.",
        "title": "Professor, Bioengineering and Therapeutic Sciences",
        "university": "University of California, San Francisco"
    },
    {
        "name": "Cynthia Fuhrmann",
        "videoURL": "https://youtube.com/embed/JfYTL0LLhlQ",
        "speaker_slug": "cynthia-fuhrmann",
        "suffix": "Ph.D.",
        "title": "Assistant Dean for Career and Professional Development; Director, Center for Biomedical Career Development",
        "university": "University of Massachusetts Medical School"
    },
    {
        "name": "Ryan Hernandez",
        "videoURL": "https://www.youtube.com/embed/kqZSbLBpcRQ",
        "speaker_slug": "ryan-hernandez",
        "suffix": "Ph.D.",
        "title": "Associate Professor, Systems Biology",
        "university": "University of California, San Francisco"
    },

    {
        "name": "Asia Matthew-Onabanjo",
        "videoURL": "https://www.youtube.com/embed/SWzZHnG-4rU",
        "speaker_slug": "asia-matthew-onabanjo",
        "suffix": "M.D./Ph.D. Candidate",
        "title": "Leslie Shaw Lab",
        "university": "University of Massachusetts Medical School"
    },
    {
        "name": "Kassandra Ori-McKenney",
        "videoURL": "https://www.youtube.com/embed/i-KvrBpW-2A",
        "speaker_slug": "kassie-ori-mckenney",
        "suffix": "Ph.D.",
        "title": "Assistant Professor, Molecular & Cellular Biology",
        "university": "University of California, Davis"
    },
    {
        "name": "Sabine Petry",
        "videoURL": "https://www.youtube.com/embed/kkK6_Akv9cw",
        "speaker_slug": "sabine-petry",
        "suffix": "Ph.D.",
        "title": "Assistant Professor, Molecular Biology ",
        "university": "Princeton University",
    },
    {
        "name": "Indira Raman",
        "videoURL": "https://www.youtube.com/embed/P0aWoY_FBOM",
        "speaker_slug": "indira-raman",
        "suffix": "Ph.D.",
        "title": "Professor, Neurobiology",
        "university": "Northwestern University"
    },
    {
        "name": "Randy Schekman",
        "videoURL": "https://www.youtube.com/embed/gdioxba2uXw",
        "speaker_slug": "randy-schekman",
        "suffix": "Ph.D.",
        "title": "Professor, Molecular & Cellular Biology; HHMI Investigator",
        "university": "University of California, Berkeley"
    },
    {
        "name": "Clarissa Scholes",
        "videoURL": "https://www.youtube.com/embed/JKY3nxYOGLU",
        "speaker_slug": "clarissa-scholes",
        "suffix": "Ph.D. Candidate",
        "title": "Angela DePace Lab",
        "university": "Harvard Medical School"
    },
    {
        "name": "Ben Vincent",
        "videoURL": "https://www.youtube.com/embed/rDGZkhlMRec",
        "speaker_slug": "ben-vincent",
        "suffix": "Ph.D. Candidate",
        "title": "Angela DePace Lab",
        "university": "Harvard Medical School"
    },
    {
        "name": "Keith Yamamoto",
        "videoURL": "https://www.youtube.com/embed/U3eN-SzdgKI",
        "speaker_slug": "keith-yamamoto",
        "suffix": "Ph.D.",
        "title": "Professor, Cellular & Molecular Pharmacology; Vice Chancellor for Science Policy and Strategy",
        "university": "University of California, San Francisco"
    },

]



if settings.STATIC_GRAB:
    valid_templates = valid_templates + [
        'server-down.html',
        'server-error.html'
        'server-overloaded.html',
    ]


def index(request, template):
    if template in valid_templates:
        return render_to_response('static_templates/' + template, {})
    else:
        return redirect('/')


@ensure_csrf_cookie
@cache_if_anonymous()
def ibio_speakers(request):
    try:
        return render_to_response('static_templates/ibio-speakers.html', {'ibio_speaker_arr': ibio_speaker_arr})
    except TopLevelLookupException:
        raise Http404

@ensure_csrf_cookie
@cache_if_anonymous()
def ibio_newsletter_signup_complete(request):
    try:
        return render_to_response('static_templates/ibio-newsletter-signup-complete.html', {})
    except TopLevelLookupException:
        raise Http404

@ensure_csrf_cookie
@cache_if_anonymous()
def ibio_trainer_info(request):
    try:
        return render_to_response('static_templates/ibio-trainer-info.html', {})
    except TopLevelLookupException:
        raise Http404




@ensure_csrf_cookie
@cache_if_anonymous()
def ibio_speaker(request, slug):
    """
    Show the speaker's bio page if present, otherwise return a 404.
    At a later point "Speaker Bios" should be a proper Django app,
    but for now we'll rely on a simple data structure stored in this class.

    :param request:
    :param slug:     a slug for the speaker's name
    :return:
    """
    speaker = next((x for x in ibio_speaker_arr if x['speaker_slug'] == slug), None)

    if not speaker:
        raise Http404

    try:
        return render_to_response('static_templates/ibio-speakers/' + slug +'.html', {'ibio_speaker': speaker})
    except TopLevelLookupException:
        raise Http404


@ensure_csrf_cookie
@cache_if_anonymous()
def render(request, template):
    """
    This view function renders the template sent without checking that it
    exists. Do not expose template as a regex part of the url. The user should
    not be able to ender any arbitray template name. The correct usage would be:

    url(r'^jobs$', 'static_template_view.views.render', {'template': 'jobs.html'}, name="jobs")
    """

    # Guess content type from file extension
    content_type, __ = mimetypes.guess_type(template)

    try:
        return render_to_response('static_templates/' + template, {}, content_type=content_type)
    except TopLevelLookupException:
        raise Http404


@ensure_csrf_cookie
@cache_if_anonymous()
def render_press_release(request, slug):
    """
    Render a press release given a slug.  Similar to the "render" function above,
    but takes a slug and does a basic conversion to convert it to a template file.
    a) all lower case,
    b) convert dashes to underscores, and
    c) appending ".html"
    """
    template = slug.lower().replace('-', '_') + ".html"
    try:
        resp = render_to_response('static_templates/press_releases/' + template, {})
    except TopLevelLookupException:
        raise Http404
    else:
        return resp


def render_404(request):
    return HttpResponseNotFound(render_to_string('static_templates/404.html', {}, request=request))


def render_500(request):
    return HttpResponseServerError(render_to_string('static_templates/server-error.html', {}, request=request))
