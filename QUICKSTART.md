# CricketIQ - Quick Start Guide

Get CricketIQ running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- MySQL Server running
- pip (comes with Python)

## Step-by-Step Setup

### 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database (2 min)

Open MySQL and run:

```sql
CREATE DATABASE cricketiq;
```

### 3. Configure Environment (30 sec)

Edit `.env` file with your MySQL credentials:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

If no password: leave `MYSQL_PASSWORD=` empty

### 4. Initialize Database (1 min)

```bash
python init_db.py
```

This loads sample data (8 teams, 9 players, 3 matches).

### 5. Start the App (30 sec)

```bash
python app.py
```

You'll see:
```
[v0] Creating database tables...
[v0] Database tables created successfully!
[v0] Starting Flask development server...
 * Running on http://0.0.0.0:5000
```

### 6. Open in Browser

Visit: **http://localhost:5000**

## What You'll See

- **Home**: Dashboard with team/player/match counts
- **Teams**: 8 IPL teams with info
- **Players**: 9 sample players with roles
- **Matches**: 3 sample matches with scores

## Common Issues

| Issue | Solution |
|-------|----------|
| "Access denied for user 'root'" | Check MYSQL_PASSWORD in .env |
| "Unknown database 'cricketiq'" | Run `CREATE DATABASE cricketiq;` in MySQL |
| "Port 5000 already in use" | Change port in app.py line 213 |
| "ModuleNotFoundError: No module named 'flask'" | Run `pip install -r requirements.txt` |

## Next Steps

1. **Add More Data**: Edit `init_db.py` and run it again
2. **Customize Styles**: Edit `static/css/style.css`
3. **Add Features**: Check the full README.md
4. **Deploy**: Follow deployment guide in README.md

## File Changes Needed

Only edit these for basic setup:
- **.env** - Your MySQL credentials
- **init_db.py** - To add custom data
- **config.py** - For production settings

## Database Reset

To start fresh:

```sql
DROP DATABASE cricketiq;
CREATE DATABASE cricketiq;
```

Then run: `python init_db.py`

## MySQL Not Running?

### macOS (Homebrew)
```bash
brew services start mysql
```

### Windows
- Open Services
- Find "MySQL"
- Click "Start"

### Linux
```bash
sudo systemctl start mysql
```

## Help!

Check the main **README.md** for:
- Full documentation
- All features
- Architecture details
- Troubleshooting

---

That's it! You now have a working IPL analytics platform.

**Questions?** Check README.md or the inline code comments.
