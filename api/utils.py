from decimal import Decimal

from api.models import Lead


ROUNDING_INCREMENT = Decimal('1000')  # Round to nearest thousand


def calculate_valuation(data: Lead):
    """
    Calculate business valuation estimate based on financial data.

    Formula based on Chelsea Corporate Business Valuation Tool:
    - SDE = Profit + Non-recurring Expenses + Depreciation + Amortisation + Interest Payable - Interest Receivable
    - Adjusted for salary adjustments and property rent adjustments
    - Valuation = (SDE × Multiplier) + Net Assets

    returns:
    {
        "low": valuation_low,
        "high": valuation_high,
        "sde": sde,
    }

    """
    # Calculate SDE
    sde = (
        data.profit  # EBITDA base
        + data.depreciation  # Add back depreciation
        + data.amortisation  # Add back amortisation
        + data.non_recurring_expenses  # Add back one-time expenses
        + data.interest_payable  # Add back interest payable
        - data.interest_receivable  # Subtract interest receivable
    )

    # Apply salary adjustment if not taking full market salary
    if not data.taking_full_market_salary:
        sde += data.salary_adjustment

    # Apply property rent adjustment if property is rented
    if data.property_own_or_rent == "Rent":
        sde += data.property_market_rent_adjustment

    # Calculate valuation range
    # Valuation = (SDE × Multiplier) + Net Assets
    valuation_low = sde * data.lower_multiplier
    valuation_high = sde * data.upper_multiplier

    valuation_low = valuation_low + data.net_assets
    valuation_high = valuation_high + data.net_assets

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
