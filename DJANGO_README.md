# ListAcross EU - Django Business Directory

A comprehensive Django-based business directory platform for European businesses with subscription plans, custom website builder, and data import capabilities.

## Features

### 🏢 Business Directory
- **Multi-category business listings** with detailed profiles
- **Geographic organization** by countries and cities
- **Advanced search and filtering** capabilities
- **Review and rating system** for businesses
- **SEO-optimized pages** for better visibility

### 💰 Subscription Plans
- **Free Plan**: Basic listing with limited features
- **Local Plan (€29/month)**: Enhanced local visibility
- **Country Plan (€79/month)**: Country-wide visibility 
- **EU Plan (€199/month)**: Full EU visibility + custom website

### 🌐 Website Builder (EU Plan)
- **Custom subdomain** (yourname.listacrosseu.com)
- **Logo upload and branding** customization
- **Multiple themes** (Modern, Classic, Minimal, Creative, Corporate)
- **Contact forms** and social media integration
- **SEO optimization** tools

### 📊 Data Import System
- **CSV/JSON file imports** for bulk business listings
- **API integrations** (OpenStreetMap, Google Places, Yelp)
- **Field mapping** and validation tools
- **Import job tracking** and error handling

### 💳 Payment Integration
- **Stripe payment processing** for subscriptions
- **Automated billing** and invoice generation
- **Subscription management** and cancellation
- **Usage tracking** and limits enforcement

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL with Redis for caching
- **Payments**: Stripe integration
- **File Storage**: Django-storages with AWS S3
- **Task Queue**: Celery with Redis
- **Authentication**: Django Allauth
- **Frontend**: Bootstrap 5, Crispy Forms

## Project Structure

```
listacrosseu/
├── accounts/          # User management and profiles
├── businesses/        # Business listings and categories  
├── subscriptions/     # Subscription plans and billing
├── websites/          # Website builder for EU plan users
├── payments/          # Stripe payment processing
├── data_import/       # CSV/JSON/API data import system
├── directory/         # Main directory views and API
├── static/           # Static files (CSS, JS, images)
├── templates/        # Django templates
├── media/           # User uploaded files
└── manage.py        # Django management script
```

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r django_requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=listacrosseu
DB_USER=postgres
DB_PASSWORD=your-password

# Stripe keys
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create initial data (subscription plans, categories, countries)
python setup_initial_data.py

# Create superuser (if not using setup script)
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Key Features Implementation

### Subscription Management

Users can subscribe to different plans with varying features:
- **Plan limitations** enforced through models and middleware
- **Automatic billing** via Stripe subscriptions
- **Usage tracking** for listings and API calls
- **Upgrade/downgrade** functionality

### Website Builder (EU Plan Only)

EU plan subscribers get:
- **Custom subdomain** (mycompany.listacrosseu.com)
- **Domain management** with SSL certificates
- **Theme selection** and customization
- **Logo upload** and branding options
- **Contact form** submissions
- **Analytics integration**

### Data Import System

Administrators can import business data from:
- **CSV files** with customizable field mapping
- **JSON APIs** with configurable endpoints
- **OpenStreetMap** Overpass API integration
- **Google Places** API (with API key)
- **Manual uploads** with validation

### Multi-tenant Architecture

The platform supports:
- **Main directory** at listacrosseu.com
- **User websites** at subdomain.listacrosseu.com
- **Middleware routing** for subdomain handling
- **Shared business listings** across all sites

## API Endpoints

### Business Directory API

```
GET /api/businesses/          # List businesses
GET /api/businesses/{id}/     # Business details
GET /api/categories/          # List categories
GET /api/countries/          # List countries
GET /api/search/             # Search businesses
```

### Subscription API

```
GET /api/subscriptions/plans/     # List subscription plans
POST /api/subscriptions/subscribe/ # Create subscription
GET /api/subscriptions/manage/    # Manage subscription
```

### Website Builder API

```
POST /api/websites/create/    # Create user website
GET /api/websites/manage/     # Manage website
PUT /api/websites/edit/      # Edit website content
GET /api/websites/domains/   # Available domains
```

## Data Import Usage

### CSV Import Example

1. Create a `DataSource` with type 'csv'
2. Upload CSV file with business data
3. Configure field mapping:
```json
{
  "name": "business_name",
  "email": "contact_email", 
  "phone": "phone_number",
  "address": "street_address",
  "city": "city_name",
  "country": "country_name",
  "category": "business_type"
}
```
4. Run import job via admin or API

### OpenStreetMap Import

Automatically imports restaurants and businesses from OpenStreetMap:
```bash
python manage.py import_data --source="OpenStreetMap Restaurants"
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in production
2. Configure PostgreSQL database
3. Set up Redis for Celery tasks
4. Configure AWS S3 for file storage
5. Set up SSL certificates
6. Configure Stripe webhook endpoints

### Docker Deployment (Optional)

Create `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python manage.py test`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@listacrosseu.com or create an issue on GitHub.