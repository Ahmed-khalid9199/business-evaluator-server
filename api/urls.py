from django.urls import path
from .views import BusinessEvaluationView

app_name = 'api'

urlpatterns = [
    path('business-evaluation/', BusinessEvaluationView.as_view(), name='business-evaluation-create'),
    path('business-evaluation/<str:session_id>/', BusinessEvaluationView.as_view(), name='business-evaluation-update'),
]

