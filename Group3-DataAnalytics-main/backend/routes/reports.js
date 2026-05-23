const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');

router.get('/executive', authenticateToken, (req, res) => {
  res.json({ success: true, message: 'Executive report endpoint - Coming soon' });
});

module.exports = router;
