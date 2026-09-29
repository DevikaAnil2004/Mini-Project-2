# CricketIQ — Complete Project Explanation & System Architecture

CricketIQ is an end-to-end Indian Premier League (IPL) data analytics, exploration, and intelligence platform. It ingests official ball-by-ball IPL records from **2008 through the present**, maintains an optimized relational database of teams, players, matches, scorecards, and standings, provides dedicated player profile analysis with career milestones, and powers predictive machine learning models.

---

## 1. System Architecture Overview

The system follows a clean **Model-View-Controller (MVC)** and tiered service-oriented architecture:

```mermaid
graph TD
    User([End User / Web Browser])

    subgraph Presentation_Layer ["Presentation Layer (Frontend)"]
        UI["Jinja2 Templates (HTML5)"]
        CSS["Design System (CSS Tokens + Glassmorphism)"]
        ClientJS["Interactive JS (Async Fetch, Filters, Charts)"]
    end

    subgraph Application_Layer ["Application & Controller Layer (Flask 3.x)"]
        AppRoutes["Flask HTTP Routing (app.py)"]
        GlobalContext["Global Processors & Error Handlers"]
    end

    subgraph Intelligence_Layer ["Intelligence & Machine Learning Engine"]
        MatchPredictor["Match Outcome Predictor (Random Forest Classifier)"]
        PlayerForecaster["Player Performance Forecaster (Random Forest Regressor)"]
        PlayerSimilarity["Playing Style Clustering (K-Means & StandardScaler)"]
        TeamAssistant["Smart Playing XI Assistant (Role & Balance Heuristics)"]
        CachedLoaders["Thread-safe LRU Model/Dataset Loader"]
    end

    subgraph Data_Layer ["Data & Persistence Layer"]
        ORM["SQLAlchemy ORM (models.py)"]
        SQLiteDB[(SQLite Database - cricketiq.db)]
        DataCSVs["Analytical Series & Registry Datasets (.csv)"]
    end

    User <--> Presentation_Layer
    Presentation_Layer <--> Application_Layer
    Application_Layer <--> Intelligence_Layer
    Application_Layer <--> Data_Layer
    Intelligence_Layer <--> Data_Layer
```

---

## 2. Complete Historical Data Pipeline (2008 – Present)

CricketIQ features an automated ingestion engine ([`scripts/build_comprehensive_ipl_db.py`](file:///d:/CricketIQ/scripts/build_comprehensive_ipl_db.py)) that downloads, cross-references, validates, and populates ball-by-ball data across all IPL seasons:

```mermaid
flowchart LR
    subgraph Sources ["External Data Sources"]
        CricsheetZip["Cricsheet IPL Ball-by-Ball JSON (1,243 fixtures)"]
        PeopleReg["People Identifier Register (people.csv)"]
        NamesReg["Name Variations Register (names.csv)"]
    end

    subgraph Pipeline ["Ingestion & Transformation Engine"]
        Parser["Ball-by-Ball Extractor & Match Replayer"]
        EntityResolver["Entity Disambiguation & Alias Matcher"]
        Aggregator["Career Stats, Overs & Milestone Aggregator"]
        StandingsEngine["Season Standings & Points Calculator"]
    end

    subgraph Destination ["Populated Database & Model Store"]
        DB[(cricketiq.db)]
        MLDatasets["Feature Datasets (.csv)"]
        TrainedModels["Trained Models (.joblib)"]
    end

    CricsheetZip --> Parser
    PeopleReg --> EntityResolver
    NamesReg --> EntityResolver
    Parser --> EntityResolver
    EntityResolver --> Aggregator
    Parser --> StandingsEngine
    Aggregator --> DB
    StandingsEngine --> DB
    Aggregator --> MLDatasets
    MLDatasets --> TrainedModels
```

### Ingestion Metrics Summary
- **Seasons Covered**: All 18 IPL seasons (2008 Inaugural match through 2026 season)
- **Matches Ingested**: 1,243 matches
- **Active & Historical Franchises**: 15 teams
- **Squad Players Logged**: 809 cricketers
- **Batting Innings**: 18,842 innings
- **Bowling Spells**: 14,734 spells
- **Career Runs Tracked**: 381,529 runs
- **Career Wickets Tracked**: 13,482 wickets

---

## 3. Database Entity Relationship (ER) Diagram

The relational schema is defined via SQLAlchemy in [`models.py`](file:///d:/CricketIQ/models.py) and enforced in SQLite with relational foreign keys and indexes:

```mermaid
erDiagram
    TEAMS ||--o{ PLAYERS : "has members"
    TEAMS ||--o{ MATCHES : "hosts as home_team"
    TEAMS ||--o{ MATCHES : "visits as away_team"
    TEAMS ||--o{ MATCHES : "wins match"
    TEAMS ||--o{ MATCHES : "wins toss"
    TEAMS ||--o{ TEAM_STATISTICS : "has season record"

    PLAYERS ||--o{ BATTING_STATISTICS : "records innings"
    PLAYERS ||--o{ BOWLING_STATISTICS : "records bowling spell"

    MATCHES ||--o{ BATTING_STATISTICS : "contains innings"
    MATCHES ||--o{ BOWLING_STATISTICS : "contains bowling spells"

    TEAMS {
        int id PK
        string name UK
        string short_name UK
        string city
        string home_ground
        int founded_year
        string owner
        string coach
        datetime created_at
        datetime updated_at
    }

    PLAYERS {
        int id PK
        string name
        int jersey_number
        string role
        string batting_style
        string bowling_style
        date date_of_birth
        string country
        int team_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    MATCHES {
        int id PK
        int season
        int match_number
        int home_team_id FK
        int away_team_id FK
        datetime match_date
        string venue
        string status
        int home_team_score
        int away_team_score
        int winner_id FK
        string man_of_the_match
        int toss_winner_id FK
        string toss_decision
        datetime created_at
        datetime updated_at
    }

    BATTING_STATISTICS {
        int id PK
        int player_id FK
        int match_id FK
        int runs
        int balls_faced
        int fours
        int sixes
        float strike_rate
        string dismissal_type
        datetime created_at
        datetime updated_at
    }

    BOWLING_STATISTICS {
        int id PK
        int player_id FK
        int match_id FK
        float overs
        int maidens
        int runs_conceded
        int wickets
        float economy_rate
        int dot_balls
        datetime created_at
        datetime updated_at
    }

    TEAM_STATISTICS {
        int id PK
        int team_id FK
        int season
        int matches_played
        int wins
        int losses
        int position
        int points
        float run_rate
        datetime created_at
        datetime updated_at
    }
```

---

## 4. Dedicated Player Profile Architecture

Every player in the database has a dedicated profile accessible at `/players/<player_id>` (e.g. [`/players/571`](http://127.0.0.1:5000/players/571) for Virat Kohli):

```mermaid
graph TD
    Req["Request: GET /players/&lt;id&gt;"] --> DBQuery["Query Player + Eagerly Join Team"]
    DBQuery --> QueryStats["Fetch BattingStatistic & BowlingStatistic Records"]
    QueryStats --> AggCalc["Calculate Dynamic Career Metrics"]

    subgraph Metrics_Computed ["Computed Career Totals & Milestones"]
        M1["Total Runs, Balls Faced, Strike Rate"]
        M2["Batting Average (Runs / Non-Not-Out Dismissals)"]
        M3["Centuries (100s) & Half-Centuries (50s)"]
        M4["Boundaries Count (4s and 6s)"]
        M5["Total Wickets, Best Bowling Figures (e.g. 5/12)"]
        M6["Overs Bowled & Career Economy Rate"]
        M7["4-Wicket & 5-Wicket Hauls, Dot Balls Bowled"]
    end

    AggCalc --> Metrics_Computed
    Metrics_Computed --> Render["Render templates/players/detail.html"]
    Render --> UIOutput["Interactive Profile Page with Match-by-Match Log"]
```

---

## 5. Intelligence & Machine Learning Subsystems

CricketIQ integrates three machine learning models and one rule-based optimization engine in the [`lib/`](file:///d:/CricketIQ/lib/) directory:

```mermaid
graph LR
    subgraph Subsystems ["Intelligence Features"]
        subgraph Sub1 ["1. Match Predictor"]
            MInput["Inputs: Team 1, Team 2, Venue, Toss"] --> RFC["Random Forest Classifier (100 Trees)"]
            RFC --> MProb["Win Probability & Contextual Factors"]
        end

        subgraph Sub2 ["2. Run Forecaster"]
            FInput["Input: Player ID + Lag 1-3 Innings"] --> RFR["Random Forest Regressor (50 Trees)"]
            RFR --> FRuns["Projected Runs for Next Match"]
        end

        subgraph Sub3 ["3. Similarity Engine"]
            SInput["Input: Player Stats Vector (Avg, SR, Wkts, Econ)"] --> Scaler["StandardScaler"]
            Scaler --> KM["K-Means Clustering (k=8)"]
            KM --> Peers["Top 5 Statistical Peers"]
        end

        subgraph Sub4 ["4. XI Assistant"]
            AInput["Input: Team Squad + Opposition"] --> Balancer["Role Optimization Heuristic"]
            Balancer --> XI["Balanced 11 (5 Bat, 1 Wk, 2 AR, 3 Bowl)"]
        end
    end
```

---

## 6. End-to-End User Interaction Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Analyst
    participant Browser as Web Browser
    participant Flask as Flask Server (app.py)
    participant ML as ML & Assistant Engine
    participant DB as SQLite Database

    User->>Browser: Open http://127.0.0.1:5000
    Browser->>Flask: GET /
    Flask->>DB: Query Dashboard Overview Stats
    DB-->>Flask: Total Teams (15), Players (809), Matches (1,243)
    Flask-->>Browser: Render Overview Dashboard

    User->>Browser: Search Player "Kohli" with filter
    Browser->>Flask: GET /players?q=Kohli
    Flask->>DB: Query Player with name ILIKE '%Kohli%'
    DB-->>Flask: Filtered records (e.g. Virat Kohli #571)
    Flask-->>Browser: Display Paginated Search Results

    User->>Browser: Click on "View Profile"
    Browser->>Flask: GET /players/571
    Flask->>DB: Fetch Career Innings (277 bat, 26 bowl)
    DB-->>Flask: Raw scorecards
    Flask-->>Browser: Render Profile: 9,346 runs, 9x 100s, 68x 50s, SR 131.14

    User->>Browser: Run Simulation (e.g. MI vs CSK)
    Browser->>Flask: GET /api/predict/match?team1=1&team2=2
    Flask->>ML: MatchPredictor.predict(team1=1, team2=2)
    ML-->>Flask: Probability split (e.g. 66.5% vs 33.5%)
    Flask-->>Browser: JSON response
    Browser-->>User: Dynamic animated outcome bars
```

---

## 7. Directory Structure & File Map

```
CricketIQ/
├── app.py                      # Flask routes, API endpoints, error handlers
├── config.py                   # Environment, SQLite, and MySQL configs
├── models.py                   # SQLAlchemy schema (6 core tables)
├── requirements.txt            # Python dependencies
│
├── data/
│   ├── historical_matches.csv  # 1,218 feature rows for match predictor
│   ├── player_stats.csv        # 809 player stat vectors for clustering
│   ├── player_performance_series.csv # 18,842 chronological innings for forecasting
│   ├── people.csv              # Official Cricsheet people identifiers
│   └── names.csv               # Official Cricsheet alternate names
│
├── instance/
│   └── cricketiq.db            # Complete SQLite relational database
│
├── lib/
│   ├── loaders.py              # Thread-safe LRU caching loaders
│   ├── ml_models.py            # Model training classes (RFC, RFR, KMeans)
│   ├── predictor.py            # MatchPredictor & PlayerForecaster runtime classes
│   ├── similarity.py           # PlayerSimilarity clustering lookup
│   └── assistant.py            # TeamAssistant Playing XI heuristic
│
├── models/                     # Serialized scikit-learn artifacts (.joblib)
│   ├── match_predictor.joblib
│   ├── player_forecaster.joblib
│   ├── player_clustering.joblib
│   └── player_scaler.joblib
│
├── scripts/
│   ├── build_comprehensive_ipl_db.py  # Complete scraping, parsing, DB & ML pipeline
│   ├── generate_dataset.py            # Synthetic dataset generator fallback
│   └── real_players_data.py           # Enriched squad attributes mapping
│
├── static/
│   ├── css/style.css           # Premium token-based design system
│   └── js/                     # Modular frontend logic
│       ├── main.js             # Theme toggle, drawer, tables
│       ├── analytics.js        # Chart.js visualization logic
│       ├── intelligence.js     # XI Assistant & Similarity client
│       └── predictions.js      # Match and Forecaster client
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Shared layout, icons, navigation
│   ├── index.html              # Dashboard home page
│   ├── analytics/index.html    # Season performance charts
│   ├── intelligence/           # Assistant & Similarity views
│   ├── matches/                # Match lists & scorecards
│   ├── players/                # Directory & dedicated profiles
│   └── teams/                  # Franchise directory & rosters
│
└── docs/                       # Project documentation, PDF, PPTX & diagrams
```
