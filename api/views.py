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
    
    POST /api/business-evaluation/ - Create partial lead (contact info)
    PUT /api/business-evaluation/<session_id>/ - Update with complete data
    """
    
    def post(self, request, *args, **kwargs):
        """
        Create a partial lead with contact information.
        
        Returns:
            - 201 Created: Partial lead successfully created with session_id
            - 400 Bad Request: Validation errors
            - 500 Internal Server Error: Database errors
        """
        serializer = LeadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    lead = serializer.save()
                    
                    logger.info(
                        f"Partial lead created: ID={lead.id}, "
                        f"Session={lead.session_id}, "
                        f"Name={lead.name}, Email={lead.email}"
                    )
                
                # Return lead data with session_id
                response_serializer = LeadSerializer(lead)
                return Response(
                    {
                        'id': lead.id,
                        'session_id': lead.session_id,
                        'message': 'Contact information saved successfully',
                        'data': response_serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                logger.error(f"Error creating partial lead: {str(e)}", exc_info=True)
                return Response(
                    {
                        'error': 'Failed to save contact information',
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
    
    def put(self, request, session_id=None, *args, **kwargs):
        """
        Update existing lead with complete data and calculate valuation.
        
        Returns:
            - 200 OK: Lead successfully updated with valuation
            - 404 Not Found: Session ID not found
            - 400 Bad Request: Validation errors
            - 500 Internal Server Error: Database errors
        """
        if not session_id:
            return Response(
                {
                    'error': 'Session ID required',
                    'details': 'Please provide session_id in URL'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lead = Lead.objects.get(session_id=session_id)
        except Lead.DoesNotExist:
            return Response(
                {
                    'error': 'Lead not found',
                    'details': f'No lead found with session_id: {session_id}'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    lead = serializer.save()
                    
                    logger.info(
                        f"Lead completed: ID={lead.id}, "
                        f"Session={lead.session_id}, "
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
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                logger.error(f"Error updating lead: {str(e)}", exc_info=True)
                return Response(
                    {
                        'error': 'Failed to complete valuation',
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

