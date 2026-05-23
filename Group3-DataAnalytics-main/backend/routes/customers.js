const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');

router.get('/', authenticateToken, (req, res) => {
  res.json({ success: true, message: 'Customers endpoint - Coming soon' });
});

module.exports = router;
