from rest_framework import serializers
from decimal import Decimal

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
            # Sector Information
            'shareholders_working_in_business',
            'taking_full_market_salary',
            'salary_adjustment',
            'property_own_or_rent',
            'property_market_rent_adjustment',
            'company_sector',
            'adjust_industry_multipliers',
            'lower_multiplier',
            'upper_multiplier',
            'purpose',
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
            # Contact Information
            'name',
            'email',
            'phone',
            'company_name',
            'company_number',
            # Valuation Information (read-only)
            'valuation_low',
            'valuation_high',
            'sde',
        ]
        read_only_fields = ['valuation_low', 'valuation_high', 'sde']
        extra_kwargs = {
            'shareholders_working_in_business': {'required': True},
            'property_own_or_rent': {'required': True},
            'company_sector': {'required': True},
            'adjust_industry_multipliers': {'required': True},
            'lower_multiplier': {'required': True},
            'upper_multiplier': {'required': True},
            'turnover': {'required': True},
            'predicted_turnover': {'required': True},
            'profit': {'required': True},
            'predicted_profit': {'required': True},
            'non_recurring_expenses': {'required': True},
            'interest_payable': {'required': True},
            'interest_receivable': {'required': True},
            'depreciation': {'required': True},
            'amortisation': {'required': True},
            'net_assets': {'required': True},
            'name': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'company_name': {'required': True},
            'company_number': {'required': True},
        }
        
    def validate(self, data):
        """
        Object-level validation for conditional requirements
        """
        # Check if shareholders are working in the business
        shareholders_working = data.get('shareholders_working_in_business', False)
        
        if shareholders_working:
            # If shareholders are working, taking_full_market_salary is required
            if 'taking_full_market_salary' not in data:
                raise serializers.ValidationError({
                    'taking_full_market_salary': 'This field is required when shareholders are working in the business.'
                })
            
            # If not taking full market salary, salary_adjustment is required
            if not data.get('taking_full_market_salary', True):
                if not data.get('salary_adjustment'):
                    raise serializers.ValidationError({
                        'salary_adjustment': 'This field is required when not taking full market salary.'
                    })
        
        # Validate property_market_rent_adjustment when property is rented
        if data.get('property_own_or_rent') == 'Rent':
            if not data.get('property_market_rent_adjustment'):
                raise serializers.ValidationError({
                    'property_market_rent_adjustment': 'This field is required when property is rented.'
                })
        
        return data

    def validate_email(self, value):
        """Validate email format."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value
    
    def validate_property_own_or_rent(self, value):
        """Validate property_own_or_rent choice."""
        valid_choices = ['Own', 'Rent']
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
        # Create instance without saving
        lead = Lead(**validated_data)
        
        # Calculate valuation
        valuation_data = calculate_valuation(lead)
        lead.valuation_low = valuation_data['low']
        lead.valuation_high = valuation_data['high']
        lead.sde = valuation_data['sde']
        
        # Save once with all data
        lead.save()
        return lead
