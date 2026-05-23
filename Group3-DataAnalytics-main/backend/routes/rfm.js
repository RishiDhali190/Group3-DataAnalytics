const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');

router.get('/scores', authenticateToken, (req, res) => {
  res.json({ success: true, message: 'RFM scores endpoint - Coming soon' });
});

module.exports = router;
