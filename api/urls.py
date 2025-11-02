from django.urls import path
from .views import BusinessEvaluationView

app_name = 'api'

urlpatterns = [
    path('business-evaluation/', BusinessEvaluationView.as_view(), name='business-evaluation'),
]

