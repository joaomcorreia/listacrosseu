# Flag Management - ListAcrossEU

## 🎌 Automatic Flag Detection System

The ListAcrossEU platform automatically detects and displays country flags based on files in the `static/assets/flags/` directory.

## 📁 File Structure

```
static/assets/flags/
├── at.png        # Austria
├── be.png        # Belgium  
├── bg.png        # Bulgaria
├── cy.png        # Cyprus
├── cz.png        # Czech Republic
├── de.png        # Germany
├── dk.png        # Denmark
├── ee.png        # Estonia
├── es.png        # Spain
├── eu.png        # European Union (special)
├── fi.png        # Finland
├── fr.png        # France
├── gr.png        # Greece
├── hr.png        # Croatia
├── hu.png        # Hungary
├── ie.png        # Ireland
├── it.png        # Italy
├── lt.png        # Lithuania
├── lu.png        # Luxembourg
├── lv.png        # Latvia
├── mt.png        # Malta
├── nl.png        # Netherlands
├── pl.png        # Poland
├── pt.png        # Portugal
├── ro.png        # Romania
├── se.png        # Sweden
├── si.png        # Slovenia
└── sk.png        # Slovakia
```

## 🔧 Adding New Flags

1. **File Naming Convention**: Use the ISO 3166-1 alpha-2 country code in lowercase
   - Example: `pt.png` for Portugal, `fr.png` for France

2. **File Format**: PNG files recommended for best quality
   - Recommended size: 36x36 pixels (circular flags work best)
   - File size: Keep under 50KB for optimal loading

3. **Auto-Detection**: New flags are automatically detected when:
   - File is placed in `static/assets/flags/` directory
   - File follows the naming convention (`{country_code}.png`)
   - Corresponding country exists in the database

## 🎨 Flag Requirements

- **Format**: PNG with transparency support
- **Size**: 36x36 pixels optimal (responsive scaling applied)
- **Style**: Circular flags recommended for consistent appearance
- **Quality**: High resolution for crisp display on all devices

## 🔄 How It Works

1. **Detection**: The `get_available_flags()` function scans the flags directory
2. **Matching**: Flags are matched with countries in the database by country code
3. **Display**: The flag slider automatically includes all available flags
4. **Navigation**: Clicking flags navigates to the respective country pages

## 🌍 Supported Countries

Currently supporting all 27 EU member states plus special entries:

- **EU Flag**: `eu.png` - Links to homepage
- **Member States**: All 27 EU countries with individual flag files
- **Extensions**: Additional flags like England, Scotland, Iceland, Norway, Switzerland

## 📊 Current Status

- ✅ **27 EU countries** with official flags
- ✅ **Automatic detection** system active
- ✅ **Infinite slider** with hover pause
- ✅ **Click navigation** to country pages
- ✅ **Responsive design** with smooth animations

## 🚀 Usage in Templates

```django
<!-- Load the flag slider -->
{% load map_tags %}
{% flag_slider %}

<!-- Or with custom settings -->
{% flag_slider show_all=False %}
```

## 💡 Development Tips

1. **Testing New Flags**: Simply drop the flag file in the directory and refresh
2. **Flag Quality**: Use tools like Photoshop or GIMP to create circular, consistent flags
3. **Performance**: Optimize PNG files with tools like TinyPNG before uploading
4. **Fallbacks**: The system has built-in fallbacks if flags are missing

---

**Last Updated**: October 5, 2025  
**Total Flags Available**: 27+ EU countries + special flags