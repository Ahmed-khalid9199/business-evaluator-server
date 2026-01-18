from decimal import Decimal

from api.models import Lead


ROUNDING_INCREMENT = Decimal('1000')  # Round to nearest thousand


def calculate_valuation(data: Lead):
    """
    Calculate business valuation estimate based on financial data.

    Formula based on Chelsea Corporate Business Valuation Tool:
    - SDE = Profit + Non-recurring Expenses + Depreciation + Amortisation + Interest Receivable - Interest Payable
    - Adjusted for salary adjustments and property rent adjustments
    - Valuation = (SDE × Multiplier) + Net Assets

    returns:
    {
        "low": valuation_low,
        "high": valuation_high,
        "sde": sde,
    }

    """
    # Ensure all required fields have values (use 0 as default for None)
    profit = data.profit or Decimal('0')
    depreciation = data.depreciation or Decimal('0')
    amortisation = data.amortisation or Decimal('0')
    non_recurring_expenses = data.non_recurring_expenses or Decimal('0')
    interest_receivable = data.interest_receivable or Decimal('0')
    interest_payable = data.interest_payable or Decimal('0')
    
    # Calculate SDE
    sde = (
        profit  # EBITDA base
        + depreciation  # Add back depreciation
        + amortisation  # Add back amortisation
        + non_recurring_expenses  # Add back one-time expenses
        + interest_receivable  # Add interest receivable
        - interest_payable  # Subtract back interest payable
    )
    
    # Add back salary adjustments (for both buyers and sellers)
    if data.salary_adjustment:
        sde += data.salary_adjustment

    # Add back property rent adjustment if property is owned
    if data.property_own_or_rent == "own" and data.property_market_rent_adjustment:
        sde += data.property_market_rent_adjustment

    # Calculate valuation range
    # Valuation = (SDE × Multiplier) + Net Assets
    lower_multiplier = data.lower_multiplier or Decimal('0')
    upper_multiplier = data.upper_multiplier or Decimal('0')
    net_assets = data.net_assets or Decimal('0')
    
    valuation_low = sde * lower_multiplier
    valuation_high = sde * upper_multiplier

    valuation_low = valuation_low + net_assets
    valuation_high = valuation_high + net_assets

    # Round to nearest thousand for cleaner presentation
    valuation_low = (valuation_low / ROUNDING_INCREMENT).quantize(
        Decimal("1")
    ) * ROUNDING_INCREMENT
    valuation_high = (valuation_high / ROUNDING_INCREMENT).quantize(
        Decimal("1")
    ) * ROUNDING_INCREMENT

    return {
        "low": valuation_low,
        "high": valuation_high,
        "sde": sde,
    }
