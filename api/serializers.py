from rest_framework import serializers
from decimal import Decimal
import uuid

from api.utils import calculate_valuation
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer for Lead model:
    - Validates all required fields
    """
    
    class Meta:
        model = Lead
        fields = [
            # Session tracking
            'session_id',
            'is_complete',
            # Contact and Purpose Information (first step)
            'user_type',
            'purpose',
            'name',
            'email',
            'phone',
            'company_name',
            'company_number',
            # Buyer-specific fields
            'management_preference',
            # Sector/Business Information
            'shareholders_working_in_business',
            'taking_salary',
            'salary_adjustment',
            'property_own_or_rent',
            'property_market_rent_adjustment',
            'company_sector',
            'adjust_industry_multipliers',
            'lower_multiplier',
            'upper_multiplier',
            'spoken_to_accountant',
            'spoken_to_broker',
            # Financial Information
            'profit',
            'predicted_profit',
            'turnover',
            'predicted_turnover',
            'interest_payable',
            'interest_receivable',
            'non_recurring_expenses',
            'depreciation',
            'amortisation',
            'net_assets',
            # Valuation Information (read-only)
            'valuation_low',
            'valuation_high',
            'sde',
        ]
        read_only_fields = ['valuation_low', 'valuation_high', 'sde', 'is_complete']
        extra_kwargs = {
            # Contact fields - only required if not updating existing lead
            'name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'company_name': {'required': False},
            'company_number': {'required': False},
            'user_type': {'required': False},
            'purpose': {'required': False},
            # Business/Sector fields
            'property_own_or_rent': {'required': False},
            'company_sector': {'required': False},
            'adjust_industry_multipliers': {'required': False},
            'lower_multiplier': {'required': False},
            'upper_multiplier': {'required': False},
            'spoken_to_accountant': {'required': False},
            'spoken_to_broker': {'required': False},
            # Financial fields
            'turnover': {'required': False},
            'predicted_turnover': {'required': False},
            'profit': {'required': False},
            'predicted_profit': {'required': False},
            'non_recurring_expenses': {'required': False},
            'interest_payable': {'required': False},
            'interest_receivable': {'required': False},
            'depreciation': {'required': False},
            'amortisation': {'required': False},
            'net_assets': {'required': False},
        }
        
    def validate(self, data):
        """
        Object-level validation for conditional requirements based on user type.
        Validates based on whether this is a partial save (POST) or complete submission (PUT with all data).
        """
        # For updates (PUT), we validate if this appears to be a complete submission
        # Check if financial fields are provided - if yes, it's a complete submission
        is_update = self.instance is not None
        has_financial_data = any([
            data.get('turnover') is not None,
            data.get('profit') is not None,
            data.get('net_assets') is not None
        ])
        
        # Only validate complete submission requirements if this is an update with financial data
        if is_update and has_financial_data:
            # Get existing instance data to check combined values
            instance_data = {}
            if self.instance:
                for field in self.Meta.fields:
                    instance_data[field] = getattr(self.instance, field, None)
            
            # Merge instance data with new data
            combined_data = {**instance_data, **data}
            
            # Validate contact information
            required_contact_fields = ['name', 'email', 'phone', 'company_name', 'company_number', 'user_type', 'purpose']
            for field in required_contact_fields:
                if not combined_data.get(field):
                    raise serializers.ValidationError({
                        field: f'This field is required for complete submission.'
                    })
            
            # Validate business/sector fields
            required_business_fields = ['company_sector', 'property_own_or_rent', 'lower_multiplier', 'upper_multiplier']
            for field in required_business_fields:
                if not combined_data.get(field):
                    raise serializers.ValidationError({
                        field: f'This field is required for complete submission.'
                    })
            
            # Validate financial fields
            required_financial_fields = ['turnover', 'profit', 'predicted_turnover', 'predicted_profit', 
                                        'interest_payable', 'interest_receivable', 'non_recurring_expenses',
                                        'depreciation', 'amortisation', 'net_assets']
            for field in required_financial_fields:
                if combined_data.get(field) is None:
                    raise serializers.ValidationError({
                        field: f'This field is required for complete submission.'
                    })
            
            # Use combined_data for user_type validation
            user_type = combined_data.get('user_type', 'other')
        else:
            # For partial submissions, just use what's provided
            user_type = data.get('user_type', 'other')
            # Skip further validation for partial submissions
            return data
        
        user_type = combined_data.get('user_type', 'other')
        
        # Buyer-specific validation
        if user_type == 'buyer':
            management_preference = combined_data.get('management_preference')
            
            if not management_preference:
                raise serializers.ValidationError({
                    'management_preference': 'This field is required for buyers.'
                })
            
            # If buyer wants to run business themselves, salary is required
            if management_preference == 'run_myself':
                if not combined_data.get('salary_adjustment'):
                    raise serializers.ValidationError({
                        'salary_adjustment': 'This field is required when you plan to run the business yourself.'
                    })
            
            # If buyer wants retained management, check shareholder details
            if management_preference == 'retained_management':
                shareholders_working = combined_data.get('shareholders_working_in_business')
                
                if shareholders_working is None:
                    raise serializers.ValidationError({
                        'shareholders_working_in_business': 'This field is required for retained management.'
                    })
                
                if shareholders_working:
                    if combined_data.get('taking_salary') is None:
                        raise serializers.ValidationError({
                            'taking_salary': 'This field is required when shareholders are working in the business.'
                        })
                    
                    if combined_data.get('taking_salary'):
                        if not combined_data.get('salary_adjustment'):
                            raise serializers.ValidationError({
                                'salary_adjustment': 'This field is required when taking salary.'
                            })
        
        # Seller-specific validation (or non-buyer)
        else:
            # Check if shareholders are working in the business
            shareholders_working = combined_data.get('shareholders_working_in_business')
            
            if shareholders_working is None:
                raise serializers.ValidationError({
                    'shareholders_working_in_business': 'This field is required for sellers.'
                })
            
            if shareholders_working:
                if combined_data.get('taking_salary') is None:
                    raise serializers.ValidationError({
                        'taking_salary': 'This field is required when shareholders are working in the business.'
                    })
                
                if combined_data.get('taking_salary'):
                    if not combined_data.get('salary_adjustment'):
                        raise serializers.ValidationError({
                            'salary_adjustment': 'This field is required when taking salary.'
                        })
        
        # Common validation for property
        if combined_data.get('property_own_or_rent') == 'own':
            if not combined_data.get('property_market_rent_adjustment'):
                raise serializers.ValidationError({
                    'property_market_rent_adjustment': 'This field is required when property is owned.'
                })
        
        return data

    def validate_email(self, value):
        """Validate email format."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value
    
    def validate_property_own_or_rent(self, value):
        """Validate property_own_or_rent choice."""
        valid_choices = ['own', 'rent']
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"property_own_or_rent must be one of {valid_choices}."
            )
        return value
    
    def validate_lower_multiplier(self, value):
        """Validate lower multiplier is non-zero and positive."""
        if value <= 0:
            raise serializers.ValidationError("Lower multiplier must be a non-zero positive number.")
        return value
    
    def validate_upper_multiplier(self, value):
        """Validate upper multiplier is non-zero and positive."""
        if value <= 0:
            raise serializers.ValidationError("Upper multiplier must be a non-zero positive number.")
        return value
    
    def create(self, validated_data):
        """
        Create a new partial lead (contact info only).
        Generates session_id automatically.
        """
        # Generate unique session ID
        validated_data['session_id'] = str(uuid.uuid4())
        validated_data['is_complete'] = False
        lead = Lead.objects.create(**validated_data)
        return lead
    
    def update(self, instance, validated_data):
        """
        Update existing lead with complete data and calculate valuation.
        """
        # Update all fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        # Mark as complete
        instance.is_complete = True
        
        # Calculate valuation
        valuation_data = calculate_valuation(instance)
        instance.valuation_low = valuation_data['low']
        instance.valuation_high = valuation_data['high']
        instance.sde = valuation_data['sde']
        
        # Save once with all data
        instance.save()
        return instance
