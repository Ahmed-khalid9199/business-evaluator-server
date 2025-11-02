from django.db import models


class Lead(models.Model):
    """
    Lead model to store business valuation form submissions.
    """
    # Sector Information
    company_sector = models.CharField(max_length=100)
    shareholders_working_in_business = models.BooleanField(default=False)
    taking_full_market_salary = models.BooleanField(default=False)
    salary_adjustment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    property_own_or_rent = models.CharField(
        max_length=10, 
        choices=[('Own', 'Own'), ('Rent', 'Rent')]
    )
    property_market_rent_adjustment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    adjust_industry_multipliers = models.BooleanField(default=False)
    lower_multiplier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upper_multiplier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purpose = models.CharField(max_length=100)
    spoken_to_accountant = models.BooleanField(default=False)
    spoken_to_broker = models.BooleanField(default=False)
    
    # Financial Information
    turnover = models.DecimalField(max_digits=15, decimal_places=2)
    predicted_turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=15, decimal_places=2)
    predicted_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_recurring_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    interest_payable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_receivable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    depreciation = models.DecimalField(max_digits=15, decimal_places=2)
    amortisation = models.DecimalField(max_digits=15, decimal_places=2)
    net_assets = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Contact Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200, blank=True)
    company_number = models.CharField(max_length=50, blank=True)
    
    # Valuation Information (calculated and stored)
    valuation_low = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valuation_high = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sde = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        db_table = 'leads'
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.submitted_at.strftime('%Y-%m-%d')})"

