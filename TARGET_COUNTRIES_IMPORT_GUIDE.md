# Netherlands, Portugal, Belgium Import Guide
# =============================================

## 🚀 Quick Start Import Instructions

### 1. Set up your Google Places API Key

**Option A: Environment Variable (Recommended)**
1. Add to your `.env` file:
```
GOOGLE_PLACES_API_KEY=your_actual_api_key_here
```

**Option B: Command Line**
Use the --api-key parameter when running the command

### 2. Test Import (Recommended First Step)
```bash
# Test with just 10 businesses per country
python manage.py import_target_countries --test-mode

# Test specific country only
python manage.py import_target_countries --test-mode --country netherlands
```

### 3. Full Import Commands

**Import All Three Countries:**
```bash
# Import 500 businesses per country (1,500 total)
python manage.py import_target_countries --businesses-per-country 500

# Import with slower rate limiting (safer for API limits)
python manage.py import_target_countries --businesses-per-country 300 --delay 1.5
```

**Import Specific Country:**
```bash
# Netherlands only
python manage.py import_target_countries --country netherlands --businesses-per-country 400

# Portugal only  
python manage.py import_target_countries --country portugal --businesses-per-country 600

# Belgium only
python manage.py import_target_countries --country belgium --businesses-per-country 300
```

### 4. Monitor Your Import Progress

**Check current data:**
```bash
python manage.py shell -c "
from businesses.models import Business
target_countries = ['Netherlands', 'Portugal', 'Belgium']
for country in target_countries:
    count = Business.objects.filter(city__country__name=country, status='active').count()
    print(f'{country}: {count} businesses')
print(f'Total: {Business.objects.filter(status=\"active\").count()} businesses')
"
```

### 5. Expected Results

**Potential Import Targets:**
- **Netherlands**: 400-800 businesses (Amsterdam, Rotterdam, Utrecht, The Hague)
- **Portugal**: 600-1000 businesses (Lisbon, Porto, Braga, Coimbra)  
- **Belgium**: 300-600 businesses (Brussels, Antwerp, Ghent, Bruges)

**Total Potential**: 1,300-2,400 new businesses

### 6. API Cost Estimation

**Google Places API Pricing** (as of 2024):
- Text Search: $32 per 1,000 requests
- Place Details: $17 per 1,000 requests

**Cost for 1,500 businesses:**
- ~150 search requests = ~$5
- ~1,500 detail requests = ~$25
- **Total estimated cost**: ~$30-40

### 7. Best Practices

1. **Start with test mode** to verify everything works
2. **Use rate limiting** (--delay 1.0 or higher) to avoid hitting limits  
3. **Import one country at a time** if you have API quotas
4. **Monitor for duplicates** - the system prevents them automatically
5. **Check data quality** after import using the verification commands

### 8. Troubleshooting

**If you get API errors:**
- Check your API key is valid
- Ensure Places API (New) is enabled in Google Cloud Console  
- Verify you have sufficient API quota
- Increase --delay parameter

**If you get few results:**
- Check the cities exist in your database
- Try different search categories
- Verify the country names match exactly

### 9. Custom Categories

The import focuses on these categories for each country:

**Netherlands**: bike shops, coffee shops, flower shops, cheese shops + standard business categories
**Portugal**: wine shops, seafood restaurants, pastry shops, tile shops + standard business categories  
**Belgium**: chocolate shops, beer bars, waffle houses, diamond dealers + standard business categories