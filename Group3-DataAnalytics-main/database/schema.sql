-- Consumer360 Database Schema
-- Star Schema Design for Analytics

-- Drop existing tables
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_location CASCADE;
DROP TABLE IF EXISTS rfm_scores CASCADE;
DROP TABLE IF EXISTS customer_segments CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table for authentication
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer' CHECK (role IN ('admin', 'analyst', 'viewer')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    acquisition_date DATE NOT NULL,
    customer_status VARCHAR(20) DEFAULT 'Active' CHECK (customer_status IN ('Active', 'Inactive', 'Churned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Product
CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_price DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2),
    supplier VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_year INT NOT NULL,
    week_of_year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT false,
    fiscal_year INT,
    fiscal_quarter INT
);

-- Dimension: Location
CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    store_code VARCHAR(50) UNIQUE NOT NULL,
    store_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    region VARCHAR(100),
    store_type VARCHAR(50),
    opened_date DATE,
    is_active BOOLEAN DEFAULT true
);

-- Fact: Sales
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    customer_id INT NOT NULL REFERENCES dim_customer(customer_id),
    product_id INT NOT NULL REFERENCES dim_product(product_id),
    date_id INT NOT NULL REFERENCES dim_date(date_id),
    location_id INT NOT NULL REFERENCES dim_location(location_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    transaction_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFM Scores Table
CREATE TABLE rfm_scores (
    rfm_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES dim_customer(customer_id),
    recency_days INT NOT NULL,
    frequency INT NOT NULL,
    monetary DECIMAL(12, 2) NOT NULL,
    recency_score INT NOT NULL CHECK (recency_score BETWEEN 1 AND 5),
    frequency_score INT NOT NULL CHECK (frequency_score BETWEEN 1 AND 5),
    monetary_score INT NOT NULL CHECK (monetary_score BETWEEN 1 AND 5),
    rfm_score DECIMAL(3, 2) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_id, calculated_at)
);

-- Customer Segments Lookup
CREATE TABLE customer_segments (
    segment_id SERIAL PRIMARY KEY,
    segment_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    min_rfm_score DECIMAL(3, 2),
    max_rfm_score DECIMAL(3, 2),
    marketing_action TEXT,
    priority INT,
    color_code VARCHAR(7)
);

-- Indexes for performance
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX idx_fact_sales_location ON fact_sales(location_id);
CREATE INDEX idx_fact_sales_transaction_timestamp ON fact_sales(transaction_timestamp);
CREATE INDEX idx_dim_customer_code ON dim_customer(customer_code);
CREATE INDEX idx_dim_customer_status ON dim_customer(customer_status);
CREATE INDEX idx_dim_product_category ON dim_product(category);
CREATE INDEX idx_dim_date_date ON dim_date(date);
CREATE INDEX idx_rfm_scores_customer ON rfm_scores(customer_id);
CREATE INDEX idx_rfm_scores_segment ON rfm_scores(segment);

-- Insert default customer segments
INSERT INTO customer_segments (segment_name, description, min_rfm_score, max_rfm_score, marketing_action, priority, color_code) VALUES
('Champions', 'Best customers who bought recently, buy often and spend the most', 4.5, 5.0, 'Reward them, early access to new products, VIP treatment', 1, '#10b981'),
('Loyal Customers', 'Spend good money with us often. Responsive to promotions', 4.0, 4.4, 'Upsell higher value products, ask for reviews, engage them', 2, '#3b82f6'),
('Potential Loyalists', 'Recent customers with average frequency and monetary value', 3.5, 3.9, 'Offer membership/loyalty program, recommend products', 3, '#06b6d4'),
('New Customers', 'Bought recently but not frequently', 3.0, 3.4, 'Provide onboarding support, build relationship, offer discounts', 4, '#8b5cf6'),
('Promising', 'Recent shoppers but haven''t spent much', 2.5, 2.9, 'Create brand awareness, offer free trials', 5, '#f59e0b'),
('Hibernating', 'Last purchase was some time ago, low spenders', 2.0, 2.4, 'Win-back campaigns, special offers, surveys', 6, '#f97316'),
('At Risk', 'Spent big money, purchased often but long time ago', 1.5, 1.9, 'Send personalized emails, limited time offers, recommend products', 7, '#ef4444'),
('Lost', 'Lowest recency, frequency and monetary scores', 1.0, 1.4, 'Revive interest with reach out campaign, ignore otherwise', 8, '#64748b');

-- Create views for common queries
CREATE OR REPLACE VIEW v_customer_summary AS
SELECT 
    c.customer_id,
    c.customer_code,
    c.first_name || ' ' || c.last_name AS full_name,
    c.email,
    c.customer_status,
    r.recency_days,
    r.frequency,
    r.monetary,
    r.rfm_score,
    r.segment,
    c.acquisition_date,
    (SELECT MAX(transaction_timestamp) FROM fact_sales WHERE customer_id = c.customer_id) AS last_purchase_date
FROM dim_customer c
LEFT JOIN LATERAL (
    SELECT * FROM rfm_scores 
    WHERE customer_id = c.customer_id 
    ORDER BY calculated_at DESC 
    LIMIT 1
) r ON true;

CREATE OR REPLACE VIEW v_sales_summary AS
SELECT 
    d.date,
    d.month_name,
    d.year,
    COUNT(DISTINCT f.transaction_id) AS transaction_count,
    COUNT(DISTINCT f.customer_id) AS unique_customers,
    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS total_revenue,
    AVG(f.total_amount) AS avg_order_value
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.date, d.month_name, d.year;

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_dim_customer_updated_at BEFORE UPDATE ON dim_customer
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dim_product_updated_at BEFORE UPDATE ON dim_product
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO consumer360_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO consumer360_app;

COMMENT ON TABLE fact_sales IS 'Fact table containing all sales transactions';
COMMENT ON TABLE dim_customer IS 'Customer dimension with demographic information';
COMMENT ON TABLE dim_product IS 'Product dimension with product details';
COMMENT ON TABLE dim_date IS 'Date dimension for time-based analysis';
COMMENT ON TABLE dim_location IS 'Store location dimension';
COMMENT ON TABLE rfm_scores IS 'RFM analysis scores for customer segmentation';
