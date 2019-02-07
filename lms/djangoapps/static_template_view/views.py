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
        "university": "Weizmann Institute of Science",
        "course": "PYSJ"
    },
    {
        "name": "Angela DePace",
        "videoURL": "https://youtube.com/embed/_pZl7pofC9s",
        "speaker_slug": "angela-depace",
        "suffix": "Ph.D.",
        "title": "Associate Professor, Systems Biology",
        "university": "Harvard Medical School",
        "course": "PYSJ"
    },
    {
        "name": "Tejal Desai",
        "videoURL": "https://youtube.com/embed/XD2IxKd1PT0",
        "speaker_slug": "tejal-desai",
        "suffix": "Ph.D.",
        "title": "Professor, Bioengineering and Therapeutic Sciences",
        "university": "University of California, San Francisco",
        "course": "PYSJ"
    },
    {
        "name": "Cynthia Fuhrmann",
        "videoURL": "https://youtube.com/embed/JfYTL0LLhlQ",
        "speaker_slug": "cynthia-fuhrmann",
        "suffix": "Ph.D.",
        "title": "Assistant Dean for Career and Professional Development; Director, Center for Biomedical Career Development",
        "university": "University of Massachusetts Medical School",
        "course": "PYSJ"
    },
    {
        "name": "Ryan Hernandez",
        "videoURL": "https://www.youtube.com/embed/kqZSbLBpcRQ",
        "speaker_slug": "ryan-hernandez",
        "suffix": "Ph.D.",
        "title": "Associate Professor, Systems Biology",
        "university": "University of California, San Francisco",
        "course": "PYSJ"
    },

    {
        "name": "Asia Matthew-Onabanjo",
        "videoURL": "https://www.youtube.com/embed/SWzZHnG-4rU",
        "speaker_slug": "asia-matthew-onabanjo",
        "suffix": "M.D./Ph.D. Candidate",
        "title": "Leslie Shaw Lab",
        "university": "University of Massachusetts Medical School",
        "course": "PYSJ"
    },
    {
        "name": "Kassandra Ori-McKenney",
        "videoURL": "https://www.youtube.com/embed/i-KvrBpW-2A",
        "speaker_slug": "kassie-ori-mckenney",
        "suffix": "Ph.D.",
        "title": "Assistant Professor, Molecular & Cellular Biology",
        "university": "University of California, Davis",
        "course": "PYSJ"
    },
    {
        "name": "Sabine Petry",
        "videoURL": "https://www.youtube.com/embed/kkK6_Akv9cw",
        "speaker_slug": "sabine-petry",
        "suffix": "Ph.D.",
        "title": "Assistant Professor, Molecular Biology ",
        "university": "Princeton University",
        "course": "PYSJ"
    },
    {
        "name": "Indira Raman",
        "videoURL": "https://www.youtube.com/embed/P0aWoY_FBOM",
        "speaker_slug": "indira-raman",
        "suffix": "Ph.D.",
        "title": "Professor, Neurobiology",
        "university": "Northwestern University",
        "course": "PYSJ"
    },
    {
        "name": "Randy Schekman",
        "videoURL": "https://www.youtube.com/embed/gdioxba2uXw",
        "speaker_slug": "randy-schekman",
        "suffix": "Ph.D.",
        "title": "Professor, Molecular & Cellular Biology; HHMI Investigator",
        "university": "University of California, Berkeley",
        "course": "PYSJ"
    },
    {
        "name": "Clarissa Scholes",
        "videoURL": "https://www.youtube.com/embed/JKY3nxYOGLU",
        "speaker_slug": "clarissa-scholes",
        "suffix": "Ph.D. Candidate",
        "title": "Angela DePace Lab",
        "university": "Harvard Medical School",
        "course": "PYSJ"
    },
    {
        "name": "Ben Vincent",
        "videoURL": "https://www.youtube.com/embed/rDGZkhlMRec",
        "speaker_slug": "ben-vincent",
        "suffix": "Ph.D. Candidate",
        "title": "Angela DePace Lab",
        "university": "Harvard Medical School",
        "course": "PYSJ"
    },
    {
        "name": "Keith Yamamoto",
        "videoURL": "https://www.youtube.com/embed/U3eN-SzdgKI",
        "speaker_slug": "keith-yamamoto",
        "suffix": "Ph.D.",
        "title": "Professor, Cellular & Molecular Pharmacology; Vice Chancellor for Science Policy and Strategy",
        "university": "University of California, San Francisco",
        "course": "PYSJ"
    },




    {
        "name": "Aimee Kao",
        "videoURL": None,
        "speaker_slug": "aimee-kao",
        "suffix": "Ph.D.",
        "title": "Associate Professor",
        "university": "University of California, San Francisco",
        "course": "BCLS"
    },
    {
        "name": "Anatol Kreitzer",
        "videoURL": None,
        "speaker_slug": "anatol-kreitzer",
        "suffix": "Ph.D.",
        "title": "Senior Investigator (Gladstone) and Associate Professor of Physiology and Neurology (UCSF)",
        "university": "Gladstone Institute of Neurological Disease / University of California, San Francisco",
        "course": "BCLS"
    },
    {
        "name": "Asha S. Collins",
        "videoURL": None,
        "speaker_slug": "asha-s-collins",
        "suffix": "Ph.D.",
        "title": "Vice President of U.S. Clinical Trial Sourcing",
        "university": "McKesson Corporation",
        "course": "BCLS"
    },
    {
        "name": "Christine Siu",
        "videoURL": None,
        "speaker_slug": "christine-siu",
        "suffix": "MBA",
        "title": "Chief Financial Officer",
        "university": "Eidos Therapeutics",
        "course": "BCLS"
    },
    {
        "name": "Daniel Dornbusch",
        "videoURL": None,
        "speaker_slug": "daniel-dornbusch",
        "suffix": "MS, MBA",
        "title": "Founder",
        "university": "KidsDOC; Acteris",
        "course": "BCLS"
    },
    {
        "name": "Deborah Dauber",
        "videoURL": None,
        "speaker_slug": "deborah-dauber",
        "suffix": "Ph.D.",
        "title": "",
        "university": "",
        "course": "BCLS"
    },
    {
        "name": "Girish Aakalu",
        "videoURL": None,
        "speaker_slug": "girish-aakalu",
        "suffix": "Ph.D.",
        "title": "Vice President and Head of Global Scientific Affairs & Scientific Intelligence",
        "university": "Ipsen",
        "course": "BCLS"
    },
    {
        "name": "JeShaune Jackson",
        "videoURL": None,
        "speaker_slug": "jeshaune-jackson",
        "suffix": "MS, MBA",
        "title": "Founder ",
        "university": "Bio-Diversity",
        "course": "BCLS"
    },
    {
        "name": "Jessica Tashker",
        "videoURL": None,
        "speaker_slug": "jessica-tashker",
        "suffix": "Ph.D.",
        "title": "Associate Director, Market Analysis and Strategy group",
        "university": "Genentech",
        "course": "BCLS"
    },
    {
        "name": "Sandra Waugh Ruggles",
        "videoURL": None,
        "speaker_slug": "sandra-waugh-ruggles",
        "suffix": "Ph.D.",
        "title": "",
        "university": "",
        "course": "BCLS"
    },


    {
        "name": "Prachee Avasthi",
        "videoURL": "https://www.youtube.com/embed/V0hklsjf1Yc",
        "speaker_slug": "prachee-avasthi",
        "suffix": "Ph.D.",
        "title": "Assistant Professor in Department of Anatomy and Cell Biology",
        "university": "Kansas University Medical Center",
        "course": "LE"
    },
    {
        "name": "Needhi Bhalla",
        "videoURL": "https://www.youtube.com/embed/uIv1H4Vxce8",
        "speaker_slug": "needhi-bhalla",
        "suffix": "Ph.D.",
        "title": "",
        "university": "University of California, Santa Cruz",
        "course": "LE"
    },
    {
        "name": u"Daniel Colón-Ramos",
        "videoURL": "https://www.youtube.com/embed/5WVUOsnr8jA",
        "speaker_slug": "daniel-colon-ramos",
        "suffix": "Ph.D.",
        "title": "",
        "university": "Yale School of Medicine",
        "course": "LE"
    },
    {
        "name": "Doug Koshland",
        "videoURL": "https://www.youtube.com/embed/zSqGvoHjVUA",
        "speaker_slug": "doug-koshland",
        "suffix": "Ph.D.",
        "title": "",
        "university": "University of California, Berkeley",
        "course": "LE"
    },
    {
        "name": "Katie Pollard",
        "videoURL": "https://www.youtube.com/embed/1CHoHKX1vy8",
        "speaker_slug": "katie-pollard",
        "suffix": "Ph.D.",
        "title": "",
        "university": "Gladstone Institute",
        "course": "LE"
    },
    {
        "name": "Neil Robbins III",
        "videoURL": "https://www.youtube.com/embed/Zno5C0SRtAg",
        "speaker_slug": "neil-robbins-III",
        "suffix": "Ph.D.",
        "title": "",
        "university": "Stanford University",
        "course": "LE"
    },
    {
        "name": "Ana Ruiz Saenz",
        "videoURL": "https://www.youtube.com/embed/w5vDdQTX45g",
        "speaker_slug": "ana-ruiz-saenz",
        "suffix": "Ph.D.",
        "title": "",
        "university": "University of California, San Francisco",
        "course": "LE"
    },
    {
        "name": "Paul Turner",
        "videoURL": "https://www.youtube.com/embed/TxQXo3XNg2w",
        "speaker_slug": "paul-turner",
        "suffix": "Ph.D.",
        "title": "",
        "university": "Yale University",
        "course": "LE"
    },
    {
        "name": "Ron Vale",
        "videoURL": "https://www.youtube.com/embed/ASkKRvK20to",
        "speaker_slug": "ron-vale",
        "suffix": "Ph.D.",
        "title": "Professor of the Department of Cellular and Molecular Pharmacology; HHMI Investigator",
        "university": "University of California, San Francisco",
        "course": "LE"
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
