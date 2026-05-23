const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');

router.get('/retention', authenticateToken, (req, res) => {
  res.json({ success: true, message: 'Cohort retention endpoint - Coming soon' });
});

module.exports = router;
