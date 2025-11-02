from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import logging

from .models import Lead
from .serializers import LeadSerializer

logger = logging.getLogger(__name__)


class BusinessEvaluationView(APIView):
    """
    API endpoint to handle business valuation form submissions.
    
    POST /api/business-evaluation/
    """
    
    def post(self, request, *args, **kwargs):
        """
        Create a new lead from business evaluation form submission.
        
        Returns:
            - 201 Created: Lead successfully created
            - 400 Bad Request: Validation errors
            - 500 Internal Server Error: Database errors
        """
        serializer = LeadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    lead = serializer.save()
                    
                    logger.info(
                        f"New lead created: ID={lead.id}, "
                        f"Name={lead.name}, Email={lead.email}, "
                        f"Valuation: {lead.valuation_low:.0f} - {lead.valuation_high:.0f}"
                    )
                
                # Return lead data with valuation
                response_serializer = LeadSerializer(lead)
                return Response(
                    {
                        'id': lead.id,
                        'message': 'Business valuation request submitted successfully',
                        'submitted_at': lead.submitted_at.isoformat(),
                        'valuation': response_serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                logger.error(f"Error creating lead: {str(e)}", exc_info=True)
                return Response(
                    {
                        'error': 'Failed to save lead',
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

