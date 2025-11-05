"""
Portuguese Business Import Strategy
Import 3,180+ businesses across Portugal (20 per city)
Focusing on diverse business types, minimizing banks
"""

import subprocess
import time
import os
from typing import List, Dict

# Major Portuguese cities for systematic import
PORTUGUESE_CITIES = [
    # Major cities (Lisbon area)
    "Lisboa, Portugal", "Cascais, Portugal", "Sintra, Portugal", "Oeiras, Portugal",
    "Almada, Portugal", "Amadora, Portugal", "Odivelas, Portugal", "Loures, Portugal",
    
    # Porto area
    "Porto, Portugal", "Vila Nova de Gaia, Portugal", "Matosinhos, Portugal", 
    "Gondomar, Portugal", "Valongo, Portugal", "Maia, Portugal", "Póvoa de Varzim, Portugal",
    
    # Central Portugal
    "Coimbra, Portugal", "Aveiro, Portugal", "Leiria, Portugal", "Viseu, Portugal",
    "Guarda, Portugal", "Castelo Branco, Portugal", "Santarém, Portugal", 
    "Caldas da Rainha, Portugal", "Óbidos, Portugal", "Nazaré, Portugal",
    
    # North Portugal
    "Braga, Portugal", "Viana do Castelo, Portugal", "Guimarães, Portugal",
    "Vila Real, Portugal", "Chaves, Portugal", "Bragança, Portugal", "Lamego, Portugal",
    
    # Central coast
    "Figueira da Foz, Portugal", "Pombal, Portugal", "Marinha Grande, Portugal",
    "Alcobaça, Portugal", "Batalha, Portugal", "Tomar, Portugal", "Torres Vedras, Portugal",
    
    # Alentejo region
    "Évora, Portugal", "Beja, Portugal", "Portalegre, Portugal", "Estremoz, Portugal",
    "Elvas, Portugal", "Monsaraz, Portugal", "Mértola, Portugal", "Serpa, Portugal",
    
    # Algarve region
    "Faro, Portugal", "Portimão, Portugal", "Lagos, Portugal", "Albufeira, Portugal",
    "Tavira, Portugal", "Vila Real de Santo António, Portugal", "Olhão, Portugal",
    "Silves, Portugal", "Sagres, Portugal", "Monchique, Portugal",
    
    # Additional cities for complete coverage
    "Setúbal, Portugal", "Palmela, Portugal", "Sesimbra, Portugal", "Barreiro, Portugal",
    "Montijo, Portugal", "Alcochete, Portugal", "Moita, Portugal", "Seixal, Portugal",
    
    # Interior cities
    "Covilhã, Portugal", "Fundão, Portugal", "Sertã, Portugal", "Abrantes, Portugal",
    "Entroncamento, Portugal", "Golegã, Portugal", "Chamusca, Portugal", "Alpiarça, Portugal",
    
    # More northern cities
    "Amarante, Portugal", "Penafiel, Portugal", "Marco de Canaveses, Portugal",
    "Felgueiras, Portugal", "Lousada, Portugal", "Paços de Ferreira, Portugal",
    
    # Western cities
    "Caldas da Rainha, Portugal", "Peniche, Portugal", "Torres Vedras, Portugal",
    "Mafra, Portugal", "Ericeira, Portugal", "Vila Franca de Xira, Portugal",
    
    # Eastern cities
    "Monsanto, Portugal", "Idanha-a-Nova, Portugal", "Penamacor, Portugal",
    "Vila Velha de Ródão, Portugal", "Nisa, Portugal", "Crato, Portugal",
    
    # Southern interior
    "Castro Verde, Portugal", "Almodôvar, Portugal", "Ourique, Portugal",
    "Santiago do Cacém, Portugal", "Grândola, Portugal", "Sines, Portugal",
    
    # Islands (if Google Places supports)
    "Funchal, Portugal", "Machico, Portugal", "Santa Cruz, Portugal",  # Madeira
    "Angra do Heroísmo, Portugal", "Horta, Portugal", "Ponta Delgada, Portugal",  # Azores
    
    # Additional mainland cities
    "Mirandela, Portugal", "Macedo de Cavaleiros, Portugal", "Mogadouro, Portugal",
    "Torre de Moncorvo, Portugal", "Freixo de Espada à Cinta, Portugal",
    
    # More coastal cities
    "Espinho, Portugal", "Ovar, Portugal", "Ílhavo, Portugal", "Vagos, Portugal",
    "Mira, Portugal", "Cantanhede, Portugal", "Mealhada, Portugal", "Águeda, Portugal",
    
    # Additional central cities
    "Oliveira do Hospital, Portugal", "Arganil, Portugal", "Góis, Portugal",
    "Pampilhosa da Serra, Portugal", "Pedrógão Grande, Portugal", "Figueiró dos Vinhos, Portugal",
    
    # More Alentejo cities
    "Redondo, Portugal", "Vendas Novas, Portugal", "Montemor-o-Novo, Portugal",
    "Arraiolos, Portugal", "Mora, Portugal", "Ponte de Sor, Portugal",
    
    # More Algarve cities
    "Castro Marim, Portugal", "Alcoutim, Portugal", "Aljezur, Portugal",
    "Vila do Bispo, Portugal", "São Brás de Alportel, Portugal", "Loulé, Portugal",
    
    # Final cities to reach 159
    "Arouca, Portugal", "Vale de Cambra, Portugal", "Oliveira de Azeméis, Portugal",
    "São João da Madeira, Portugal", "Santa Maria da Feira, Portugal", "Espinho, Portugal",
    "Vila do Conde, Portugal", "Trofa, Portugal", "Santo Tirso, Portugal", "Famalicão, Portugal",
    "Vila Verde, Portugal", "Barcelos, Portugal", "Esposende, Portugal", "Caminha, Portugal",
    "Valença, Portugal", "Monção, Portugal", "Melgaço, Portugal", "Arcos de Valdevez, Portugal",
    "Ponte da Barca, Portugal", "Ponte de Lima, Portugal", "Viana do Castelo, Portugal"
]

# Business types to focus on (avoiding banks)
BUSINESS_TYPES = [
    "restaurants", "cafes", "shops", "pharmacies", "bakeries", 
    "hotels", "supermarkets", "clothing stores", "hair salons",
    "auto repair", "gas stations", "bookstores", "electronics stores",
    "jewelry stores", "shoe stores", "tourist attractions", 
    "medical clinics", "veterinary clinics", "gyms", "spas",
    "real estate agencies", "insurance agencies", "travel agencies",
    "car dealers", "furniture stores", "home improvement stores"
]

def run_import_command(query: str, region: str = "pt") -> Dict:
    """Run a Google Places import command and return results"""
    try:
        print(f"🔍 Importing: {query}")
        
        # Set environment variable for this session
        env = os.environ.copy()
        env['GOOGLE_PLACES_API_KEY'] = 'AIzaSyBmKk3uM1BZV_qTuodk9fQmYWLzp1J-k48'
        
        # Run the import command
        result = subprocess.run([
            'python', 'manage.py', 'import_google_places',
            '--query', query,
            '--region', region
        ], capture_output=True, text=True, env=env, cwd='C:\\projects\\listacrosseu')
        
        # Parse results from output
        output = result.stdout
        
        # Extract statistics
        imported = 0
        skipped = 0
        errors = 0
        
        if "Import Statistics:" in output:
            lines = output.split('\n')
            for line in lines:
                if "Imported:" in line:
                    imported = int(line.split('Imported: ')[1].split(' ')[0])
                elif "Skipped:" in line:
                    skipped = int(line.split('Skipped: ')[1].split(' ')[0])
                elif "Errors:" in line:
                    errors = int(line.split('Errors: ')[1].split(' ')[0])
        
        return {
            'query': query,
            'imported': imported,
            'skipped': skipped,
            'errors': errors,
            'success': result.returncode == 0
        }
        
    except Exception as e:
        print(f"❌ Error with query '{query}': {e}")
        return {
            'query': query,
            'imported': 0,
            'skipped': 0,
            'errors': 1,
            'success': False
        }

def import_businesses_for_city(city: str, max_imports: int = 20) -> List[Dict]:
    """Import businesses for a specific city"""
    results = []
    imported_count = 0
    
    print(f"\n🏙️ Processing city: {city}")
    print(f"Target: {max_imports} businesses")
    
    # Try different business types until we reach the target
    for business_type in BUSINESS_TYPES:
        if imported_count >= max_imports:
            break
            
        # Create query for this business type in this city
        query = f"{business_type} in {city}"
        
        # Run import
        result = run_import_command(query)
        results.append(result)
        
        imported_count += result['imported']
        
        print(f"  📊 {business_type}: +{result['imported']} businesses (Total: {imported_count})")
        
        # Small delay to respect API limits
        time.sleep(0.5)
        
        # Stop if we've reached our target
        if imported_count >= max_imports:
            print(f"  ✅ Target reached: {imported_count} businesses imported")
            break
    
    return results

def main():
    """Main import function"""
    print("🇵🇹 Starting Portuguese Business Import")
    print(f"📊 Target: ~3,180 businesses across {len(PORTUGUESE_CITIES)} cities")
    print(f"🎯 ~20 businesses per city")
    print("\n" + "="*60)
    
    all_results = []
    total_imported = 0
    total_skipped = 0
    total_errors = 0
    
    # Process each city
    for i, city in enumerate(PORTUGUESE_CITIES, 1):
        print(f"\n[{i}/{len(PORTUGUESE_CITIES)}] {city}")
        
        city_results = import_businesses_for_city(city, max_imports=20)
        all_results.extend(city_results)
        
        # Update totals
        city_imported = sum(r['imported'] for r in city_results)
        city_skipped = sum(r['skipped'] for r in city_results)
        city_errors = sum(r['errors'] for r in city_results)
        
        total_imported += city_imported
        total_skipped += city_skipped
        total_errors += city_errors
        
        print(f"City Summary: {city_imported} imported, {city_skipped} skipped, {city_errors} errors")
        print(f"Running Total: {total_imported} businesses imported")
        
        # Progress update every 10 cities
        if i % 10 == 0:
            print(f"\n🎉 Progress Update: {i}/{len(PORTUGUESE_CITIES)} cities completed")
            print(f"📈 Total imported so far: {total_imported} businesses")
            
        # Longer delay between cities to respect rate limits
        time.sleep(2)
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 PORTUGUESE IMPORT COMPLETED!")
    print(f"📊 Final Statistics:")
    print(f"  🏙️ Cities processed: {len(PORTUGUESE_CITIES)}")
    print(f"  ✅ Businesses imported: {total_imported}")
    print(f"  ⏭️ Businesses skipped: {total_skipped}")
    print(f"  ❌ Errors: {total_errors}")
    print(f"  🎯 Target achieved: {(total_imported/3180)*100:.1f}%")
    
    return {
        'cities_processed': len(PORTUGUESE_CITIES),
        'total_imported': total_imported,
        'total_skipped': total_skipped,
        'total_errors': total_errors,
        'results': all_results
    }

if __name__ == "__main__":
    main()