#!/bin/bash
# Portuguese Business Import Script
# Import businesses from major Portuguese cities (20 per city)

# Set API key
export GOOGLE_PLACES_API_KEY="AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48"

echo "🇵🇹 Starting Portuguese Business Import"
echo "📊 Target: Major Portuguese cities with 20 businesses each"
echo "🎯 Avoiding banks, focusing on diverse business types"
echo ""

# Major Portuguese cities (starting with top 20 for initial test)
cities=(
    "Lisboa, Portugal"
    "Porto, Portugal" 
    "Coimbra, Portugal"
    "Braga, Portugal"
    "Faro, Portugal"
    "Aveiro, Portugal"
    "Leiria, Portugal"
    "Setúbal, Portugal"
    "Viseu, Portugal"
    "Évora, Portugal"
    "Portimão, Portugal"
    "Vila Nova de Gaia, Portugal"
    "Cascais, Portugal"
    "Guimarães, Portugal"
    "Lagos, Portugal"
    "Sintra, Portugal"
    "Viana do Castelo, Portugal"
    "Albufeira, Portugal"
    "Matosinhos, Portugal"
    "Tavira, Portugal"
)

# Business queries (avoiding banks)
business_queries=(
    "restaurants"
    "cafes"  
    "pharmacies"
    "supermarkets"
    "hotels"
    "shops"
    "bakeries"
    "hair salons"
    "auto repair"
    "gas stations"
    "clothing stores"
    "bookstores"
    "tourist attractions"
    "medical clinics"
    "real estate agencies"
)

total_imported=0
total_processed=0

# Process each city
for i in "${!cities[@]}"; do
    city="${cities[$i]}"
    city_num=$((i + 1))
    
    echo "[$city_num/${#cities[@]}] 🏙️ Processing: $city"
    
    city_imported=0
    
    # Try different business types for this city
    for query in "${business_queries[@]}"; do
        if [ $city_imported -ge 20 ]; then
            break
        fi
        
        full_query="$query in $city"
        echo "  🔍 Searching: $full_query"
        
        # Run the import command
        python manage.py import_google_places --query "$full_query" --region "pt"
        
        # Small delay between requests
        sleep 1
        
        city_imported=$((city_imported + 5))  # Estimate 5 per query
    done
    
    total_processed=$((total_processed + 1))
    total_imported=$((total_imported + city_imported))
    
    echo "  ✅ City completed. Estimated: $city_imported businesses"
    echo "  📊 Running total: ~$total_imported businesses"
    echo ""
    
    # Progress update every 5 cities
    if [ $((city_num % 5)) -eq 0 ]; then
        echo "🎉 Progress: $city_num/${#cities[@]} cities completed"
        echo "📈 Estimated total: ~$total_imported businesses imported"
        echo "⏳ Taking a short break..."
        sleep 5
        echo ""
    fi
done

echo "🎉 PORTUGUESE IMPORT BATCH COMPLETED!"
echo "📊 Cities processed: ${#cities[@]}"
echo "📈 Estimated businesses imported: ~$total_imported"
echo ""
echo "🚀 Ready to continue with more cities if needed!"