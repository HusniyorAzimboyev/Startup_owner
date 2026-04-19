import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import StartupProfile
from apps.tasks.models import Task

logger = logging.getLogger(__name__)

# AI Response Generator
def generate_ai_response(user, message):
    """Generate AI responses based on user message"""
    message_lower = message.lower()
    
    # Get user context
    try:
        startup = StartupProfile.objects.get(user=user)
        startup_name = startup.name
        stage = startup.get_stage_display()
    except StartupProfile.DoesNotExist:
        startup_name = "your startup"
        stage = "unknown"
    
    # Task-related queries
    if any(word in message_lower for word in ['task', 'todo', 'do', 'work']):
        pending = Task.objects.filter(user=user, status='todo').count()
        in_progress = Task.objects.filter(user=user, status='in_progress').count()
        return f"📋 You have {pending} tasks pending and {in_progress} in progress. I recommend focusing on high-priority items first. Would you like help organizing your tasks?"
    
    # Mentor/mentorship queries
    if any(word in message_lower for word in ['mentor', 'help', 'advice', 'guidance', 'feedback']):
        return f"🎓 Great question! For {startup_name} at the {stage} stage, I recommend:\n\n1. **Find mentors** in your industry\n2. **Schedule regular sessions** to stay on track\n3. **Take notes** on their feedback\n4. **Act on advice** consistently\n\nWould you like me to help you find a mentor?"
    
    # Progress/metrics queries
    if any(word in message_lower for word in ['progress', 'metrics', 'metrics', 'track', 'growing']):
        return f"📈 Progress tracking is crucial! For {startup_name}:\n\n✅ Set clear KPIs\n✅ Track daily metrics\n✅ Review weekly\n✅ Adjust strategy\n\nVisit your Progress Dashboard to see your completion rates and trends."
    
    # Investor/funding queries
    if any(word in message_lower for word in ['investor', 'fund', 'funding', 'pitch', 'money']):
        return f"💰 Fundraising tips for {startup_name}:\n\n1. **Perfect your pitch deck**\n2. **Know your numbers** (revenue, growth rate)\n3. **Network actively** with investors\n4. **Prepare for due diligence**\n5. **Have a clear growth plan**\n\nCheck the Investors section to connect with potential investors!"
    
    # Stage-specific advice
    if any(word in message_lower for word in ['stage', 'phase', 'growth', 'scaling', 'expand']):
        if stage.lower() == 'idea':
            return f"💡 For an Idea stage startup:\n\n✅ Validate your market\n✅ Build MVP quickly\n✅ Get customer feedback\n✅ Plan your next steps\n\nFocus on learning and rapid iteration!"
        elif stage.lower() == 'mvp':
            return f"🛠️ For an MVP stage startup:\n\n✅ Refine based on user feedback\n✅ Find product-market fit\n✅ Build your first users\n✅ Plan for scaling\n\nSpeed and user feedback are key!"
        else:
            return f"🚀 For a Growth stage startup:\n\n✅ Scale operations\n✅ Expand to new markets\n✅ Optimize unit economics\n✅ Build your team\n\nFocus on sustainable growth!"
    
    # General startup advice
    if any(word in message_lower for word in ['help', 'suggest', 'what', 'how', 'best']):
        return f"🚀 For {startup_name}, here's my advice:\n\n1. **Stay focused** on your core mission\n2. **Communicate** with your team/mentors\n3. **Track metrics** religiously\n4. **Iterate quickly** based on feedback\n5. **Celebrate wins** no matter how small\n\nWhat specific area would you like help with?"
    
    # Default response
    return f"💭 Interesting question about {startup_name}! I'm here to help with:\n\n📋 Task management\n🎓 Mentor guidance\n📈 Progress tracking\n💰 Fundraising tips\n🚀 Growth strategies\n\nAsk me anything about your startup journey!"


@login_required
@require_http_methods(["POST"])
def chat(request):
    """Handle AI chat requests"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'error': 'Message cannot be empty',
                'response': 'Please enter a message to continue.'
            }, status=400)
        
        # Generate AI response
        response = generate_ai_response(request.user, message)
        
        return JsonResponse({
            'success': True,
            'response': response
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON',
            'response': 'Please send a valid message format.'
        }, status=400)
    
    except Exception as e:
        logger.exception(f'Error in AI chat for user {request.user.id}: {e}')
        return JsonResponse({
            'error': str(e),
            'response': 'Sorry, I encountered an error. Please try again.'
        }, status=500)
