const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 1000 // limit each IP to 1000 requests per windowMs
});
app.use(limiter);

// Initialize SQLite database
const db = new sqlite3.Database('./database/businesses.db');

// Create tables
db.serialize(() => {
    // Businesses table
    db.run(`CREATE TABLE IF NOT EXISTS businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    address TEXT,
    city TEXT,
    country TEXT,
    country_code TEXT,
    phone TEXT,
    website TEXT,
    email TEXT,
    latitude REAL,
    longitude REAL,
    description TEXT,
    opening_hours TEXT,
    source TEXT,
    plan_type TEXT DEFAULT 'free',
    visibility_radius INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

    // Users/Business owners table
    db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    business_id INTEGER,
    plan_type TEXT DEFAULT 'free',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses (id)
  )`);

    // Reviews table
    db.run(`CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    reviewer_name TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses (id)
  )`);

    console.log('Database tables initialized');
});

// API Routes

// Get all businesses with filtering and pagination
app.get('/api/businesses', (req, res) => {
    const {
        country,
        city,
        category,
        search,
        latitude,
        longitude,
        radius = 50, // km
        page = 1,
        limit = 20
    } = req.query;

    let query = 'SELECT * FROM businesses WHERE 1=1';
    const params = [];

    // Apply filters
    if (country) {
        query += ' AND country_code = ?';
        params.push(country.toLowerCase());
    }

    if (city) {
        query += ' AND LOWER(city) LIKE ?';
        params.push(`%${city.toLowerCase()}%`);
    }

    if (category) {
        query += ' AND LOWER(category) LIKE ?';
        params.push(`%${category.toLowerCase()}%`);
    }

    if (search) {
        query += ' AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)';
        params.push(`%${search.toLowerCase()}%`, `%${search.toLowerCase()}%`);
    }

    // Geographic filtering (simplified - in production use proper geospatial queries)
    if (latitude && longitude) {
        const lat = parseFloat(latitude);
        const lng = parseFloat(longitude);
        const radiusKm = parseFloat(radius);

        // Simple bounding box calculation (not accurate for large distances)
        const latDelta = radiusKm / 111.0; // Rough conversion
        const lngDelta = radiusKm / (111.0 * Math.cos(lat * Math.PI / 180));

        query += ' AND latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?';
        params.push(lat - latDelta, lat + latDelta, lng - lngDelta, lng + lngDelta);
    }

    // Pagination
    const offset = (parseInt(page) - 1) * parseInt(limit);
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?';
    params.push(parseInt(limit), offset);

    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        // Parse opening_hours JSON string back to object
        const businesses = rows.map(row => ({
            ...row,
            opening_hours: row.opening_hours ? JSON.parse(row.opening_hours) : null
        }));

        res.json({
            businesses,
            pagination: {
                page: parseInt(page),
                limit: parseInt(limit),
                total: businesses.length
            }
        });
    });
});

// Get single business by ID
app.get('/api/businesses/:id', (req, res) => {
    const { id } = req.params;

    db.get('SELECT * FROM businesses WHERE id = ?', [id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        if (!row) {
            res.status(404).json({ error: 'Business not found' });
            return;
        }

        // Parse opening_hours and get reviews
        const business = {
            ...row,
            opening_hours: row.opening_hours ? JSON.parse(row.opening_hours) : null
        };

        // Get reviews for this business
        db.all('SELECT * FROM reviews WHERE business_id = ? ORDER BY created_at DESC', [id], (err, reviews) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }

            res.json({
                ...business,
                reviews
            });
        });
    });
});

// Search businesses
app.get('/api/search', (req, res) => {
    const { q, country, category } = req.query;

    if (!q) {
        res.status(400).json({ error: 'Search query is required' });
        return;
    }

    let query = `
    SELECT *, 
    (CASE 
      WHEN LOWER(name) LIKE ? THEN 3
      WHEN LOWER(category) LIKE ? THEN 2
      WHEN LOWER(description) LIKE ? THEN 1
      ELSE 0
    END) as relevance
    FROM businesses 
    WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?
  `;

    const searchTerm = `%${q.toLowerCase()}%`;
    const params = [searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, searchTerm];

    if (country) {
        query += ' AND country_code = ?';
        params.push(country.toLowerCase());
    }

    if (category) {
        query += ' AND LOWER(category) LIKE ?';
        params.push(`%${category.toLowerCase()}%`);
    }

    query += ' ORDER BY relevance DESC, name ASC LIMIT 50';

    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        const results = rows.map(row => ({
            ...row,
            opening_hours: row.opening_hours ? JSON.parse(row.opening_hours) : null
        }));

        res.json({ results });
    });
});

// Get businesses by country
app.get('/api/countries/:countryCode/businesses', (req, res) => {
    const { countryCode } = req.params;
    const { page = 1, limit = 20 } = req.query;

    const offset = (parseInt(page) - 1) * parseInt(limit);

    db.all(
        'SELECT * FROM businesses WHERE country_code = ? ORDER BY city, name LIMIT ? OFFSET ?',
        [countryCode.toLowerCase(), parseInt(limit), offset],
        (err, rows) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }

            const businesses = rows.map(row => ({
                ...row,
                opening_hours: row.opening_hours ? JSON.parse(row.opening_hours) : null
            }));

            res.json({ businesses });
        }
    );
});

// Get statistics
app.get('/api/stats', (req, res) => {
    const queries = {
        totalBusinesses: 'SELECT COUNT(*) as count FROM businesses',
        businessesByCountry: `
      SELECT country, country_code, COUNT(*) as count 
      FROM businesses 
      GROUP BY country, country_code 
      ORDER BY count DESC
    `,
        businessesByCategory: `
      SELECT category, COUNT(*) as count 
      FROM businesses 
      GROUP BY category 
      ORDER BY count DESC 
      LIMIT 10
    `,
        topCities: `
      SELECT city, country, COUNT(*) as count 
      FROM businesses 
      GROUP BY city, country 
      ORDER BY count DESC 
      LIMIT 20
    `
    };

    const results = {};
    let completedQueries = 0;
    const totalQueries = Object.keys(queries).length;

    Object.entries(queries).forEach(([key, query]) => {
        db.all(query, [], (err, rows) => {
            if (err) {
                console.error(`Error in ${key}:`, err);
                results[key] = [];
            } else {
                results[key] = rows;
            }

            completedQueries++;
            if (completedQueries === totalQueries) {
                res.json(results);
            }
        });
    });
});

// Add a review
app.post('/api/businesses/:id/reviews', (req, res) => {
    const { id } = req.params;
    const { reviewer_name, rating, comment } = req.body;

    if (!rating || rating < 1 || rating > 5) {
        res.status(400).json({ error: 'Rating must be between 1 and 5' });
        return;
    }

    db.run(
        'INSERT INTO reviews (business_id, reviewer_name, rating, comment) VALUES (?, ?, ?, ?)',
        [id, reviewer_name || 'Anonymous', rating, comment],
        function (err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }

            res.status(201).json({
                id: this.lastID,
                message: 'Review added successfully'
            });
        }
    );
});

// Import CSV data (admin endpoint)
app.post('/api/admin/import-csv', (req, res) => {
    const csvPath = req.body.csvPath;

    if (!csvPath || !fs.existsSync(csvPath)) {
        res.status(400).json({ error: 'Valid CSV file path is required' });
        return;
    }

    const businesses = [];

    fs.createReadStream(csvPath)
        .pipe(csv())
        .on('data', (data) => {
            businesses.push(data);
        })
        .on('end', () => {
            let insertedCount = 0;
            let errorCount = 0;

            businesses.forEach((business, index) => {
                const {
                    name, category, address, city, country, country_code,
                    phone, website, email, latitude, longitude, description,
                    opening_hours, source
                } = business;

                db.run(
                    `INSERT INTO businesses 
           (name, category, address, city, country, country_code, phone, website, email, 
            latitude, longitude, description, opening_hours, source) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                    [name, category, address, city, country, country_code?.toLowerCase(),
                        phone, website, email, parseFloat(latitude) || null,
                        parseFloat(longitude) || null, description, opening_hours, source],
                    function (err) {
                        if (err) {
                            console.error(`Error inserting business ${index}:`, err);
                            errorCount++;
                        } else {
                            insertedCount++;
                        }

                        // Check if this is the last insertion
                        if (insertedCount + errorCount === businesses.length) {
                            res.json({
                                message: 'CSV import completed',
                                inserted: insertedCount,
                                errors: errorCount,
                                total: businesses.length
                            });
                        }
                    }
                );
            });
        })
        .on('error', (err) => {
            res.status(500).json({ error: 'Error reading CSV file: ' + err.message });
        });
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
    });
});

// Create database directory
const dbDir = path.join(__dirname, 'database');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

app.listen(PORT, () => {
    console.log(`ListAcross EU API server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/api/health`);
});