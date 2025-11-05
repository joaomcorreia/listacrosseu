from django.core.management.base import BaseCommand
from django.db.models import Count
from businesses.models import Business
from django.utils import timezone


class Command(BaseCommand):
    help = 'Validate address duplicates and identify legitimate multi-tenant locations'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Automatically flag legitimate multi-tenant locations',
        )
        parser.add_argument(
            '--min-businesses',
            type=int,
            default=3,
            help='Minimum number of businesses at same address to analyze (default: 3)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🏢 Analyzing Address Duplicates for Multi-Tenant Locations...')
        )
        
        min_businesses = options['min_businesses']
        fix_mode = options['fix']
        
        # Find addresses with multiple businesses
        address_groups = Business.objects.exclude(
            address__isnull=True
        ).exclude(
            address=''
        ).values(
            'address', 'city'
        ).annotate(
            count=Count('id')
        ).filter(
            count__gte=min_businesses
        ).order_by('-count')
        
        total_groups = len(address_groups)
        legitimate_locations = 0
        suspicious_groups = 0
        
        self.stdout.write(f"Found {total_groups} addresses with {min_businesses}+ businesses")
        self.stdout.write("=" * 80)
        
        for group in address_groups:
            businesses = Business.objects.filter(
                address=group['address'],
                city_id=group['city']
            ).order_by('name')
            
            # Analyze if this looks like a legitimate multi-tenant location
            business_names = [b.name for b in businesses]
            categories = list(set([b.category.name if b.category else 'Uncategorized' for b in businesses]))
            
            # Indicators of legitimate multi-tenant location:
            # 1. Many different categories
            # 2. No similar business names
            # 3. Different owners (if available)
            # 4. Well-known chain stores together
            
            similarity_score = self.calculate_similarity_score(business_names)
            category_diversity = len(categories)
            
            is_legitimate = (
                category_diversity >= min(3, len(business_names) * 0.6) and  # Good category diversity
                similarity_score < 0.3 and  # Low name similarity
                len(business_names) >= min_businesses  # Sufficient number of businesses
            )
            
            if is_legitimate:
                legitimate_locations += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ LEGITIMATE: {group['address'][:60]}...")
                )
                self.stdout.write(f"   📊 {len(business_names)} businesses, {category_diversity} categories")
                self.stdout.write(f"   🏪 Businesses: {', '.join(business_names[:5])}")
                if len(business_names) > 5:
                    self.stdout.write(f"   ... and {len(business_names) - 5} more")
                    
                if fix_mode:
                    # Add a note to these businesses indicating they're in a legitimate multi-tenant location
                    businesses.update(
                        notes=f"Multi-tenant location validated on {timezone.now().date()}"
                    )
                    
            else:
                suspicious_groups += 1
                self.stdout.write(
                    self.style.WARNING(f"⚠️  SUSPICIOUS: {group['address'][:60]}...")
                )
                self.stdout.write(f"   📊 {len(business_names)} businesses, similarity: {similarity_score:.2f}")
                self.stdout.write(f"   🔍 Names: {', '.join(business_names)}")
                
                # Check for potential issues
                issues = []
                if similarity_score > 0.5:
                    issues.append("High name similarity")
                if category_diversity <= 1:
                    issues.append("Same category")
                if len(set([b.owner.username if b.owner else 'No owner' for b in businesses])) <= 1:
                    issues.append("Same owner")
                    
                if issues:
                    self.stdout.write(f"   ⚠️  Issues: {', '.join(issues)}")
            
            self.stdout.write("")  # Empty line for readability
        
        # Summary
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS(f"📈 ANALYSIS COMPLETE:"))
        self.stdout.write(f"   🏢 Total address groups analyzed: {total_groups}")
        self.stdout.write(f"   ✅ Legitimate multi-tenant locations: {legitimate_locations}")
        self.stdout.write(f"   ⚠️  Suspicious duplicate groups: {suspicious_groups}")
        self.stdout.write(f"   📊 Legitimacy rate: {(legitimate_locations/total_groups)*100:.1f}%")
        
        if fix_mode:
            self.stdout.write(f"   💾 Updated {legitimate_locations} business groups with validation notes")
        else:
            self.stdout.write("   💡 Use --fix to automatically flag legitimate locations")
            
        # Recommendations
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("📝 RECOMMENDATIONS:"))
        
        if suspicious_groups > 0:
            self.stdout.write(f"   🔍 Review {suspicious_groups} suspicious groups manually")
            self.stdout.write("   🚨 These may contain actual duplicate businesses")
            
        if legitimate_locations > 0:
            self.stdout.write(f"   ✅ {legitimate_locations} locations appear to be legitimate multi-tenant buildings")
            self.stdout.write("   🏪 Consider these normal for shopping malls, office buildings, etc.")
            
        self.stdout.write("   💡 Focus duplicate cleanup on exact name matches and high similarity scores")
    
    def calculate_similarity_score(self, names):
        """Calculate average similarity between all business names"""
        if len(names) <= 1:
            return 0
            
        from businesses.models import Business
        
        total_comparisons = 0
        total_similarity = 0
        
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                # Normalize names
                temp_business = Business()
                norm1 = temp_business.normalize_business_name(name1)
                norm2 = temp_business.normalize_business_name(name2)
                
                # Calculate word overlap similarity
                words1 = set(norm1.split())
                words2 = set(norm2.split())
                
                if words1 and words2:
                    overlap = len(words1 & words2)
                    union = len(words1 | words2)
                    similarity = overlap / union if union > 0 else 0
                    
                    total_similarity += similarity
                    total_comparisons += 1
        
        return total_similarity / total_comparisons if total_comparisons > 0 else 0