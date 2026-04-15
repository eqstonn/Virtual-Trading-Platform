# Virtual Trading Platform

A web application that allows users to practice stock trading in a risk-free virtual environment. Track your portfolio, execute trades, and monitor your performance with real-time market data.

## Features

**User Authentication** - Secure sign up and login using Supabase Auth
**Live Trading Dashboard** - Real-time stock charts and trading interface
**Portfolio Management** - Track holdings, average prices, and performance
**Buy & Sell Stocks** - Execute trades with automatic balance calculations
**Cash Balance Tracking** - Monitor your available funds and trading history
**Trading Activity Log** - View complete transaction history
**Modern UI** - Clean, responsive design with dark theme

## Tech Stack

### Backend
- **Python 3** with **FastAPI** - High-performance REST API
- **Supabase** - PostgreSQL database with built-in authentication
- **SQLAlchemy ORM** - Database operations and migrations
- **Pydantic** - Data validation for API requests

### Frontend
- **React 18** - Component-based UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Chart library for data visualization
- **Lucide React** - Modern icon library

### Database
- **PostgreSQL** (via Supabase)
- Tables: users, profiles, holdings, transactions

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Supabase account

### Backend Setup

1. Clone the repository
```bash
git clone <repository-url>
cd Virtual\ Trading\ Platform
```

2. Create a Python virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### Frontend Setup

1. Navigate to the frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Update the API base URL in your components if needed
```javascript
// Default: http://localhost:8000
```

## Running the Application

### Run Both Frontend & Backend Concurrently
```bash
npm run dev
```
This will start:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sign_up` | Create a new user account |
| POST | `/login` | Authenticate user |
| GET | `/session` | Get current session info |
| POST | `/signout` | Logout user |
| GET | `/profile/{user_id}` | Get user profile & balance |

## Project Structure

```
Virtual Trading Platform/
├── backend/
│   ├── app_api.py              # FastAPI application & routes
│   ├── auth_service.py         # Authentication logic
│   ├── database_service.py     # Database operations
│   ├── trading_service.py      # Buy/sell logic
│   ├── market_data.py          # Market data handling
│   └── main.py                 # Test/demo script
├── frontend/
│   ├── src/
│   │   ├── TradingDashboard.jsx   # Main dashboard component
│   │   ├── HomePage.jsx           # Landing page
│   │   ├── LoginModal.jsx         # Login form
│   │   ├── SignUpModal.jsx        # Sign up form
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Tailwind styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── requirements.txt            # Python dependencies
├── package.json                # NPM root scripts
└── README.md                   # This file
```

## How It Works

### Trading Flow
1. User signs up or logs in with email/password
2. System creates user profile with $10,000 starting balance
3. User searches for stocks in the trading dashboard
4. User can buy or sell stocks
5. System calculates new average price for holdings
6. Cash balance is updated after each trade
7. Portfolio displays current holdings and performance

### Data Validation
- All API requests validated using Pydantic models
- CORS enabled for frontend communication
- User session managed via Supabase Auth

## Environment Variables

Create a `.env` file in the root directory:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_public_key
```

## Future Enhancements

- [ ] Advanced charting with technical indicators
- [ ] Leaderboard and social features
- [ ] Mobile-responsive optimization
- [ ] Trade alerts and notifications
- [ ] Export trading history to CSV
