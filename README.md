# Business Valuation Evaluator Server

Django REST Framework backend application for handling business valuation form submissions.

## Features

- RESTful API endpoint for business evaluation form submissions
- Data transformation (string to boolean, string to decimal)
- Comprehensive validation
- **Automatic email notifications** with business valuation estimates
- Admin interface for lead management
- CORS enabled for frontend integration
- PostgreSQL or SQLite database support

## Setup Instructions

### 1. Install Dependencies

Create a virtual environment (recommended):

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

### 2. Database Configuration

The project is configured to use SQLite by default (development). To use PostgreSQL:

1. Update `evaluator_server/settings.py`:
   - Uncomment the PostgreSQL database configuration
   - Comment out the SQLite configuration
   - Update database credentials

2. Create PostgreSQL database:
```bash
createdb evaluator_db
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/business-evaluation/`

Admin panel: `http://localhost:8000/admin/`

## API Documentation

### Endpoints

**POST** `/api/business-evaluation/`

### Viewing and Testing the API

Django REST Framework provides a browseable API interface that allows you to view and test the API directly in your web browser.

#### Accessing the Browseable API

1. **Start the development server** (if not already running):
   ```bash
   python manage.py runserver
   ```

2. **Navigate to the API endpoint** in your browser:
   ```
   http://localhost:8000/api/business-evaluation/
   ```

The browseable API is only available when `DEBUG=True` (development mode) and provides an interactive way to explore and test all API endpoints without needing external tools like Postman or cURL.

## Production Considerations

Before deploying to production:

1. **Security**:
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Configure proper `ALLOWED_HOSTS`
   - Restrict `CORS_ALLOWED_ORIGINS`
   - Consider adding API authentication

2. **Database**:
   - Use PostgreSQL for production
   - Set up proper database backups
   - Configure connection pooling

3. **Static Files**:
   - Configure static file serving
   - Use a CDN or reverse proxy

4. **Logging**:
   - Configure proper logging settings
   - Set up log rotation

5. **Monitoring**:
   - Add error tracking (e.g., Sentry)
   - Set up health check endpoints

## Email Notifications

When a new lead is submitted, an automatic email is sent to the user with:

- Personalized greeting
- Business valuation estimate (calculated from financial data)
- Information about next steps
- Contact information and call-to-action buttons

### Email Configuration

By default, emails are sent to the console (for development). To configure SMTP in production:

1. Set environment variables in `.env` file:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_TIMEOUT=10
   
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   CONTACT_EMAIL=info@chelseacorporate.com
   CONTACT_PHONE=(0) 20 3011 1373
   SITE_URL=https://chelseacorporate.com
   BACKEND_URL=https://your-backend-url.com
   ```

2. Customize contact information in settings:
   ```python
   CONTACT_EMAIL = 'info@chelseacorporate.com'
   CONTACT_PHONE = '0117 435 4350'
   SITE_URL = 'https://chelseacorporate.com'
   ```

### Valuation Calculation

The email includes a valuation estimate calculated using the following formula:

**Step 1: Calculate SDE (Seller's Discretionary Earnings)**
```
SDE = Profit + Non-recurring Expenses + Depreciation + Amortisation + Interest Payable - Interest Receivable
```

**Step 2: Apply Adjustments**
- **Salary Adjustment**: Added to SDE if shareholders are not taking full market salary
- **Property Rent Adjustment**: Added to SDE if the property is rented (instead of owned)

**Step 3: Calculate Valuation Range**
```
Valuation Low  = (Adjusted SDE × Lower Multiplier) + Net Assets
Valuation High = (Adjusted SDE × Upper Multiplier) + Net Assets
```

**Multipliers:**
- The lower and upper multipliers are provided in the API request
- Default range is typically 3x-5x, but can be customized per business
- Final valuations are rounded to the nearest £1,000 for presentation

**Components:**
- **SDE** represents the true discretionary earnings available to the business owner
- **Multipliers** reflect industry standards and business characteristics
- **Net Assets** include the business's tangible assets (cash, property, equipment, etc.)


## Optional Enhancements

- CSV export functionality for leads
- Lead status tracking (new, contacted, converted)
- API authentication (token-based)
- Rate limiting
- API versioning
- Custom valuation calculation logic per industry sector

