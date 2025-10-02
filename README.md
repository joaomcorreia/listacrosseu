# 🇪🇺 ListAcrossEU - European Business Directory Platform

A comprehensive Django-based business directory platform for EU countries with multi-tier subscription plans and integrated website builder.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Import](#data-import)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## ✨ Features

### 🏢 Business Directory
- **Multi-country support** for all 27 EU member states
- **Advanced search** and filtering by location, category, and services
- **Business profiles** with contact information, hours, and media
- **Review system** with ratings and moderation
- **Geographic integration** with city and country relationships

### 💰 Subscription Plans
- **Free Plan**: Basic listing with limited features
- **Local Plan**: Enhanced visibility in specific cities
- **Country Plan**: National visibility and premium features
- **EU Plan**: Continental reach with website builder included

### 🌐 Website Builder (EU Plan)
- **Subdomain websites** (business.listacross.eu)
- **Multiple themes**: Modern, Classic, Minimal, Creative, Corporate
- **Custom branding**: Logo, colors, and content management
- **Contact forms** with submission management
- **SEO optimization** with meta tags and analytics
- **Social media integration**

### 📊 Monetization Features
- **Featured listings** and paid placements
- **Premium business cards** with enhanced visibility
- **Trending destinations** section for promoted content
- **Analytics dashboard** for business owners

### 🛠 Admin & Management
- **Comprehensive admin panel** for all entities
- **CSV import system** for bulk data management
- **User management** with role-based permissions
- **Content moderation** for reviews and submissions

## 🚀 Tech Stack

- **Backend**: Django 5.0.7, Python 3.11+
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django Auth with custom user model
- **File Storage**: Django file handling with media support
- **APIs**: Django REST Framework ready
- **Deployment**: Production ready with static file handling

## 🔧 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/listacrosseu.git
   cd listacrosseu
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load initial data**
   ```bash
   # EU countries are automatically loaded
   python manage.py shell -c "from setup_initial_data import setup_countries; setup_countries()"
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to see the application.

## 📱 Usage

### For Business Owners
1. **Register** and choose a subscription plan
2. **Create business listing** with complete information
3. **Upload media** and manage business hours
4. **Respond to reviews** and engage with customers
5. **Upgrade to EU Plan** for website builder access

### For Directory Admins
1. **Access admin panel** at `/admin/`
2. **Manage businesses**, users, and content
3. **Import bulk data** using CSV management commands
4. **Monitor analytics** and user engagement
5. **Moderate reviews** and handle reports

## 📁 Project Structure

```
listacrosseu/
├── accounts/           # User authentication and profiles
├── api/               # API endpoints and serializers
├── businesses/        # Core business directory functionality
├── data_import/       # Data import utilities
├── directory/         # Main directory views and templates
├── payments/          # Payment processing
├── static/           # CSS, JS, images
├── subscriptions/    # Subscription plans and billing
├── templates/        # HTML templates
├── websites/         # Website builder functionality
├── media/           # Uploaded files
├── manage.py        # Django management script
└── requirements.txt # Python dependencies
```

## 📊 Data Import

### CSV Import System
```bash
# Create CSV templates
python manage.py create_csv_templates

# Import data (use --dry-run first to test)
python manage.py import_categories categories.csv --dry-run
python manage.py import_cities cities.csv --dry-run  
python manage.py import_businesses businesses.csv --dry-run

# Actual import
python manage.py import_categories categories.csv
python manage.py import_cities cities.csv
python manage.py import_businesses businesses.csv
```

### CSV Format Examples

**Cities CSV:**
```csv
name,country_code,latitude,longitude,population,is_capital
Paris,FR,48.8566,2.3522,2161000,True
Berlin,DE,52.5200,13.4050,3669491,True
```

**Businesses CSV:**
```csv
owner_email,name,slug,description,email,phone,website,address,city_name,country_code,postal_code,category_slug,plan,status,featured,verified
admin@listacross.eu,Restaurant Le Bernardin,le-bernardin,Fine French dining,contact@lebernardine.com,+33123456789,https://lebernardine.com,123 Rue de la Paix,Paris,FR,75001,restaurants,free,active,true,true
```

## 🔗 API Documentation

### Main Directory Endpoints
- `GET /` - Homepage with EU countries map
- `GET /country/{code}/` - Country page with cities
- `GET /country/{code}/{city}/` - City page with businesses

### Business Endpoints
- `GET /api/businesses/` - List businesses with filters
- `GET /api/businesses/{id}/` - Business details
- `POST /api/businesses/` - Create business (authenticated)

### Website Builder
- `GET /api/websites/display/` - View published websites
- `GET /api/websites/display/{subdomain}/` - View specific website
- `POST /api/websites/contact/` - Submit contact forms

## 🌟 Key Features Walkthrough

### Homepage Features
- **Interactive EU map** with country flags (36px icons)
- **Featured cities carousel** (6+ cards, 280px width)
- **Business categories** with icon-based navigation (8 cards)
- **Trending destinations** for promoted content
- **How it Works** horizontal section
- **Blog posts slider** with auto-scroll
- **Pricing tables** for subscription plans
- **Professional footer** with 5 navigation sections

### Admin Panel Features
- **Business management** with bulk operations
- **User management** with subscription tracking
- **Review moderation** with approval system
- **Website builder** with theme selection
- **CSV import tools** with validation and error reporting

## 🚀 Deployment

### Production Checklist
1. Configure environment variables in `.env`
2. Set up PostgreSQL database
3. Configure static file serving
4. Set up domain and SSL certificate
5. Configure email backend for notifications

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: Project Wiki
- **Email**: admin@listacross.eu

---

**Built with ❤️ for European businesses by the Django community**