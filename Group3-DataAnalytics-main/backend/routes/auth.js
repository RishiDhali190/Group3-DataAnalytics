const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../config/database');

/**
 * @route   POST /api/v1/auth/login
 * @desc    Login user
 * @access  Public
 */
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // For demo purposes, accept demo credentials
    if (email === 'admin@consumer360.com' && password === 'admin123') {
      const token = jwt.sign(
        { id: 1, email, role: 'admin' },
        process.env.JWT_SECRET || 'your_secret_key',
        { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
      );

      return res.json({
        success: true,
        token,
        user: {
          id: 1,
          email,
          name: 'Admin User',
          role: 'admin'
        }
      });
    }

    res.status(401).json({ success: false, message: 'Invalid credentials' });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
