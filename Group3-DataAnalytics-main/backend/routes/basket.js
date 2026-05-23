const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');

router.get('/rules', authenticateToken, (req, res) => {
  res.json({ success: true, message: 'Market basket rules endpoint - Coming soon' });
});

module.exports = router;
