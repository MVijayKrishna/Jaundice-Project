# from django.shortcuts import render
# from .models import JaundiceCase

def home(request):
    return render(request, 'home.html')

# def explore(request):
#     cases = JaundiceCase.objects.all()
#     return render(request, 'explore.html', {'cases': cases})

from django.shortcuts import render
# from .models import JaundiceCase
# import random

# def explore(request):
#     all_cases = list(JaundiceCase.objects.all())
#     cases = random.sample(all_cases, min(30, len(all_cases)))
#     return render(request, 'explore.html', {'cases': cases})

# from django.db.models import Q
# import random

# def explore(request):
#     cases = JaundiceCase.objects.all()

#     ethnicity = request.GET.get('ethnicity')
    ## region = request.GET.get('region')
#     feeding = request.GET.get('feeding_pattern')

#     if ethnicity:
#         cases = cases.filter(ethnicity=ethnicity)
#     if region:
#         cases = cases.filter(region=region)
#     if feeding:
#         cases = cases.filter(feeding_pattern=feeding)

#     cases = list(cases)
#     random.shuffle(cases)
#     cases = cases[:30]

#     return render(request, 'explore.html', {'cases': cases})

from django.shortcuts import render
from django.db.models import Q
from .models import JaundiceCase  # Ensure this is correctly imported

def explore(request):
    ethnicity = request.GET.get('ethnicity')
    region = request.GET.get('region')
    feeding = request.GET.get('feeding')
    search_query = request.GET.get('q')

    cases = JaundiceCase.objects.all()

    if ethnicity:
        cases = cases.filter(ethnicity__iexact=ethnicity)
    if region:
        cases = cases.filter(region__iexact=region)
    if feeding:
        cases = cases.filter(feeding_pattern__iexact=feeding)

    if search_query:
        cases = cases.filter(
            Q(feeding_pattern__icontains=search_query) |
            Q(sleeping_pattern__icontains=search_query) |
            Q(stooling_pattern__icontains=search_query) |
            Q(urine_color__icontains=search_query) |
            Q(skin_color__icontains=search_query) |
            Q(eye_color__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    cases = cases.order_by('?')[:30]

    # Define dropdown options here
    ethnicities = ["Black", "Asian", "Mixed"]
    regions = ["Eyes", "Palms", "Feet", "Gums", "Tongue"]

    return render(request, 'explore.html', {
        'cases': cases,
        'ethnicities': ethnicities,
        'regions': regions,
        'request': request,
    })
















    

# from django.shortcuts import get_object_or_404

# def case_detail(request, pk):
#     case = get_object_or_404(JaundiceCase, pk=pk)
#     return render(request, 'case_detail.html', {'case': case})

from .models import JaundiceCase
from django.shortcuts import get_object_or_404, render
import random

def case_detail(request, pk):
    case = get_object_or_404(JaundiceCase, pk=pk)
    related_cases = list(JaundiceCase.objects.exclude(pk=pk))
    random.shuffle(related_cases)
    return render(request, 'case_detail.html', {
        'case': case,
        'related_cases': related_cases[:6]  # limit to 6 thumbnails
    })





def jaundice_checker(request):
    return render(request, 'jaundice_checker.html')


from django.core.files.storage import FileSystemStorage

def comparison_tool(request):
    image1_url = None
    image2_url = None

    if request.method == 'POST':
        fs = FileSystemStorage()

        if request.FILES.get('image1'):
            image1 = request.FILES['image1']
            filename1 = fs.save(f"comparisons/{image1.name}", image1)
            image1_url = fs.url(filename1)

        if request.FILES.get('image2'):
            image2 = request.FILES['image2']
            filename2 = fs.save(f"comparisons/{image2.name}", image2)
            image2_url = fs.url(filename2)

    return render(request, 'comparison_tool.html', {
        'image1_url': image1_url,
        'image2_url': image2_url
    })
