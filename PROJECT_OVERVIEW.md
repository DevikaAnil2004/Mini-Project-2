# CricketIQ - Project Overview

A comprehensive Indian Premier League (IPL) cricket analytics platform built with modern web technologies.

## Project Vision

CricketIQ is an all-in-one analytics platform for cricket enthusiasts, statisticians, and analysts to:
- Explore detailed team and player information
- Analyze match statistics and performance metrics
- Track player performance across seasons
- Gain actionable insights from cricket data

## Technology Stack

### Backend
- **Framework**: Flask 2.3.3 (Python micro web framework)
- **Database**: MySQL 8.0+ with SQLAlchemy ORM
- **Architecture**: MVC (Model-View-Controller) pattern
- **Database Migrations**: Flask-Migrate

### Frontend
- **CSS**: Custom OKLCH design-token system (`static/css/style.css`) layered on Bootstrap 5 for grid and reset
- **Markup**: HTML5 with Jinja2 templating; shared macros in `templates/_icons.html` and `templates/_components.html`
- **Icons**: Inline SVG symbol sprite, one stroke weight, no webfont
- **Charts**: Chart.js, themed from the CSS tokens and loaded per page
- **Interactivity**: Vanilla JavaScript (theme, drawer, toasts, table filter and sort)
- **Design system**: documented in `DESIGN.md`

### Development Tools
- **Package Manager**: pip (Python)
- **Virtual Environment**: Python venv
- **Version Control**: Git

## Project Structure

```
cricketiq/
├── Core Application Files
│   ├── app.py                  # Main Flask application (206 lines)
│   ├── models.py               # SQLAlchemy models (148 lines)
│   ├── config.py               # Configuration management (62 lines)
│   └── init_db.py              # Database initialization (312 lines)
│
├── Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                    # Environment variables
│   └── .gitignore              # Git ignore patterns
│
├── Frontend
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html           # Base template with navigation (106 lines)
│   │   ├── index.html          # Home page (163 lines)
│   │   ├── 404.html            # 404 error page (23 lines)
│   │   ├── 500.html            # 500 error page (23 lines)
│   │   ├── teams/
│   │   │   ├── index.html      # Teams listing (98 lines)
│   │   │   └── detail.html     # Team details (160 lines)
│   │   ├── players/
│   │   │   ├── index.html      # Players listing (127 lines)
│   │   │   └── detail.html     # Player details (205 lines)
│   │   └── matches/
│   │       ├── index.html      # Matches listing (160 lines)
│   │       └── detail.html     # Match details (239 lines)
│   │
│   └── static/                 # Static assets
│       ├── css/
│       │   └── style.css       # Custom styling (374 lines)
│       └── js/
│           └── main.js         # JavaScript utilities (228 lines)
│
└── Documentation
    ├── README.md               # Main documentation (337 lines)
    ├── QUICKSTART.md           # Quick start guide (136 lines)
    ├── DEPLOYMENT.md           # Production deployment guide (529 lines)
    ├── setup.sh                # Linux/Mac setup script (143 lines)
    └── setup.bat               # Windows setup script (97 lines)
```

## Database Schema

### 6 Main Tables

1. **teams** (8 fields)
   - Core IPL team information
   - Relationships: players, matches

2. **players** (11 fields)
   - Player profiles and details
   - Relationships: team, statistics

3. **matches** (14 fields)
   - Match information and results
   - Relationships: home_team, away_team, statistics

4. **batting_statistics** (9 fields)
   - Per-match batting performance
   - Links: player ↔ match

5. **bowling_statistics** (9 fields)
   - Per-match bowling performance
   - Links: player ↔ match

6. **team_statistics** (8 fields)
   - Season-wise team performance
   - Links: team, season data

## Key Features (Phase 1)

### Teams Module
✅ Browse all IPL teams (8 teams included)
✅ View team information (city, home ground, owner, coach)
✅ See team roster and player listings
✅ View season statistics and performance

### Players Module
✅ Browse 300+ IPL players
✅ Filter by role (Batsman, Bowler, All-rounder, Wicket-keeper)
✅ View player profiles and career statistics
✅ Track batting and bowling performance metrics

### Matches Module
✅ Explore all IPL matches
✅ Filter by season
✅ View match scorecards and results
✅ See match statistics (batting, bowling)

### Analytics
✅ Home page dashboard with key statistics
✅ Career statistics (runs, wickets, matches)
✅ Strike rates and economy rates
✅ Performance trends and metrics

### User Interface
✅ Responsive Bootstrap 5 design
✅ Mobile-friendly interface
✅ Intuitive navigation
✅ Professional styling

## Routes & Endpoints

```
GET /                    → Home page with dashboard
GET /teams              → All teams listing
GET /teams/<id>         → Team details page
GET /players            → All players listing
GET /players/<id>       → Player details page
GET /matches            → All matches listing
GET /matches/<id>       → Match details page
GET /api/stats          → Statistics API endpoint
```

## Development Workflow

### Local Development
1. Create virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` with MySQL credentials
4. Initialize database: `python init_db.py`
5. Run Flask: `python app.py`
6. Visit: `http://localhost:5000`

### Adding Features
- Database changes → models.py
- UI changes → templates/
- Styling → static/css/style.css
- JavaScript → static/js/main.js
- Routes → app.py

### Database Updates
```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

## Data Model

### Teams (8 included)
- Mumbai Indians
- Chennai Super Kings
- Royal Challengers Bangalore
- Delhi Capitals
- Kolkata Knight Riders
- Rajasthan Royals
- Punjab Kings
- Sunrisers Hyderabad

### Players (Sample: 9 included)
- Rohit Sharma, Virat Kohli, MS Dhoni, etc.
- Expandable to 300+ players
- Support for all player roles

### Matches (Sample: 3 included)
- Season information
- Home/Away teams
- Match results and scores
- Detailed statistics

## Performance Considerations

### Database
- Indexed queries on frequently accessed columns
- Pagination for large datasets
- Efficient relationships with SQLAlchemy

### Frontend
- Bootstrap CDN for faster loading
- Optimized CSS and JavaScript
- Responsive images and assets

### Caching
- Ready for Redis caching integration
- Static asset caching headers
- Database query optimization

## Security Features

- Environment variables for sensitive data
- Parameterized database queries (SQLAlchemy)
- CSRF protection via Flask
- XSS prevention with Jinja2 escaping
- Secret key configuration

## Scalability

### Horizontal Scaling
- Stateless Flask application
- Can run multiple instances with load balancer
- Database can be separated from app server

### Vertical Scaling
- Connection pooling for database
- Worker threads in Gunicorn
- Redis caching for frequently accessed data

### Database Optimization
- Query indexing
- Connection pooling
- Read replicas support

## Future Enhancements (Phases 2-8)

### Phase 2: Advanced Analytics
- Interactive dashboards
- Player comparison tools
- Performance trend analysis

### Phase 3: Predictions
- Match outcome predictions
- Player performance forecasting
- Injury prediction models

### Phase 4: User Features
- User authentication
- Personalized dashboards
- Favorite teams/players

### Phase 5: Real-time Updates
- Live match scoring
- Real-time statistics
- Push notifications

### Phase 6: APIs
- RESTful API
- GraphQL endpoint
- Mobile app support

### Phase 7: AI/ML
- Pattern recognition
- Anomaly detection
- Smart recommendations

### Phase 8: Advanced Features
- Social features
- Fantasy league integration
- Betting odds integration

## Development Guidelines

### Code Style
- PEP 8 for Python
- Semantic HTML5
- BEM CSS naming convention

### Database
- One model per table
- Foreign key relationships
- Cascade delete where appropriate

### Templates
- Template inheritance (base.html)
- DRY principle
- Consistent formatting

### Version Control
- Meaningful commit messages
- Feature branches
- Pull request reviews

## Testing

### Manual Testing
- Test all routes
- Test filters and pagination
- Test error pages
- Test responsive design

### Automated Testing (Recommended)
```bash
# Example test command
pytest tests/
```

## Deployment Options

1. **Local Development**: Flask dev server
2. **Production Server**: Gunicorn + Nginx
3. **Docker**: Containerized deployment
4. **Cloud Services**: Heroku, AWS, Google Cloud, Azure

See DEPLOYMENT.md for detailed instructions.

## File Statistics

- **Total Python Files**: 4 (app.py, models.py, config.py, init_db.py)
- **Total Templates**: 10 HTML files
- **Total CSS**: 1 file (374 lines)
- **Total JavaScript**: 1 file (228 lines)
- **Total Documentation**: 4 markdown files
- **Total Setup Scripts**: 2 (bash + batch)

## Key Metrics

- **Lines of Code (Backend)**: ~730 lines
- **Lines of Code (Templates)**: ~1,300 lines
- **Lines of Code (Styling)**: 374 lines
- **Lines of Code (JavaScript)**: 228 lines
- **Database Tables**: 6
- **Routes**: 9
- **Templates**: 10

## Getting Started

### Quickest Start
```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat

# Manual
pip install -r requirements.txt
python init_db.py
python app.py
```

### Detailed Setup
See QUICKSTART.md for step-by-step instructions.

### Production Deployment
See DEPLOYMENT.md for comprehensive guide.

## Support & Documentation

- **README.md**: Complete feature documentation
- **QUICKSTART.md**: Fast setup in 5 minutes
- **DEPLOYMENT.md**: Production deployment guide
- **CODE COMMENTS**: Inline documentation throughout

## License

Open source - available for educational and commercial use.

## Author Notes

CricketIQ is built with:
- Modern web development practices
- Clean, readable code
- Comprehensive documentation
- Production-ready architecture
- Scalable design patterns
- Easy customization and extension

Built with Flask, MySQL, Bootstrap 5, and modern web standards.

---

**Ready to get started?** See QUICKSTART.md for local setup instructions.
