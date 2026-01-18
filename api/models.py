from django.db import models


class Lead(models.Model):
    """
    Lead model to store business valuation form submissions.
    """
    # Contact and Purpose Information (now first step)
    user_type = models.CharField(
        max_length=20,
        choices=[
            ('buyer', 'Buyer'),
            ('seller', 'Seller'),
            ('both', 'Both'),
            ('other', 'Other')
        ],
        default='other'
    )
    purpose = models.CharField(max_length=100)
    
    # Buyer-specific fields
    management_preference = models.CharField(
        max_length=30,
        choices=[
            ('retained_management', 'Retained Management'),
            ('run_myself', 'Run Myself')
        ],
        null=True,
        blank=True
    )
    
    # Sector Information (for sellers) / Business Information (for buyers)
    company_sector = models.CharField(max_length=100, null=True, blank=True)
    shareholders_working_in_business = models.BooleanField(default=False, null=True, blank=True)
    taking_salary = models.BooleanField(default=False, null=True, blank=True)
    salary_adjustment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    property_own_or_rent = models.CharField(
        max_length=10, 
        choices=[('own', 'own'), ('rent', 'rent')],
        null=True,
        blank=True
    )
    property_market_rent_adjustment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    adjust_industry_multipliers = models.BooleanField(default=False, null=True, blank=True)
    lower_multiplier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_multiplier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spoken_to_accountant = models.BooleanField(default=False, null=True, blank=True)
    spoken_to_broker = models.BooleanField(default=False, null=True, blank=True)
    
    # Financial Information
    turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    predicted_turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    predicted_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_recurring_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_payable = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_receivable = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    depreciation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    amortisation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Contact Information
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_number = models.CharField(max_length=50, null=True, blank=True)
    
    # Valuation Information (calculated and stored)
    valuation_low = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valuation_high = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sde = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Session tracking
    session_id = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    is_complete = models.BooleanField(default=False)
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        db_table = 'leads'
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.submitted_at.strftime('%Y-%m-%d')})"

