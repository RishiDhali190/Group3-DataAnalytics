const express = require('express');
const router = express.Router();
const db = require('../config/database');
const { authenticateToken } = require('../middleware/auth');

/**
 * @route   GET /api/v1/dashboard/kpis
 * @desc    Get key performance indicators
 * @access  Private
 */
router.get('/kpis', authenticateToken, async (req, res) => {
  try {
    const { startDate, endDate } = req.query;
    
    // Total Revenue
    const revenueQuery = `
      SELECT COALESCE(SUM(total_amount), 0) as total_revenue
      FROM fact_sales
      WHERE transaction_timestamp >= COALESCE($1, '2023-01-01')
        AND transaction_timestamp <= COALESCE($2, CURRENT_DATE)
    `;
    const revenueResult = await db.query(revenueQuery, [startDate, endDate]);
    
    // Total Customers
    const customersQuery = `SELECT COUNT(*) as total_customers FROM dim_customer WHERE customer_status = 'Active'`;
    const customersResult = await db.query(customersQuery);
    
    // Active Customers (purchased in last 90 days)
    const activeQuery = `
      SELECT COUNT(DISTINCT customer_id) as active_customers
      FROM fact_sales
      WHERE transaction_timestamp >= CURRENT_DATE - INTERVAL '90 days'
    `;
    const activeResult = await db.query(activeQuery);
    
    // Retention Rate
    const retentionQuery = `
      WITH cohort AS (
        SELECT customer_id, MIN(DATE_TRUNC('month', transaction_timestamp)) as cohort_month
        FROM fact_sales
        GROUP BY customer_id
      ),
      retention AS (
        SELECT 
          c.cohort_month,
          COUNT(DISTINCT CASE WHEN f.transaction_timestamp >= c.cohort_month + INTERVAL '1 month' 
                              AND f.transaction_timestamp < c.cohort_month + INTERVAL '2 months' 
                              THEN f.customer_id END) * 100.0 / COUNT(DISTINCT c.customer_id) as retention_rate
        FROM cohort c
        LEFT JOIN fact_sales f ON c.customer_id = f.customer_id
        GROUP BY c.cohort_month
      )
      SELECT AVG(retention_rate) as avg_retention_rate FROM retention
    `;
    const retentionResult = await db.query(retentionQuery);
    
    // Average Order Value
    const aovQuery = `
      SELECT AVG(total_amount) as avg_order_value
      FROM fact_sales
      WHERE transaction_timestamp >= COALESCE($1, '2023-01-01')
        AND transaction_timestamp <= COALESCE($2, CURRENT_DATE)
    `;
    const aovResult = await db.query(aovQuery, [startDate, endDate]);
    
    // Customer Lifetime Value
    const clvQuery = `
      SELECT AVG(customer_total) as avg_clv
      FROM (
        SELECT customer_id, SUM(total_amount) as customer_total
        FROM fact_sales
        GROUP BY customer_id
      ) customer_totals
    `;
    const clvResult = await db.query(clvQuery);
    
    res.json({
      success: true,
      data: {
        totalRevenue: parseFloat(revenueResult.rows[0].total_revenue),
        totalCustomers: parseInt(customersResult.rows[0].total_customers),
        activeCustomers: parseInt(activeResult.rows[0].active_customers),
        retentionRate: parseFloat(retentionResult.rows[0].avg_retention_rate || 0),
        avgOrderValue: parseFloat(aovResult.rows[0].avg_order_value || 0),
        customerLTV: parseFloat(clvResult.rows[0].avg_clv || 0)
      }
    });
  } catch (error) {
    console.error('Dashboard KPIs error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

/**
 * @route   GET /api/v1/dashboard/revenue-trend
 * @desc    Get monthly revenue trend
 * @access  Private
 */
router.get('/revenue-trend', authenticateToken, async (req, res) => {
  try {
    const { months = 12 } = req.query;
    
    const query = `
      SELECT 
        TO_CHAR(d.date, 'Mon YYYY') as month,
        COALESCE(SUM(f.total_amount), 0) as revenue
      FROM dim_date d
      LEFT JOIN fact_sales f ON d.date_id = f.date_id
      WHERE d.date >= CURRENT_DATE - INTERVAL '${months} months'
      GROUP BY d.year, d.month, TO_CHAR(d.date, 'Mon YYYY')
      ORDER BY d.year, d.month
    `;
    
    const result = await db.query(query);
    
    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Revenue trend error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

/**
 * @route   GET /api/v1/dashboard/top-products
 * @desc    Get top selling products
 * @access  Private
 */
router.get('/top-products', authenticateToken, async (req, res) => {
  try {
    const { limit = 10 } = req.query;
    
    const query = `
      SELECT 
        p.product_name,
        p.category,
        COUNT(f.sale_id) as order_count,
        SUM(f.quantity) as total_quantity,
        SUM(f.total_amount) as total_revenue
      FROM fact_sales f
      JOIN dim_product p ON f.product_id = p.product_id
      GROUP BY p.product_id, p.product_name, p.category
      ORDER BY total_revenue DESC
      LIMIT $1
    `;
    
    const result = await db.query(query, [limit]);
    
    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Top products error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

/**
 * @route   GET /api/v1/dashboard/recent-transactions
 * @desc    Get recent transactions
 * @access  Private
 */
router.get('/recent-transactions', authenticateToken, async (req, res) => {
  try {
    const { limit = 10 } = req.query;
    
    const query = `
      SELECT 
        f.transaction_id,
        c.first_name || ' ' || c.last_name as customer_name,
        f.total_amount,
        f.transaction_timestamp,
        r.segment,
        f.payment_method
      FROM fact_sales f
      JOIN dim_customer c ON f.customer_id = c.customer_id
      LEFT JOIN LATERAL (
        SELECT segment FROM rfm_scores 
        WHERE customer_id = c.customer_id 
        ORDER BY calculated_at DESC 
        LIMIT 1
      ) r ON true
      ORDER BY f.transaction_timestamp DESC
      LIMIT $1
    `;
    
    const result = await db.query(query, [limit]);
    
    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Recent transactions error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
