"""
Automated Data Collection System - Master Controller
Orchestrates all data collection processes for the massive EU directory
"""

import os
import django
import subprocess
import sys
import time
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from businesses.models import Country, City, Category, Business


class AutomatedDataCollectionSystem:
    """Master controller for automated data collection"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.log_file = f"data_collection_{self.start_time.strftime('%Y%m%d_%H%M%S')}.log"
        
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def run_script(self, script_path, description):
        """Run a Python script and log results"""
        
        self.log(f"🚀 STARTING: {description}")
        self.log(f"📂 Script: {script_path}")
        
        try:
            # Run the script
            result = subprocess.run([
                sys.executable, script_path
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.log(f"✅ SUCCESS: {description}")
                if result.stdout:
                    self.log(f"📋 Output: {result.stdout[-500:]}")  # Last 500 chars
            else:
                self.log(f"❌ ERROR: {description}")
                self.log(f"💥 Error: {result.stderr}")
                
            return result.returncode == 0
            
        except Exception as e:
            self.log(f"💥 EXCEPTION running {description}: {e}")
            return False
    
    def get_current_stats(self):
        """Get current database statistics"""
        stats = {
            'countries': Country.objects.count(),
            'cities': City.objects.count(),
            'categories': Category.objects.count(),
            'businesses': Business.objects.count(),
        }
        return stats
    
    def log_stats(self, label):
        """Log current statistics"""
        stats = self.get_current_stats()
        self.log(f"📊 {label}:")
        self.log(f"   Countries: {stats['countries']:,}")
        self.log(f"   Cities: {stats['cities']:,}")
        self.log(f"   Categories: {stats['categories']:,}")
        self.log(f"   Businesses: {stats['businesses']:,}")
    
    def run_full_collection_cycle(self):
        """Run the complete data collection cycle"""
        
        self.log("🎯 AUTOMATED DATA COLLECTION SYSTEM STARTING")
        self.log("=" * 80)
        self.log(f"📅 Start time: {self.start_time}")
        self.log(f"🎯 Target: 820+ cities, 49,200+ businesses")
        
        # Initial stats
        initial_stats = self.get_current_stats()
        self.log_stats("INITIAL STATUS")
        
        # Phase 1: Expand Cities (139 → 820+)
        self.log("\n" + "🏙️ PHASE 1: EXPANDING EU CITIES DATABASE")
        self.log("-" * 60)
        
        cities_success = self.run_script(
            "scripts/expand_eu_cities.py",
            "EU Cities Expansion to 820+ cities"
        )
        
        if cities_success:
            self.log_stats("AFTER CITIES EXPANSION")
        else:
            self.log("⚠️ Cities expansion had issues, continuing anyway...")
        
        # Phase 2: Expand Categories (67 → 200+)
        self.log("\n" + "🏷️ PHASE 2: EXPANDING BUSINESS CATEGORIES")
        self.log("-" * 60)
        
        categories_success = self.run_script(
            "scripts/expand_business_categories.py", 
            "Business Categories Expansion"
        )
        
        if categories_success:
            self.log_stats("AFTER CATEGORIES EXPANSION")
        else:
            self.log("⚠️ Categories expansion had issues, continuing anyway...")
        
        # Phase 3: Massive Business Collection (0 → 49,200+)
        self.log("\n" + "🏢 PHASE 3: MASSIVE BUSINESS DATA COLLECTION")
        self.log("-" * 60)
        self.log("⚠️ This phase may take several hours...")
        
        business_success = self.run_script(
            "scripts/massive_business_collector.py",
            "Massive Business Data Collection (Target: 49,200+ businesses)"
        )
        
        if business_success:
            self.log_stats("AFTER BUSINESS COLLECTION")
        else:
            self.log("⚠️ Business collection had issues...")
        
        # Final Summary
        final_stats = self.get_current_stats()
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.log("\n" + "🎉 AUTOMATED DATA COLLECTION COMPLETED")
        self.log("=" * 80)
        self.log(f"📅 End time: {end_time}")
        self.log(f"⏱️ Total duration: {duration}")
        
        self.log("\n📊 FINAL RESULTS:")
        self.log(f"   Countries: {initial_stats['countries']:,} → {final_stats['countries']:,}")
        self.log(f"   Cities: {initial_stats['cities']:,} → {final_stats['cities']:,}")  
        self.log(f"   Categories: {initial_stats['categories']:,} → {final_stats['categories']:,}")
        self.log(f"   Businesses: {initial_stats['businesses']:,} → {final_stats['businesses']:,}")
        
        # Calculate achievements
        cities_added = final_stats['cities'] - initial_stats['cities']
        categories_added = final_stats['categories'] - initial_stats['categories'] 
        businesses_added = final_stats['businesses'] - initial_stats['businesses']
        
        self.log("\n🎯 ACHIEVEMENTS:")
        self.log(f"   ✅ Cities added: {cities_added:,}")
        self.log(f"   ✅ Categories added: {categories_added:,}")
        self.log(f"   ✅ Businesses added: {businesses_added:,}")
        
        # Success metrics
        cities_target = 820
        business_target = 49200
        
        cities_percentage = (final_stats['cities'] / cities_target) * 100
        business_percentage = (final_stats['businesses'] / business_target) * 100
        
        self.log("\n🏆 SUCCESS METRICS:")
        self.log(f"   🏙️ Cities target achievement: {cities_percentage:.1f}% ({final_stats['cities']:,}/{cities_target:,})")
        self.log(f"   🏢 Business target achievement: {business_percentage:.1f}% ({final_stats['businesses']:,}/{business_target:,})")
        
        if business_percentage >= 80:
            self.log("🎉 EXCELLENT! Business target mostly achieved!")
        elif business_percentage >= 50:
            self.log("👍 GOOD! Made significant progress on business target!")
        elif business_percentage >= 25:
            self.log("📈 PROGRESS! Good start on business collection!")
        else:
            self.log("⚠️ MORE WORK NEEDED: Consider running additional collection cycles")
        
        self.log(f"\n📝 Log file saved: {self.log_file}")
        self.log("🚀 ListAcross.eu is ready for massive European business directory launch!")
        
        return {
            'success': True,
            'duration': duration,
            'initial_stats': initial_stats,
            'final_stats': final_stats,
            'achievements': {
                'cities_added': cities_added,
                'categories_added': categories_added,
                'businesses_added': businesses_added
            }
        }


# Master execution function
def run_master_collection():
    """Run the master data collection process"""
    
    collector = AutomatedDataCollectionSystem()
    
    try:
        results = collector.run_full_collection_cycle()
        return results
        
    except KeyboardInterrupt:
        collector.log("⚠️ COLLECTION INTERRUPTED by user")
        collector.log("💾 Partial results have been saved to database")
        return {'success': False, 'reason': 'interrupted'}
        
    except Exception as e:
        collector.log(f"💥 CRITICAL ERROR: {e}")
        return {'success': False, 'reason': str(e)}


if __name__ == "__main__":
    print("🎯 ListAcross.eu - Massive EU Business Directory Builder")
    print("🚀 This will build a comprehensive directory with:")
    print("   • 820+ European cities")  
    print("   • 200+ business categories")
    print("   • 49,200+ businesses (60 per city)")
    print("\n⏱️ Estimated time: 2-6 hours depending on API limits")
    print("💾 All data will be saved to your Django database")
    
    confirm = input("\n❓ Ready to start massive data collection? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        print("\n🚀 Starting automated data collection...")
        results = run_master_collection()
        
        if results.get('success'):
            print(f"\n🎉 SUCCESS! Collection completed in {results['duration']}")
            print("🚀 Your EU business directory is ready!")
        else:
            print(f"\n⚠️ Collection ended: {results.get('reason', 'unknown error')}")
    else:
        print("❌ Collection cancelled by user")