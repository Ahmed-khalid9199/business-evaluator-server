from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Lead model.
    """
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'company_sector',
        'turnover',
        'profit',
        'valuation_low',
        'valuation_high',
        'submitted_at',
    ]
    list_filter = [
        'submitted_at',
        'property_own_or_rent',
        'shareholders_working_in_business',
        'spoken_to_accountant',
        'spoken_to_broker',
    ]
    search_fields = [
        'name',
        'email',
        'phone',
        'company_sector',
    ]
    readonly_fields = [
        'valuation_low',
        'valuation_high',
        'sde',
        'submitted_at',
        'updated_at',
    ]
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name', 'company_number')
        }),
        ('Sector Information', {
            'fields': (
                'company_sector',
                'shareholders_working_in_business',
                'taking_full_market_salary',
                'salary_adjustment',
                'property_own_or_rent',
                'property_market_rent_adjustment',
                'adjust_industry_multipliers',
                'lower_multiplier',
                'upper_multiplier',
                'purpose',
                'spoken_to_accountant',
                'spoken_to_broker',
            )
        }),
        ('Financial Information', {
            'fields': (
                'turnover',
                'predicted_turnover',
                'profit',
                'predicted_profit',
                'non_recurring_expenses',
                'interest_payable',
                'interest_receivable',
                'depreciation',
                'amortisation',
                'net_assets',
            ),
            'classes': ('collapse',)
        }),
        ('Valuation Information', {
            'fields': (
                'sde',
                'valuation_low',
                'valuation_high',
            ),
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

