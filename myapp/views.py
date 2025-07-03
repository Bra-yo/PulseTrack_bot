from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.utils import analyze_sentiment, extract_topics
from django.http import JsonResponse
from django.utils import timezone
from .models import Feedback
from collections import Counter
from .twilio_utils import send_whatsapp_message
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm



@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        # Get employee message
        employee_msg = request.POST.get('Body', '')
        from_number = request.POST.get('From', '')

        # Analyze sentiment & topics
        sentiment = analyze_sentiment(employee_msg)
        topics = extract_topics(employee_msg)

        # Store raw feedback
        print(f"New feedback from {from_number}: {employee_msg}")

        # Save to DB
        Feedback.objects.create(
            message=employee_msg,
            sentiment_score=sentiment,
            detected_topics=topics
        )

        # Auto-reply to confirm receipt
        twilio_response = f"Thanks for your feedback! Your feedback is anonymous."
        return HttpResponse(twilio_response, content_type='text/plain')
    return HttpResponse("Invalid request", status=400)


def feedback_data_api(request):
    # Get last 7 days of feedback
    feedbacks = Feedback.objects.filter(
        timestamp__gte=timezone.now() - timezone.timedelta(days=7)
    )

    # Prepare sentiment trend data
    daily_avg = feedbacks.extra(
        select={'day': 'DATE(timestamp)'}
    ).values('day').annotate(avg_sentiment=Avg('sentiment_score'))

    # Count topics
    all_topics = [topic for fb in feedbacks for topic in fb.detected_topics]
    topic_counts = Counter(all_topics).most_common(5)

    return JsonResponse({
        'dates': [entry['day'] for entry in daily_avg],
        'sentiments': [entry['avg_sentiment'] for entry in daily_avg],
        'topics': [{'name': k, 'count': v} for k, v in topic_counts]
    })

def dashboard_view(request):
    return render(request, 'dashboard.html')

def send_test_message(request):
    # Example usage
    sid = send_whatsapp_message(
        to_number="+254748264302",
        template_variables={"1": "12/1", "2": "3pm"}
    )
    return HttpResponse(f"Message sent! SID: {sid}")

def is_hr(user):
    return user.groups.filter(name='HR').exists()

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign to HR group if it's the first user
            if User.objects.count() == 1:
                hr_group = Group.objects.get_or_create(name='HR')[0]
                user.groups.add(hr_group)
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@user_passes_test(is_hr)
def dashboard_view(request):
    return render(request, 'dashboard.html')