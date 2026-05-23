# Consumer360 – Full-Stack Retail Analytics Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-yellow)
![PostgreSQL](https://img.shields.io/badge/postgresql-14%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Enterprise-grade retail customer analytics platform with RFM segmentation, cohort analysis, and market basket analysis.**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Dashboard │  │   RFM    │  │  Cohort  │  │  Basket  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────┐
│              BACKEND (Node.js/Express)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Auth   │  │   API    │  │  Routes  │  │   Jobs   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│           ANALYTICS ENGINE (Python)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   RFM    │  │  Cohort  │  │  Basket  │  │   ETL    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│              DATABASE (PostgreSQL)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Star Schema: Fact Sales + Dimensions (Customer,    │  │
│  │  Product, Date, Location) + RFM Scores              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Consumer360/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   ├── utils/           # Utility functions
│   │   └── App.js
│   └── package.json
│
├── backend/                  # Node.js Express API
│   ├── routes/              # API route handlers
│   │   ├── auth.js
│   │   ├── customers.js
│   │   ├── rfm.js
│   │   ├── cohort.js
│   │   ├── basket.js
│   │   ├── dashboard.js
│   │   └── reports.js
│   ├── middleware/          # Express middleware
│   ├── config/              # Configuration files
│   ├── utils/               # Utility functions
│   ├── server.js            # Main server file
│   └── package.json
│
├── analytics/                # Python analytics engine
│   ├── rfm_engine.py        # RFM analysis
│   ├── cohort_analysis.py   # Cohort retention
│   ├── basket_analysis.py   # Market basket (Apriori)
│   ├── etl_pipeline.py      # ETL data processing
│   └── requirements.txt
│
├── database/                 # Database scripts
│   ├── schema.sql           # Star schema DDL
│   ├── seed.sql             # Sample data
│   ├── migrate.js           # Migration script
│   └── backup.sh            # Backup script
│
├── data/                     # Sample datasets
│   ├── customers.csv
│   ├── products.csv
│   ├── transactions.csv
│   └── generate_sample_data.py
│
├── docs/                     # Documentation
│   ├── API.md               # API documentation
│   ├── DATABASE.md          # Database schema docs
│   └── DEPLOYMENT.md        # Deployment guide
│
├── docker-compose.yml        # Docker orchestration
├── Dockerfile               # Docker image
├── .env.example             # Environment variables template
└── README.md                # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** >= 18.0.0
- **Python** >= 3.9
- **PostgreSQL** >= 14
- **npm** or **yarn**
- **pip** (Python package manager)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/consumer360.git
cd consumer360
```

### 2. Setup Database

```bash
# Create PostgreSQL database
createdb consumer360_db

# Run schema migration
psql -d consumer360_db -f database/schema.sql

# Generate sample data
cd data
python generate_sample_data.py

# Load data into database (see database/README.md)
```

### 3. Setup Backend

```bash
cd backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Start backend server
npm run dev
```

Backend will run on `http://localhost:5000`

### 4. Setup Analytics Engine

```bash
cd analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run RFM analysis
python rfm_engine.py
```

### 5. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **PostgreSQL**: localhost:5432
- **pgAdmin**: http://localhost:5050

### Manual Docker Build

```bash
# Build backend image
docker build -t consumer360-backend ./backend

# Build frontend image
docker build -t consumer360-frontend ./frontend

# Run containers
docker run -d -p 5000:5000 consumer360-backend
docker run -d -p 3000:3000 consumer360-frontend
```

---

## 📊 Features

### 1. **Authentication & Authorization**
- JWT-based authentication
- Role-based access control (Admin, Analyst, Viewer)
- Secure password hashing with bcrypt
- Session management

### 2. **Dashboard**
- Real-time KPI cards (Revenue, Customers, Retention, AOV, LTV)
- Interactive Chart.js visualizations
- Revenue trend analysis
- Top products ranking
- Recent transactions feed

### 3. **RFM Segmentation**
- Automated RFM scoring (1-5 scale)
- 8 customer segments:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - New Customers
  - Promising
  - Hibernating
  - At Risk
  - Lost
- Segment-wise revenue contribution
- Marketing action recommendations

### 4. **Customer Analytics**
- Searchable customer profiles
- Purchase history tracking
- Spending pattern analysis
- Customer lifetime value calculation
- Churn prediction indicators

### 5. **Cohort Analysis**
- Monthly cohort grouping
- Retention heatmap visualization
- Month-over-month retention tracking
- Cohort performance comparison

### 6. **Market Basket Analysis**
- Apriori algorithm implementation
- Association rule mining
- Product affinity matrix
- Cross-sell recommendations
- Support, Confidence, Lift metrics

### 7. **Reports & Exports**
- PDF report generation
- CSV data exports
- Scheduled email reports
- Executive summaries
- Custom date range filtering

### 8. **Automation**
- Weekly RFM refresh (cron jobs)
- Automated data pipeline
- Scheduled analytics updates
- Email notifications

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/register      # Register new user
POST   /api/v1/auth/login         # Login
POST   /api/v1/auth/refresh       # Refresh token
POST   /api/v1/auth/logout        # Logout
```

### Dashboard
```
GET    /api/v1/dashboard/kpis              # Get KPIs
GET    /api/v1/dashboard/revenue-trend     # Revenue trend
GET    /api/v1/dashboard/top-products      # Top products
GET    /api/v1/dashboard/recent-transactions  # Recent orders
```

### Customers
```
GET    /api/v1/customers                   # List customers
GET    /api/v1/customers/:id               # Get customer
POST   /api/v1/customers                   # Create customer
PUT    /api/v1/customers/:id               # Update customer
DELETE /api/v1/customers/:id               # Delete customer
```

### RFM Analysis
```
GET    /api/v1/rfm/scores                  # Get RFM scores
GET    /api/v1/rfm/segments                # Get segments
POST   /api/v1/rfm/calculate               # Run RFM analysis
GET    /api/v1/rfm/segment/:name           # Get segment details
```

### Cohort Analysis
```
GET    /api/v1/cohort/retention            # Retention matrix
GET    /api/v1/cohort/trends               # Cohort trends
```

### Market Basket
```
GET    /api/v1/basket/rules                # Association rules
GET    /api/v1/basket/recommendations      # Product recommendations
```

### Reports
```
GET    /api/v1/reports/executive           # Executive summary
GET    /api/v1/reports/rfm                 # RFM report
GET    /api/v1/reports/cohort              # Cohort report
POST   /api/v1/reports/schedule            # Schedule report
```

Full API documentation: [docs/API.md](docs/API.md)

---

## 🗄️ Database Schema

### Star Schema Design

**Fact Table:**
- `fact_sales` - Transaction records

**Dimension Tables:**
- `dim_customer` - Customer information
- `dim_product` - Product catalog
- `dim_date` - Date dimension
- `dim_location` - Store locations

**Analytics Tables:**
- `rfm_scores` - RFM analysis results
- `customer_segments` - Segment definitions

See [database/schema.sql](database/schema.sql) for complete DDL.

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
npm test                    # Run all tests
npm run test:coverage       # With coverage report
```

### Frontend Tests
```bash
cd frontend
npm test                    # Run React tests
```

### Python Tests
```bash
cd analytics
pytest                      # Run analytics tests
pytest --cov               # With coverage
```

---

## 📈 Performance Optimization

- **Database Indexing**: Optimized indexes on fact and dimension tables
- **Query Optimization**: Materialized views for common queries
- **Caching**: Redis caching for frequently accessed data
- **API Rate Limiting**: Prevent abuse
- **Connection Pooling**: Efficient database connections
- **Lazy Loading**: Frontend component optimization

---

## 🔒 Security

- JWT authentication with refresh tokens
- Password hashing with bcrypt (10 rounds)
- SQL injection prevention (parameterized queries)
- XSS protection with Helmet.js
- CORS configuration
- Rate limiting
- Input validation with Joi
- Environment variable protection

---

## 📦 Dependencies

### Backend (Node.js)
- express - Web framework
- pg - PostgreSQL client
- jsonwebtoken - JWT auth
- bcryptjs - Password hashing
- helmet - Security headers
- cors - CORS middleware
- joi - Input validation
- winston - Logging

### Frontend (React)
- react - UI library
- axios - HTTP client
- chart.js - Data visualization
- react-router-dom - Routing
- tailwindcss - Styling

### Analytics (Python)
- pandas - Data manipulation
- numpy - Numerical computing
- psycopg2 - PostgreSQL adapter
- mlxtend - Apriori algorithm
- scikit-learn - ML utilities

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👥 Team

- **Rishi Dhali** – Team Lead
- Sm Musharraf Ashraf
- Adarsh J M
- Siddharth V

---

## 📞 Support

For issues and questions:
- 📧 Email: support@consumer360.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/consumer360/issues)
- 📖 Docs: [Documentation](https://docs.consumer360.com)

---

## 🎯 Roadmap

- [ ] Real-time analytics dashboard
- [ ] AI-powered churn prediction
- [ ] Revenue forecasting with ARIMA
- [ ] Customer sentiment analysis
- [ ] Mobile app (React Native)
- [ ] Advanced ML models
- [ ] Multi-tenant support
- [ ] GraphQL API

---

**Built with ❤️ by the Consumer360 Team**
