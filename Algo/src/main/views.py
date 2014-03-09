# coding=utf-8
import string
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, Http404, redirect
from django.views.decorators.csrf import csrf_exempt
import random
from main.models import AlgorithmModel, LanguageModel, ImplementationModel, TagModel, UserProfile


def home(request):
    algorithms = AlgorithmModel.objects \
        .prefetch_related('implementations__language', 'tags') \
        .filter(verified=True)
    tags = set()
    for algorithm in algorithms:
        for tag in algorithm.tags.all():
            tags.add(tag)
    tags = list(tags)
    tags.sort(key=lambda c: c.name)
    for tag in tags:
        tag.items = sorted([algo for algo in algorithms if tag in algo.tags.all()], key=lambda c: c.name)
    return render_to_response('home.html', {
        'algorithms': algorithms,
        'tags': tags,
        'popular_languages': list(LanguageModel.objects.all()[:7]),
    }, context_instance=RequestContext(request))


def standard_algorithm(request, algo_id, language_code=None):
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if language_code:
        implementations = algorithm.implementations.filter(language__slug=language_code.lower())
        if not implementations:
            print 'too bad'
            raise Http404
    else:
        implementations = algorithm.implementations.all()[:1]
    implementation = implementations[0]
    all_tags = [tag.name for tag in TagModel.objects.all()]
    languages = list(LanguageModel.objects.all()[:7])
    if implementation.language in languages:
        languages.remove(implementation.language)
    implementations = list(algorithm.implementations.all())
    if implementation in implementations:
        implementations.remove(implementation)
    not_implemented = list(LanguageModel.objects.all())
    for item in algorithm.implementations.all():
        for candidate in list(not_implemented):
            if candidate.id == item.language_id:
                not_implemented.remove(candidate)
                break

    more_not_implemented = len(not_implemented) > 7
    not_implemented.sort(key=lambda i: i.index, reverse=True)
    not_implemented = not_implemented[:7]
    response = render_to_response('standard_algorithm.html', {
        'algorithm': algorithm,
        'implementation': implementation,
        'implementations': implementations,
        'source': implementation.source or '\n\n\n\n\n\n\n\n\n\n\n\n',
        'family': implementation.language.family,
        'language': implementation.language.lexer or implementation.language.family,
        'tags': [tag.name for tag in algorithm.tags.all()],
        'all_tags': all_tags,
        'can_save': get_can_save(request, algorithm),
        'popular_languages': languages,
        'not_implemented': not_implemented,
        'more_not_implemented': more_not_implemented,
    }, context_instance=RequestContext(request))
    response.set_cookie('key', get_user_key(request))
    return response


def create_algorithm_with_language(request, language_id):
    language = get_object_or_404(LanguageModel, pk=language_id)
    algorithm = AlgorithmModel()
    algorithm.key = get_user_key(request)
    algorithm.save()
    implementation = ImplementationModel(algorithm=algorithm, language=language, source=language.example_code)
    implementation.save()
    return redirect('/fork/%s' % algorithm.id)


def create_algorithm(request):
    languages = LanguageModel.objects.order_by('-index', 'name').all()
    return render_to_response('create_algorithm.html', {
        'languages': languages,
    }, context_instance=RequestContext(request))


def implement_algorithm_with_language(request, algo_id, language_id):
    language = get_object_or_404(LanguageModel, pk=language_id)
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if not get_can_save(request, algorithm):
        fork_of_id = algorithm.id
        tags = algorithm.tags.all()
        algorithm.id = None
        algorithm.key = get_user_key(request)
        algorithm.fork_of_id = fork_of_id
        algorithm.name = "Fork of %s" % algorithm.name
        algorithm.verified = False
        algorithm.verification_request = False
        algorithm.merge_request = False
        algorithm.save()

        for tag in tags:
            tag.algorithms.add(algorithm)
            tag.save()
        algorithm.save()

    implementation = ImplementationModel(algorithm=algorithm, language=language, source=language.example_code)
    implementation.save()
    return redirect('/fork/%s/%s' % (algorithm.id, language.slug))


def implement_algorithm(request, algo_id):
    languages = LanguageModel.objects.order_by('-index', 'name').all()
    return render_to_response('implement_algorithm.html', {
        'languages': languages,
        'algo_id': algo_id,
    }, context_instance=RequestContext(request))


@csrf_exempt
def request_become_standard(request):
    if request.method != "POST":
        raise Http404
    algo_id = int(request.POST['algo_id'])
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if not get_can_save(request, algorithm):
        raise Http404

    algorithm.verification_request = True
    algorithm.save()

    return HttpResponse("accepted")


@csrf_exempt
def request_merge(request):
    if request.method != "POST":
        raise Http404
    algo_id = int(request.POST['algo_id'])
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if not get_can_save(request, algorithm) or not algorithm.fork_of_id:
        raise Http404

    algorithm.merge_request = True
    algorithm.save()

    return HttpResponse("accepted")


@csrf_exempt
def merge_algorithm(request):
    if request.method != "POST":
        raise Http404
    algo_id = int(request.POST['algo_id'])
    merge_id = int(request.POST['merge_id'])
    ok = request.POST['ok'] == 'yes'
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if not get_can_save(request, algorithm):
        raise Http404

    merge = get_object_or_404(AlgorithmModel, pk=merge_id)

    merge.merge_request = False
    merge.save()

    if ok:
        existing_languages = {impl.language_id for impl in algorithm.implementations.all()}
        for implementation in merge.implementations.all():
            if implementation.language_id not in existing_languages:
                implementation.id = None
                implementation.algorithm_id = algo_id
                implementation.save()

        return HttpResponse("merged")
    else:
        return HttpResponse("accepted")

@csrf_exempt
def save_algorithm(request):
    if request.method != "POST":
        raise Http404
    algo_id = int(request.POST['algo_id'])
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if not get_can_save(request, algorithm):
        raise Http404

    implementation_id = int(request.POST['code_id'])
    implementation = get_object_or_404(ImplementationModel, pk=implementation_id)
    if implementation.algorithm.id != algo_id:
        raise Http404

    algorithm.name = request.POST['name']
    algorithm.description = request.POST['description']
    algorithm.save()
    implementation.source = request.POST['source']
    implementation.save()

    tags = [name.strip() for name in (request.POST['tags'] or "").split(',')]
    existing = algorithm.tags.all()
    existing_names = [i.name for i in existing]
    for tag in existing:
        if tag.name not in tags:
            algorithm.tags.remove(tag)
    for tag in tags:
        if tag not in existing_names:
            t, is_new = TagModel.objects.get_or_create(name=tag)
            if is_new:
                t.save()
            algorithm.tags.add(t)
    algorithm.save()

    return HttpResponse('saved')

@csrf_exempt
def fork_algorithm(request):
    if request.method != "POST":
        raise Http404
    algo_id = int(request.POST['algo_id'])
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    implementation_id = int(request.POST['code_id'])
    implementation = get_object_or_404(ImplementationModel, pk=implementation_id)
    if implementation.algorithm.id != algo_id:
        raise Http404

    fork_of_id = algorithm.id
    algorithm.id = None
    algorithm.key = get_user_key(request)
    algorithm.fork_of_id = fork_of_id
    algorithm.name = "Fork of %s" % request.POST['name']
    algorithm.description = request.POST['description']
    algorithm.verified = False
    algorithm.verification_request = False
    algorithm.merge_request = False
    algorithm.save()
    implementation.id = None
    implementation.algorithm = algorithm
    implementation.source = request.POST['source']
    implementation.save()

    tags = [name.strip() for name in (request.POST['tags'] or "").split(',')]
    existing = algorithm.tags.all()
    existing_names = [i.name for i in existing]
    for tag in existing:
        if tag.name not in tags:
            algorithm.tags.remove(tag)
    for tag in tags:
        if tag not in existing_names:
            t, is_new = TagModel.objects.get_or_create(name=tag)
            if is_new:
                t.save()
            algorithm.tags.add(t)
    algorithm.save()

    return HttpResponse(algorithm.id)


def generate_key(length=64):
    return ''.join(random.choice(string.printable) for i in xrange(length))


def get_user_key(request):
    if request.user.is_authenticated():
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created:
            profile.key = generate_key()
            profile.save()
        key = profile.key
    else:
        key = request.COOKIES.get('key', generate_key())
    return key


def get_can_save(request, algorithm):
    key = get_user_key(request)
    can_save = request.user.is_superuser or key == algorithm.key
    return can_save


def user_algorithm(request, algo_id, language_code=None):
    algorithm = get_object_or_404(AlgorithmModel, pk=algo_id)
    if language_code:
        implementations = algorithm.implementations.filter(language__slug=language_code.lower())
        if not implementations:
            print 'too bad'
            raise Http404
    else:
        implementations = algorithm.implementations.all()[:1]
    implementation = implementations[0]
    all_tags = [tag.name for tag in TagModel.objects.all()]
    languages = list(LanguageModel.objects.all()[:7])
    if implementation.language in languages:
        languages.remove(implementation.language)
    implementations = list(algorithm.implementations.all())
    if implementation in implementations:
        implementations.remove(implementation)
    not_implemented = list(LanguageModel.objects.all())
    for item in algorithm.implementations.all():
        for candidate in list(not_implemented):
            if candidate.id == item.language_id:
                not_implemented.remove(candidate)
                break

    can_save = get_can_save(request, algorithm)
    if can_save:
        merge_requests = algorithm.forks.filter(merge_request=True)
    else:
        merge_requests = []

    more_not_implemented = len(not_implemented) > 7
    not_implemented.sort(key=lambda i: i.index, reverse=True)
    not_implemented = not_implemented[:7]
    response = render_to_response('user_algorithm.html', {
        'algorithm': algorithm,
        'implementation': implementation,
        'implementations': implementations,
        'source': implementation.source or '\n\n\n\n\n\n\n\n\n\n\n\n',
        'family': implementation.language.family,
        'language': implementation.language.lexer or implementation.language.family,
        'tags': [tag.name for tag in algorithm.tags.all()],
        'all_tags': all_tags,
        'can_save': can_save,
        'merge_requests': merge_requests,
        'popular_languages': languages,
        'not_implemented': not_implemented,
        'more_not_implemented': more_not_implemented,
    }, context_instance=RequestContext(request))
    response.set_cookie('key', get_user_key(request))
    return response

@csrf_exempt
def recognize_face(request):
    if request.method != "POST":
        raise Http404
    if 'photo' not in request.FILES:
        return HttpResponse("No file found")

    photo = request.FILES['photo']

    import cv2
    import cv2.cv as cv

    def detect(img, cascade_fn='haarcascades/haarcascade_frontalface_alt.xml',
               scaleFactor=1.3, minNeighbors=4, minSize=(20, 20),
               flags=cv.CV_HAAR_SCALE_IMAGE):

        cascade = cv2.CascadeClassifier(cascade_fn)
        rects = cascade.detectMultiScale(img, scaleFactor=scaleFactor,
                                         minNeighbors=minNeighbors,
                                         minSize=minSize, flags=flags)
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        return rects

    path = '/tmp/%s' % photo.name
    destination = open(path, 'wb+')

    for chunk in photo.chunks():
        destination.write(chunk)
    destination.close()

    img_color = cv2.imread(path)
    img_gray = cv2.cvtColor(img_color, cv.CV_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    rects = detect(img_gray)
    #print dir(rects[0])
    values = ["[%s, %s, %s, %s]" % (r[0], r[1], r[2], r[3]) for r in rects]
    #import json
    #response_data = json.dumps(rects)
    return HttpResponse(",".join(values))



def face_recognition(request):
    return render_to_response('face_recognition.html', {}, context_instance=RequestContext(request))