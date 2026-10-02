# CricketIQ - IPL Analytics Platform

A comprehensive Indian Premier League (IPL) cricket analytics platform built with Flask and MySQL. Explore team statistics, player performance, match details, and cricket insights with an interactive web interface.

## Features

- **Team Management**: Browse all IPL teams with detailed information
- **Player Profiles**: View player statistics, career data, and performance metrics
- **Match Analytics**: Access detailed match information, scorecards, and statistics
- **Batting Statistics**: Track runs, strike rates, dismissals, and individual performance
- **Bowling Statistics**: Monitor wickets, economy rates, and bowling performance
- **Season Statistics**: View team performance across IPL seasons
- **Responsive Design**: Sidebar shell on desktop, drawer navigation on mobile, dark and light themes
- **Search & Filter**: Server-side role and season filters, plus instant client-side filtering and column sorting on every table

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL with SQLAlchemy ORM (SQLite in development)
- **Frontend**: Jinja2 templates, a custom OKLCH design-token CSS layer on top of Bootstrap 5 grid/reset, vanilla JavaScript
- **Icons**: Inline SVG sprite (`templates/_icons.html`) — no icon webfont
- **Charts**: Chart.js, loaded only on the pages that render charts
- **Database Migrations**: Flask-Migrate

See [DESIGN.md](DESIGN.md) for the design system: tokens, components and the rules the interface follows.

## Project Structure

```
cricketiq/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── main.js            # JavaScript functionality
└── templates/
    ├── base.html              # Base template with navigation
    ├── index.html             # Home page
    ├── 404.html               # 404 error page
    ├── 500.html               # 500 error page
    ├── teams/
    │   ├── index.html         # Teams listing
    │   └── detail.html        # Team details
    ├── players/
    │   ├── index.html         # Players listing
    │   └── detail.html        # Player details
    └── matches/
        ├── index.html         # Matches listing
        └── detail.html        # Match details
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL Server (8.0+)
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download the Project

```bash
cd cricketiq
```

### Step 2: Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

#### Option A: Using Local MySQL (Recommended)

1. **Start MySQL Server**:
   - On macOS with Homebrew: `brew services start mysql`
   - On Windows: Start MySQL from Services or MySQL Command Line Client
   - On Linux: `sudo systemctl start mysql`

2. **Create Database**:
   ```sql
   mysql -u root -p
   
   CREATE DATABASE cricketiq;
   EXIT;
   ```

3. **Update .env file**:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_DEBUG=True
   
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_PORT=3306
   MYSQL_DATABASE=cricketiq
   
   SECRET_KEY=your-secret-key-change-this-in-production
   ```

#### Option B: No Password MySQL
If your MySQL doesn't have a password:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_PORT=3306
MYSQL_DATABASE=cricketiq
```

### Step 5: Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Add 8 sample IPL teams
- Add sample players
- Add sample matches
- Add team statistics

### Step 6: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Home Page
Visit the home page to see:
- Overall statistics (total teams, players, matches)
- Latest matches
- Quick navigation links

### Teams
- Browse all IPL teams
- View team information (city, home ground, owner, coach)
- See team players
- View season statistics

### Players
- Browse all active players
- Filter by role (Batsman, Bowler, All-rounder, Wicket-keeper)
- View player details and career statistics
- Check batting and bowling performance

### Matches
- Browse all matches
- Filter by season
- View match details and scorecards
- See batting and bowling statistics

## Database Schema

### Tables

1. **teams**: IPL team information
2. **players**: Player profiles and details
3. **matches**: Match information and results
4. **batting_statistics**: Player batting performance
5. **bowling_statistics**: Player bowling performance
6. **team_statistics**: Team season statistics

## API Endpoints

- `GET /` - Home page
- `GET /teams` - Teams listing
- `GET /teams/<id>` - Team details
- `GET /players` - Players listing
- `GET /players/<id>` - Player details
- `GET /matches` - Matches listing
- `GET /matches/<id>` - Match details
- `GET /api/stats` - Statistics API endpoint

## Configuration

### Environment Variables

Edit `.env` file to configure:

- `FLASK_ENV`: Set to 'development' or 'production'
- `FLASK_DEBUG`: Enable/disable debug mode
- `MYSQL_*`: Database connection settings
- `SECRET_KEY`: Flask secret key for sessions

### Adding More Sample Data

Edit `init_db.py` to add more:
- Teams
- Players
- Matches
- Statistics

Then run: `python init_db.py`

## Development

### Running in Debug Mode
The application runs in debug mode by default during development:
- Hot-reload on file changes
- Interactive debugger
- Detailed error pages

### Database Migrations
For schema changes, use Flask-Migrate:

```bash
flask db init
flask db migrate -m "Description"
flask db upgrade
```

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running
- Check MYSQL_USER and MYSQL_PASSWORD in .env
- Verify MYSQL_DATABASE exists

### Table Already Exists Error
- Database already initialized
- To reset: `DROP DATABASE cricketiq;` then run `init_db.py`

### Port 5000 Already in Use
Change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found
Ensure virtual environment is activated and all dependencies installed:
```bash
pip install -r requirements.txt
```

## File Descriptions

### Core Files
- **app.py**: Main Flask application with all routes and error handlers
- **models.py**: SQLAlchemy ORM models for database tables
- **config.py**: Configuration classes for different environments
- **init_db.py**: Script to initialize database with sample data

### Templates
- **base.html**: Base template with navigation and footer
- **index.html**: Home page with statistics and latest matches
- **teams/**: Team listing and detail pages
- **players/**: Player listing and detail pages
- **matches/**: Match listing and detail pages

### Static Files
- **static/css/style.css**: Custom styling and responsive design
- **static/js/main.js**: JavaScript utilities and interactions

## Features Overview

### Phase 1 (Current)
- ✅ Project structure and setup
- ✅ Database schema with 6 tables
- ✅ Flask app factory pattern
- ✅ SQLAlchemy ORM models
- ✅ Bootstrap 5 responsive UI
- ✅ Team management pages
- ✅ Player management pages
- ✅ Match listing and details
- ✅ Statistics display
- ✅ Search and filtering

### Phase 2 (Planned)
- Analytics dashboard
- Advanced statistics
- Player performance trends
- Team comparison

### Phase 3 (Planned)
- Predictions and forecasting
- Live match updates
- User authentication
- Personalized dashboards

## License

This project is open source and available for educational and commercial use.

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Flask and SQLAlchemy documentation

## Quick Start Command

After installation, start the app with:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the application
python app.py
```

Then open your browser and go to: **http://localhost:5000**

---

**CricketIQ v1.0** - Built with Flask, MySQL, and Bootstrap 5
