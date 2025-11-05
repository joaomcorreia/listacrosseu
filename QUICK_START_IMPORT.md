# 🚀 Quick Start: Import Netherlands, Portugal, Belgium Businesses

## Step 1: Get Your Google Places API Key

### A. Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable the **Places API (New)** - this is important!

### B. Create API Key
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy your API key (looks like: `AIzaSyBvOkBo...`)

### C. Add to Your .env File
Replace `your_google_places_api_key_here` in your `.env` file with your actual API key:
```
GOOGLE_PLACES_API_KEY=AIzaSyBvOkBo_your_actual_key_here
```

## Step 2: Test the Import System

### Test Import (Start Here!)
```cmd
# Test with just 3 businesses per country (9 total)
python manage.py import_target_countries --test-mode
```

### If Test Works, Try Small Import
```cmd
# Import 50 businesses per country (150 total)
python manage.py import_target_countries --businesses-per-country 50
```

## Step 3: Check Your Results

After import, check what you got:
```cmd
python manage.py shell -c "from businesses.models import Business; target_countries = ['Netherlands', 'Portugal', 'Belgium']; [print(f'{country}: {Business.objects.filter(city__country__name=country, status=\"active\").count()} businesses') for country in target_countries]; print(f'Total: {Business.objects.filter(status=\"active\").count()} businesses')"
```

## Step 4: Full Import (If Everything Works)

### Import All Three Countries
```cmd
# Import 400 businesses per country (1,200 total)
python manage.py import_target_countries --businesses-per-country 400

# Or import specific country only
python manage.py import_target_countries --country netherlands --businesses-per-country 500
```

## Expected Results

You should see businesses like:
- **Netherlands**: Bike shops in Amsterdam, Coffee shops in Rotterdam
- **Portugal**: Wine shops in Porto, Seafood restaurants in Lisbon  
- **Belgium**: Chocolate shops in Brussels, Beer bars in Antwerp

## Troubleshooting

**❌ "No API key found"**
- Check your `.env` file has `GOOGLE_PLACES_API_KEY=your_key`
- Restart your Django server after adding the key

**❌ "API key not valid" or "403 Forbidden"**
- Make sure Places API (New) is enabled in Google Cloud Console
- Check your API key is correct and has no extra spaces

**❌ "No results found"**
- Some cities might have few businesses in certain categories
- Try running again - the system randomly searches different areas
- Check the cities exist in your database first

**❌ Rate limit errors**
- Add `--delay 2.0` to slow down requests
- Reduce `--businesses-per-country` number

## Cost Estimate

For 1,200 businesses (~$30-40 in API costs):
- ~120 search requests = ~$4
- ~1,200 detail requests = ~$20
- **Total**: ~$24-30

Start with test mode (free - only ~$0.50) to make sure everything works!

## Next Steps After Import

1. Check your Next.js frontend shows the new countries
2. Verify businesses appear on the map
3. Test search and filtering with new data
4. Consider adding more countries if successful