# 🚀 Consumer360 - Quick Start Guide

Get the full-stack retail analytics platform running in **5 minutes**!

---

## Option 1: Docker (Easiest - Recommended)

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum

### Steps

```bash
# 1. Navigate to project directory
cd Consumer360

# 2. Start all services with Docker Compose
docker-compose up -d

# 3. Wait for services to start (30-60 seconds)
docker-compose logs -f

# 4. Access the application
```

**Access Points:**
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:5000
- 🗄️ **pgAdmin**: http://localhost:5050 (admin@consumer360.com / admin123)
- 📊 **API Health**: http://localhost:5000/health

**Default Login:**
- Email: `admin@consumer360.com`
- Password: `admin123`

---

## Option 2: Manual Setup (Full Control)

### Prerequisites
- Node.js >= 18.0.0
- Python >= 3.9
- PostgreSQL >= 14

### Step 1: Generate Sample Data

```bash
cd data
python generate_sample_data.py
```

This creates:
- `customers.csv` (5,000 customers)
- `products.csv` (200 products)
- `transactions.csv` (50,000 transactions)

### Step 2: Setup Database

```bash
# Create database
createdb consumer360_db

# Run schema
psql -d consumer360_db -f database/schema.sql

# Load data (see database/load_data.sql)
```

### Step 3: Setup Backend

```bash
cd backend

# Install dependencies
npm install

# Create environment file
copy .env.example .env

# Edit .env with your database credentials
notepad .env

# Start server
npm run dev
```

Backend runs on: http://localhost:5000

### Step 4: Setup Analytics Engine

```bash
cd analytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run RFM analysis
python rfm_engine.py
```

### Step 5: Open Frontend

```bash
# Simply open the HTML file in your browser
start frontend/index.html

# OR use a local server
cd frontend
python -m http.server 3000
```

Frontend runs on: http://localhost:3000

---

## Option 3: Automated Setup (Windows)

```bash
# Run the setup script
setup.bat
```

This automatically:
1. Checks prerequisites
2. Generates sample data
3. Installs all dependencies
4. Creates configuration files

---

## 📊 What You Get

### 1. **Dashboard**
- 6 KPI cards (Revenue, Customers, Retention, AOV, LTV)
- Revenue trend chart (12 months)
- Customer segment distribution
- Top 10 products
- Recent transactions

### 2. **RFM Segmentation**
- 8 customer segments with color coding
- RFM score distribution charts
- Segment summary table
- Marketing action recommendations

### 3. **Customer Analytics**
- Searchable customer table (5,000 customers)
- Filter by segment and status
- Customer detail modal with purchase history
- Spending trend visualization

### 4. **Cohort Analysis**
- 12-month retention heatmap
- Cohort trend analysis
- Average retention metrics

### 5. **Market Basket Analysis**
- 15 association rules
- Product affinity matrix
- Frequently bought together cards
- Cross-sell recommendations

### 6. **Reports & Exports**
- PDF export (print to PDF)
- CSV downloads
- 5 pre-built report templates

---

## 🔧 Configuration

### Backend (.env)

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=consumer360_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your_secret_key_here
JWT_EXPIRES_IN=7d

# Server
PORT=5000
NODE_ENV=development
```

### Analytics (.env)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=consumer360_db
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## 🧪 Test the API

```bash
# Health check
curl http://localhost:5000/health

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@consumer360.com","password":"admin123"}'

# Get dashboard KPIs
curl http://localhost:5000/api/v1/dashboard/kpis \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📈 Run Analytics

### RFM Analysis

```bash
cd analytics
python rfm_engine.py
```

Output:
- Calculates R, F, M scores for all customers
- Assigns segments (Champions, Loyal, At Risk, etc.)
- Saves results to `rfm_scores` table
- Generates `rfm_scores_output.csv`

### Cohort Analysis

```bash
python cohort_analysis.py
```

### Market Basket Analysis

```bash
python basket_analysis.py
```

---

## 🐛 Troubleshooting

### Database Connection Error

```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Solution:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify credentials in `.env`
3. Ensure database exists: `psql -l`

### Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solution:**
1. Change PORT in `.env`
2. Or kill the process: `npx kill-port 5000`

### Python Module Not Found

```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
1. Activate virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`

### Docker Issues

```
ERROR: Cannot connect to the Docker daemon
```

**Solution:**
1. Start Docker Desktop
2. Wait for Docker to fully start
3. Run `docker-compose up -d` again

---

## 📚 Next Steps

1. **Explore the Dashboard**: Open http://localhost:3000
2. **Check API Docs**: See `docs/API.md`
3. **Customize Segments**: Edit `database/schema.sql`
4. **Add Real Data**: Replace CSV files in `data/`
5. **Schedule Analytics**: Set up cron jobs for automated RFM refresh

---

## 🎯 Key Files

| File | Purpose |
|------|---------|
| `frontend/index.html` | Complete frontend UI (self-contained) |
| `backend/server.js` | Express API server |
| `analytics/rfm_engine.py` | RFM calculation engine |
| `database/schema.sql` | PostgreSQL star schema |
| `data/generate_sample_data.py` | Sample data generator |
| `docker-compose.yml` | Docker orchestration |

---

## 💡 Tips

- **Use Docker** for the easiest setup
- **Generate fresh data** anytime with `python generate_sample_data.py`
- **Run RFM analysis weekly** for updated segments
- **Export reports** as PDF using browser print (Ctrl+P)
- **Check logs** with `docker-compose logs -f` if using Docker

---

## 🆘 Need Help?

- 📖 Full docs: `README_FULLSTACK.md`
- 🔌 API reference: `docs/API.md`
- 🗄️ Database schema: `docs/DATABASE.md`
- 🐛 Report issues: GitHub Issues

---

**You're all set! 🎉**

Open http://localhost:3000 and start exploring your retail analytics platform!
