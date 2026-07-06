# CricketIQ Setup Checklist

Use this checklist to ensure proper setup of the CricketIQ application.

## Pre-Setup Requirements

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] MySQL Server installed and running
- [ ] pip available (`pip --version`)
- [ ] Git installed (optional, for version control)
- [ ] Text editor or IDE (VS Code, PyCharm, etc.)
- [ ] Terminal/Command Prompt access

## Setup Steps

### 1. Initial Setup

- [ ] Download/clone CricketIQ project
- [ ] Navigate to project directory: `cd cricketiq`
- [ ] Verify project structure (check all folders exist)
- [ ] Read QUICKSTART.md for overview

### 2. Virtual Environment

- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate virtual environment:
  - [ ] Linux/Mac: `source venv/bin/activate`
  - [ ] Windows: `venv\Scripts\activate`
- [ ] Verify activation (should show `(venv)` in prompt)

### 3. Dependencies Installation

- [ ] Run: `pip install -r requirements.txt`
- [ ] Wait for installation to complete
- [ ] Verify Flask installed: `pip list | grep Flask`
- [ ] Verify SQLAlchemy installed: `pip list | grep SQLAlchemy`

### 4. MySQL Configuration

#### Option A: No Password (Default)
- [ ] Start MySQL Server
- [ ] Open MySQL Command Line
- [ ] Run: `CREATE DATABASE cricketiq;`
- [ ] Verify database created: `SHOW DATABASES;`
- [ ] .env MYSQL_PASSWORD should be empty

#### Option B: With Password
- [ ] Start MySQL Server
- [ ] Open MySQL Command Line
- [ ] Create user: `CREATE USER 'cricketiq'@'localhost' IDENTIFIED BY 'password';`
- [ ] Grant privileges: `GRANT ALL PRIVILEGES ON cricketiq.* TO 'cricketiq'@'localhost';`
- [ ] Create database: `CREATE DATABASE cricketiq;`
- [ ] Flush privileges: `FLUSH PRIVILEGES;`
- [ ] Update .env with credentials

### 5. Environment Configuration

- [ ] Open .env file in text editor
- [ ] Update MYSQL_HOST (default: localhost)
- [ ] Update MYSQL_USER (default: root)
- [ ] Update MYSQL_PASSWORD (your MySQL password)
- [ ] Update MYSQL_PORT (default: 3306)
- [ ] Update MYSQL_DATABASE (default: cricketiq)
- [ ] Generate SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Update SECRET_KEY in .env

### 6. Database Initialization

- [ ] Verify virtual environment is activated
- [ ] Run: `python init_db.py`
- [ ] Should see output:
  - [ ] `[v0] Creating database tables...`
  - [ ] `[v0] Database tables created successfully!`
  - [ ] `[v0] Added 8 teams`
  - [ ] `[v0] Added 9 players`
  - [ ] `[v0] Added 3 matches`
  - [ ] `[v0] Added team statistics`
  - [ ] `[v0] Database initialization completed successfully!`

### 7. Application Startup

- [ ] Run: `python app.py`
- [ ] Should see output:
  - [ ] `[v0] Creating database tables...`
  - [ ] `[v0] Database tables created successfully!`
  - [ ] `[v0] Starting Flask development server...`
  - [ ] `Running on http://0.0.0.0:5000`

### 8. Browser Access

- [ ] Open web browser
- [ ] Navigate to: `http://localhost:5000`
- [ ] Page should load (not error page)
- [ ] See navigation bar with:
  - [ ] CricketIQ logo
  - [ ] Home link
  - [ ] Teams link
  - [ ] Players link
  - [ ] Matches link

## Feature Verification

### Home Page (/
- [ ] Statistics display (Teams, Players, Matches count)
- [ ] Latest matches table visible
- [ ] Feature cards display
- [ ] CTA buttons work

### Teams Page (/teams)
- [ ] 8 teams display in grid
- [ ] Team cards show:
  - [ ] Team name
  - [ ] Short name
  - [ ] City
  - [ ] Home ground
  - [ ] Player count
  - [ ] "View Details" button
- [ ] Pagination works (if applicable)

### Team Detail Page
- [ ] Team information displays
- [ ] Players list shows
- [ ] Statistics display
- [ ] Back button works

### Players Page (/players)
- [ ] Players list displays
- [ ] Role filter works
- [ ] Can filter by role
- [ ] Players show:
  - [ ] Name
  - [ ] Team
  - [ ] Role
  - [ ] Batting/Bowling style
- [ ] Pagination works

### Player Detail Page
- [ ] Player information displays
- [ ] Career statistics show
- [ ] Batting statistics table appears
- [ ] Bowling statistics table appears
- [ ] Links to team page work

### Matches Page (/matches)
- [ ] Matches list displays
- [ ] Season filter works
- [ ] Matches show:
  - [ ] Date
  - [ ] Teams
  - [ ] Venue
  - [ ] Score
  - [ ] Status badge
- [ ] Pagination works

### Match Detail Page
- [ ] Match information displays
- [ ] Score shows
- [ ] Winner displays
- [ ] Batting statistics table visible
- [ ] Bowling statistics table visible
- [ ] Player links work

## Responsive Design Check

### Mobile (320px width)
- [ ] Navigation toggles to hamburger menu
- [ ] Content is readable
- [ ] Tables are responsive
- [ ] Buttons are clickable

### Tablet (768px width)
- [ ] Layout adapts
- [ ] Navigation visible
- [ ] Grid adjusts columns
- [ ] Tables readable

### Desktop (1200px width)
- [ ] Full layout displays
- [ ] All features visible
- [ ] Tables fully displayed
- [ ] Optimal spacing

## API Endpoints Check

- [ ] `GET /` - Home page (200 OK)
- [ ] `GET /teams` - Teams listing (200 OK)
- [ ] `GET /teams/1` - Team detail (200 OK)
- [ ] `GET /players` - Players listing (200 OK)
- [ ] `GET /players/1` - Player detail (200 OK)
- [ ] `GET /matches` - Matches listing (200 OK)
- [ ] `GET /matches/1` - Match detail (200 OK)
- [ ] `GET /api/stats` - Stats API (200 OK, JSON response)
- [ ] Invalid route - 404 page displays

## Database Verification

### In MySQL Terminal
```sql
- [ ] USE cricketiq;
- [ ] SHOW TABLES; (should show 6 tables)
- [ ] SELECT COUNT(*) FROM teams; (should be 8)
- [ ] SELECT COUNT(*) FROM players; (should be 9+)
- [ ] SELECT COUNT(*) FROM matches; (should be 3+)
```

## Console Check

- [ ] No JavaScript errors in browser console
- [ ] No Python errors in terminal
- [ ] No SQL errors in logs
- [ ] Request logs showing (GET requests)

## File Structure Verification

```
cricketiq/
├── app.py                  [ ] Exists (206 lines)
├── models.py               [ ] Exists (148 lines)
├── config.py               [ ] Exists (62 lines)
├── init_db.py              [ ] Exists (312 lines)
├── requirements.txt        [ ] Exists
├── .env                    [ ] Exists
├── .gitignore              [ ] Exists
├── README.md               [ ] Exists
├── QUICKSTART.md           [ ] Exists
├── DEPLOYMENT.md           [ ] Exists
├── PROJECT_OVERVIEW.md     [ ] Exists
├── setup.sh                [ ] Exists
├── setup.bat               [ ] Exists
├── templates/              [ ] Directory exists
│   ├── base.html           [ ] Exists
│   ├── index.html          [ ] Exists
│   ├── 404.html            [ ] Exists
│   ├── 500.html            [ ] Exists
│   ├── teams/              [ ] Directory exists
│   │   ├── index.html      [ ] Exists
│   │   └── detail.html     [ ] Exists
│   ├── players/            [ ] Directory exists
│   │   ├── index.html      [ ] Exists
│   │   └── detail.html     [ ] Exists
│   └── matches/            [ ] Directory exists
│       ├── index.html      [ ] Exists
│       └── detail.html     [ ] Exists
└── static/                 [ ] Directory exists
    ├── css/                [ ] Directory exists
    │   └── style.css       [ ] Exists (374 lines)
    └── js/                 [ ] Directory exists
        └── main.js         [ ] Exists (228 lines)
```

## Common Issues & Fixes

### Issue: ModuleNotFoundError: No module named 'flask'
- [ ] Activate virtual environment
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify Flask: `pip list | grep Flask`

### Issue: Access denied for user 'root'@'localhost'
- [ ] Check MYSQL_PASSWORD in .env
- [ ] Verify MySQL user and password
- [ ] Test MySQL connection manually

### Issue: Unknown database 'cricketiq'
- [ ] Create database: `CREATE DATABASE cricketiq;`
- [ ] Verify database exists: `SHOW DATABASES;`
- [ ] Run: `python init_db.py`

### Issue: Port 5000 already in use
- [ ] Find process: `lsof -ti:5000`
- [ ] Kill process: `kill -9 <PID>`
- [ ] Or change port in app.py line 213

### Issue: Templates not loading
- [ ] Check templates/ directory exists
- [ ] Verify file paths in app.py
- [ ] Check template syntax in HTML files

## Post-Setup Tasks

### Development
- [ ] Add more sample data in init_db.py
- [ ] Customize colors in static/css/style.css
- [ ] Modify templates in templates/
- [ ] Add new routes in app.py
- [ ] Extend models in models.py

### Git Setup (Optional)
- [ ] Initialize git: `git init`
- [ ] Add files: `git add .`
- [ ] Initial commit: `git commit -m "Initial CricketIQ setup"`
- [ ] Create .gitignore entries for:
  - [ ] venv/
  - [ ] __pycache__/
  - [ ] .env
  - [ ] *.db

### Production Preparation
- [ ] Review DEPLOYMENT.md
- [ ] Set up Gunicorn
- [ ] Configure Nginx
- [ ] Setup SSL certificate
- [ ] Configure firewall
- [ ] Setup monitoring

## Documentation Review

- [ ] Read README.md (complete guide)
- [ ] Read QUICKSTART.md (reference)
- [ ] Read DEPLOYMENT.md (for production)
- [ ] Read PROJECT_OVERVIEW.md (architecture)
- [ ] Review code comments in:
  - [ ] app.py
  - [ ] models.py
  - [ ] config.py

## Testing Checklist

### Manual Testing
- [ ] Navigate all pages
- [ ] Test all filters
- [ ] Test pagination
- [ ] Click all links
- [ ] Test error pages (404, 500)
- [ ] Test responsive design
- [ ] Test with different browsers

### Data Testing
- [ ] Verify sample data loads
- [ ] Check team-player relationships
- [ ] Verify statistics display
- [ ] Check match details
- [ ] Verify player statistics

## Performance Check

- [ ] Page load time reasonable (< 2 seconds)
- [ ] No SQL errors in logs
- [ ] Memory usage normal
- [ ] CPU usage low during idle
- [ ] Database queries efficient

## Security Check

- [ ] .env not committed to git
- [ ] SECRET_KEY is unique
- [ ] No hardcoded passwords
- [ ] Error messages don't expose internals
- [ ] SQL queries use parameters (SQLAlchemy handles this)

## Final Verification

- [ ] All checklist items completed
- [ ] All pages load without errors
- [ ] Sample data displays correctly
- [ ] Database connection working
- [ ] No warnings in console
- [ ] Ready for development

## Ready to Deploy?

If all items checked:
- [ ] Review DEPLOYMENT.md
- [ ] Set up production environment
- [ ] Configure server
- [ ] Setup database
- [ ] Deploy application

---

## Sign-Off

Setup Date: _______________
Verified By: _______________
Status: [ ] Complete [ ] Issues Found

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Congratulations!** Your CricketIQ setup is complete and verified.

Next Steps:
1. Start developing and customizing
2. Add more data as needed
3. Deploy to production when ready
4. Monitor performance
5. Gather user feedback

For help, see README.md or contact support.
