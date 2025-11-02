"""
Valuation configuration file.
Adjust these values based on the specific formula from the requirements document.
"""

from decimal import Decimal

# Base EBITDA Multipliers
BASE_MULTIPLIER_LOW = Decimal('3.0')   # Conservative estimate
BASE_MULTIPLIER_HIGH = Decimal('5.0')  # Optimistic estimate

# Multiplier Adjustments
PROPERTY_OWNED_ADJUSTMENT = Decimal('0.2')      # Adjustment when property is owned
SHAREHOLDERS_WORKING_ADJUSTMENT = Decimal('0.1')  # Adjustment when shareholders work in business

# Multiplier Bounds (to prevent unrealistic values)
MIN_MULTIPLIER = Decimal('2.5')
MAX_MULTIPLIER_LOW = Decimal('6.0')
MAX_MULTIPLIER_HIGH = Decimal('7.0')

# Minimum Valuation
MIN_VALUATION = Decimal('50000')  # Minimum business valuation threshold

# Rounding
ROUNDING_INCREMENT = Decimal('1000')  # Round to nearest thousand

# Sector-specific multipliers (optional)
# Uncomment and adjust based on your sector classification:
# SECTOR_MULTIPLIERS = {
#     '1': {'low': Decimal('3.5'), 'high': Decimal('5.5')},  # Example sector
#     '2': {'low': Decimal('2.8'), 'high': Decimal('4.8')},  # Another sector
#     # Add more sectors as needed
# }

