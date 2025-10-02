// Business Listing Page JavaScript

// Override the flag slider to prevent conflicts
window.flagSliderInitialized = true;

document.addEventListener('DOMContentLoaded', function () {
    // Stop any existing animations from app.js
    const track = document.querySelector('.flags .track');
    if (track) {
        track.style.transform = 'none';
        track.style.animation = 'none';
    }

    // Extract business ID from URL parameters or use demo data
    const urlParams = new URLSearchParams(window.location.search);
    const businessId = urlParams.get('id') || 'demo';

    // Load business data (this would come from your API)
    loadBusinessData(businessId);

    // Load similar businesses
    loadSimilarBusinesses(businessId);

    // Initialize map
    initializeMap();

    // Load reviews
    loadReviews(businessId);
});

function loadBusinessData(businessId) {
    // Demo database - in production this would come from your API
    const demoBusinesses = {
        'demo': {
            name: "Café Central Vienna",
            category: "Restaurant & Café",
            address: "Herrengasse 14, 1010 Vienna",
            city: "Vienna",
            country: "Austria",
            country_code: "at",
            phone: "+43 1 533 3763",
            email: "info@cafecentral.wien",
            website: "www.cafecentral.wien",
            description: "Historic Viennese coffeehouse serving traditional Austrian cuisine and world-famous coffee since 1876. Located in the heart of Vienna, Café Central has been a meeting place for intellectuals, artists, and coffee lovers for over a century.",
            image: "assets/demo/cafe-central.jpg",
            rating: 4.5,
            reviews_count: 1247,
            hours: {
                monday: "7:30 AM - 10:00 PM",
                tuesday: "7:30 AM - 10:00 PM",
                wednesday: "7:30 AM - 10:00 PM",
                thursday: "7:30 AM - 10:00 PM",
                friday: "7:30 AM - 10:00 PM",
                saturday: "9:00 AM - 10:00 PM",
                sunday: "10:00 AM - 6:00 PM"
            },
            coordinates: { lat: 48.2082, lng: 16.3738 }
        },
        '2': {
            name: "La Brasserie du Marché",
            category: "French Restaurant",
            address: "15 Rue des Martyrs, 75009 Paris",
            city: "Paris",
            country: "France",
            country_code: "fr",
            phone: "+33 1 48 78 62 73",
            email: "contact@brasseriedumarche.fr",
            website: "www.brasseriedumarche.fr",
            description: "Authentic French brasserie in the heart of Montmartre, serving traditional French cuisine with fresh ingredients from local markets. Family-owned since 1952.",
            image: "assets/demo/french-brasserie.jpg",
            rating: 4.7,
            reviews_count: 892,
            hours: {
                monday: "12:00 PM - 2:00 PM, 7:00 PM - 11:00 PM",
                tuesday: "12:00 PM - 2:00 PM, 7:00 PM - 11:00 PM",
                wednesday: "12:00 PM - 2:00 PM, 7:00 PM - 11:00 PM",
                thursday: "12:00 PM - 2:00 PM, 7:00 PM - 11:00 PM",
                friday: "12:00 PM - 2:00 PM, 7:00 PM - 11:30 PM",
                saturday: "7:00 PM - 11:30 PM",
                sunday: "Closed"
            },
            coordinates: { lat: 48.8566, lng: 2.3522 }
        },
        '3': {
            name: "Berlin Tech Solutions GmbH",
            category: "IT Services",
            address: "Alexanderplatz 1, 10178 Berlin",
            city: "Berlin",
            country: "Germany",
            country_code: "de",
            phone: "+49 30 12345678",
            email: "info@berlintech.de",
            website: "www.berlintech-solutions.de",
            description: "Leading IT consulting and software development company specializing in fintech and e-commerce solutions. Serving clients across Europe since 2010.",
            image: "assets/demo/tech-office.jpg",
            rating: 4.3,
            reviews_count: 156,
            hours: {
                monday: "9:00 AM - 6:00 PM",
                tuesday: "9:00 AM - 6:00 PM",
                wednesday: "9:00 AM - 6:00 PM",
                thursday: "9:00 AM - 6:00 PM",
                friday: "9:00 AM - 5:00 PM",
                saturday: "Closed",
                sunday: "Closed"
            },
            coordinates: { lat: 52.5200, lng: 13.4050 }
        },
        '4': {
            name: "Trattoria Bella Napoli",
            category: "Italian Restaurant",
            address: "Via Roma 23, 00187 Rome",
            city: "Rome",
            country: "Italy",
            country_code: "it",
            phone: "+39 06 1234567",
            email: "info@bellanapoli.it",
            website: "www.trattoriabellanapoli.it",
            description: "Authentic Neapolitan cuisine in the heart of Rome. Fresh pasta made daily, wood-fired pizza, and the finest Italian wines. Family recipes passed down through generations.",
            image: "assets/demo/italian-trattoria.jpg",
            rating: 4.8,
            reviews_count: 2341,
            hours: {
                monday: "12:00 PM - 3:00 PM, 6:00 PM - 11:00 PM",
                tuesday: "12:00 PM - 3:00 PM, 6:00 PM - 11:00 PM",
                wednesday: "12:00 PM - 3:00 PM, 6:00 PM - 11:00 PM",
                thursday: "12:00 PM - 3:00 PM, 6:00 PM - 11:00 PM",
                friday: "12:00 PM - 3:00 PM, 6:00 PM - 11:30 PM",
                saturday: "12:00 PM - 11:30 PM",
                sunday: "12:00 PM - 10:00 PM"
            },
            coordinates: { lat: 41.9028, lng: 12.4964 }
        },
        '5': {
            name: "Amsterdam Bike Rental",
            category: "Tourism & Recreation",
            address: "Damrak 62, 1012 LM Amsterdam",
            city: "Amsterdam",
            country: "Netherlands",
            country_code: "nl",
            phone: "+31 20 1234567",
            email: "rent@amsterdambikes.nl",
            website: "www.amsterdambike-rental.nl",
            description: "Premium bike rental service in Amsterdam city center. Electric bikes, city bikes, and guided tours available. Explore Amsterdam like a local!",
            image: "assets/demo/bike-rental.jpg",
            rating: 4.6,
            reviews_count: 743,
            hours: {
                monday: "8:00 AM - 7:00 PM",
                tuesday: "8:00 AM - 7:00 PM",
                wednesday: "8:00 AM - 7:00 PM",
                thursday: "8:00 AM - 7:00 PM",
                friday: "8:00 AM - 8:00 PM",
                saturday: "8:00 AM - 8:00 PM",
                sunday: "9:00 AM - 6:00 PM"
            },
            coordinates: { lat: 52.3676, lng: 4.9041 }
        }
    };
    
    const demoData = demoBusinesses[businessId] || demoBusinesses['demo'];

    // Update page content with business data
    updatePageContent(demoData);
}

function updatePageContent(data) {
    // Update title and meta description
    document.title = `${data.name} - ${data.city}, ${data.country} | ListAcross EU`;

    // Update business header
    document.querySelector('.business-name').textContent = data.name;
    document.querySelector('.category').textContent = data.category;
    document.querySelector('.location').textContent = `📍 ${data.address}, ${data.city}, ${data.country}`;
    document.querySelector('.rating-text').textContent = `(${data.reviews_count} reviews)`;

    // Update business description
    document.querySelector('.business-description p').textContent = data.description;

    // Update contact information
    const contactItems = document.querySelectorAll('.contact-item');
    contactItems[0].innerHTML = `<strong>Phone:</strong> ${data.phone}`;
    contactItems[1].innerHTML = `<strong>Email:</strong> ${data.email}`;
    contactItems[2].innerHTML = `<strong>Website:</strong> <a href="https://${data.website}" target="_blank">${data.website}</a>`;
    contactItems[3].innerHTML = `<strong>Address:</strong> ${data.address}`;

    // Update opening hours
    const hoursGrid = document.querySelector('.hours-grid');
    hoursGrid.innerHTML = Object.entries(data.hours).map(([day, hours]) =>
        `<div class="day">
            <span>${day.charAt(0).toUpperCase() + day.slice(1)}</span>
            <span>${hours}</span>
        </div>`
    ).join('');

    // Update breadcrumb
    const breadcrumb = document.querySelector('.breadcrumb');
    breadcrumb.innerHTML = `
        <div class="container">
            <a href="index.html">Home</a> > 
            <a href="country.html?c=${data.country_code}">${data.country}</a> > 
            <a href="city.html?c=${data.country_code}&city=${data.city}">${data.city}</a> > 
            <span>${data.name}</span>
        </div>
    `;
}

function loadSimilarBusinesses(businessId) {
    // Demo similar businesses
    const similarBusinesses = [
        {
            name: "Demel Café",
            category: "Bakery & Café",
            rating: 4.3,
            distance: "0.3 km"
        },
        {
            name: "Sacher Hotel Café",
            category: "Hotel & Restaurant",
            rating: 4.6,
            distance: "0.5 km"
        },
        {
            name: "Landtmann Café",
            category: "Restaurant & Café",
            rating: 4.2,
            distance: "0.8 km"
        }
    ];

    const container = document.getElementById('similar-businesses-list');
    container.innerHTML = similarBusinesses.map(business => `
        <div class="similar-business-item" style="padding: 12px 0; border-bottom: 1px solid #f3f4f6;">
            <div style="font-weight: 600; font-size: 14px;">${business.name}</div>
            <div style="font-size: 12px; color: var(--muted); margin: 4px 0;">
                ${business.category} • ${business.distance} away
            </div>
            <div style="color: #fbbf24; font-size: 12px;">
                ★★★★☆ ${business.rating}
            </div>
        </div>
    `).join('');
}

function loadReviews(businessId) {
    // Demo reviews
    const reviews = [
        {
            name: "Maria S.",
            rating: 5,
            date: "2 weeks ago",
            text: "Absolutely wonderful atmosphere! The coffee was exceptional and the Sachertorte was to die for. True Viennese experience."
        },
        {
            name: "James K.",
            rating: 4,
            date: "1 month ago",
            text: "Historic charm with great service. A bit pricey but worth it for the experience. The architecture alone is worth a visit."
        },
        {
            name: "Sophie L.",
            rating: 5,
            date: "2 months ago",
            text: "Perfect spot for breakfast or afternoon coffee. The staff is knowledgeable about the history and very welcoming to tourists."
        }
    ];

    const container = document.getElementById('reviews-container');
    container.innerHTML = reviews.map(review => `
        <div class="review-item" style="padding: 16px 0; border-bottom: 1px solid #f3f4f6;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <strong style="font-size: 14px;">${review.name}</strong>
                    <div style="color: #fbbf24; font-size: 14px;">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</div>
                </div>
                <span style="font-size: 12px; color: var(--muted);">${review.date}</span>
            </div>
            <p style="margin: 0; font-size: 14px; line-height: 1.5;">${review.text}</p>
        </div>
    `).join('');
}

function initializeMap() {
    // Placeholder for map initialization
    // In a real implementation, you would integrate with Google Maps, Mapbox, or OpenStreetMap
    const mapContainer = document.getElementById('business-map');
    mapContainer.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: var(--muted);">
            🗺️ Interactive Map Loading...
        </div>
    `;

    // TODO: Implement actual map integration
    // Example with Google Maps:
    // const map = new google.maps.Map(mapContainer, {
    //     center: { lat: 48.2082, lng: 16.3738 },
    //     zoom: 15
    // });
}