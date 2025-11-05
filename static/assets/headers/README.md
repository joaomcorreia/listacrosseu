# Header Images Guide

This folder contains header background images for country-specific pages.

## Naming Convention

All header images should follow this exact naming pattern:
```
{country_slug}_header-1920x600.jpg
```

## Examples

- `austria_header-1920x600.jpg` - For Austria pages
- `belgium_header-1920x600.jpg` - For Belgium pages
- `france_header-1920x600.jpg` - For France pages
- `germany_header-1920x600.jpg` - For Germany pages
- `portugal_header-1920x600.jpg` - For Portugal pages
- `spain_header-1920x600.jpg` - For Spain pages
- etc.

## Image Specifications

- **Dimensions**: 1920x600 pixels (16:5 aspect ratio)
- **Format**: JPG (for better performance)
- **Quality**: High quality, optimized for web
- **Content**: Should represent the country's landmarks, culture, or scenery

## Usage

These images are automatically used as backgrounds for:

1. **Country pages** (`/country-name/`) - Direct country background
2. **Category-Country pages** (`/category/country/`) - Country background with category overlay
3. **City pages** (`/country/city/`) - Country background with city overlay  
4. **Business pages** (`/country/city/category/business/`) - Country background with business overlay

## Fallback

If a country image doesn't exist, the system will fall back to the CSS gradient backgrounds:
- Country pages: Red gradient (#dc3545 → #fd7e14)
- Category pages: Green gradient (#28a745 → #20c997)
- City pages: Purple gradient (#6f42c1 → #e83e8c)
- Business pages: Cyan gradient (#17a2b8 → #6610f2)

## Country Slugs Reference

Make sure to use the exact country slugs from the database:

- Austria: `austria`
- Belgium: `belgium`
- Bulgaria: `bulgaria`
- Croatia: `croatia`
- Cyprus: `cyprus`
- Czech Republic: `czech-republic`
- Denmark: `denmark`
- Estonia: `estonia`
- Finland: `finland`
- France: `france`
- Germany: `germany`
- Greece: `greece`
- Hungary: `hungary`
- Ireland: `ireland`
- Italy: `italy`
- Latvia: `latvia`
- Lithuania: `lithuania`
- Luxembourg: `luxembourg`
- Malta: `malta`
- Netherlands: `netherlands`
- Poland: `poland`
- Portugal: `portugal`
- Romania: `romania`
- Slovakia: `slovakia`
- Slovenia: `slovenia`
- Spain: `spain`
- Sweden: `sweden`

## Adding Images

1. Prepare your image at 1920x600 pixels
2. Name it using the convention: `{country_slug}_header-1920x600.jpg`
3. Place it in this folder: `/static/assets/headers/`
4. The image will automatically appear on all relevant pages for that country

## Tips

- Choose images that represent the country well (landmarks, landscapes, architecture)
- Ensure good contrast so white text remains readable
- Test on both desktop and mobile devices
- Consider the emotional impact - tourism and business-friendly imagery works best