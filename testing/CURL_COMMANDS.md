# cURL Commands for Testing BusinessEvaluationView

## Quick Test Command (Windows CMD)
```cmd
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d @test_payload.json
```

## Quick Test Command (PowerShell)
```powershell
curl.exe -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d "@test_payload.json"
```

## Quick Test Command (Linux/Mac/Git Bash)
```bash
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d @test_payload.json
```

## Using JSON File (Recommended)
Use the `test_payload.json` file included in this directory:

**Windows CMD:**
```cmd
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d @test_payload.json
```

**PowerShell:**
```powershell
curl.exe -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d "@test_payload.json"
```

**Linux/Mac/Git Bash:**
```bash
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d @test_payload.json
```

## Inline JSON (Windows CMD - Single Line)
```cmd
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d "{\"shareholders_working_in_business\": true, \"taking_full_market_salary\": false, \"salary_adjustment\": \"50000.00\", \"property_own_or_rent\": \"Own\", \"property_market_rent_adjustment\": \"24000.00\", \"company_sector\": \"Technology\", \"adjust_industry_multipliers\": true, \"lower_multiplier\": \"3.5\", \"upper_multiplier\": \"5.0\", \"purpose\": \"Business Sale\", \"spoken_to_accountant\": true, \"spoken_to_broker\": false, \"turnover\": \"500000.00\", \"predicted_turnover\": \"550000.00\", \"profit\": \"150000.00\", \"predicted_profit\": \"175000.00\", \"interest_payable\": \"5000.00\", \"interest_receivable\": \"2000.00\", \"non_recurring_expenses\": \"10000.00\", \"depreciation\": \"15000.00\", \"amortisation\": \"8000.00\", \"net_assets\": \"200000.00\", \"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"phone\": \"+44 20 1234 5678\", \"company_name\": \"Tech Solutions Ltd\", \"company_number\": \"12345678\"}"
```

## Pretty Print Response (Windows)
```cmd
curl -X POST http://localhost:8000/api/business-evaluation/ -H "Content-Type: application/json" -d @test_payload.json | python -m json.tool
```

## Expected Response (Success - 201 Created)
```json
{
  "id": 1,
  "message": "Business valuation request submitted successfully",
  "submitted_at": "2025-01-15T10:30:00.123456Z"
}
```

## Expected Response (Validation Error - 400 Bad Request)
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["Enter a valid email address."],
    ...
  }
}
```

## Notes
- Make sure your Django development server is running: `python manage.py runserver`
- Default port is 8000, adjust the URL if using a different port
- All decimal fields should be sent as strings (e.g., "50000.00")
- Boolean fields accept `true`/`false` (lowercase)
- `property_own_or_rent` must be either "Own" or "Rent"
- `lower_multiplier` and `upper_multiplier` must be positive numbers > 0

