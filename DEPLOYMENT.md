# CricketIQ - Deployment Guide

Complete guide for deploying CricketIQ locally or to production.

## Local Development Setup

### Option 1: Automated Setup (Recommended)

#### macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Configure .env file
- Create MySQL database
- Initialize with sample data

#### Windows:
```bash
setup.bat
```

### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL**
   ```sql
   CREATE DATABASE cricketiq;
   ```

4. **Configure .env**
   ```
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=cricketiq
   ```

5. **Initialize Database**
   ```bash
   python init_db.py
   ```

6. **Run Application**
   ```bash
   python app.py
   ```

Visit: http://localhost:5000

## Production Deployment

### Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- MySQL 8.0+
- Nginx or Apache
- Gunicorn (WSGI server)
- Supervisor (process management)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, MySQL, Nginx
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx

# Install Gunicorn
pip install gunicorn
```

### Step 2: Clone and Setup Project

```bash
cd /var/www
sudo git clone <your-repo> cricketiq
cd cricketiq

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env for production
cat > .env << EOF
FLASK_ENV=production
FLASK_DEBUG=False
MYSQL_HOST=localhost
MYSQL_USER=cricketiq_user
MYSQL_PASSWORD=secure_password
MYSQL_DATABASE=cricketiq
SECRET_KEY=$(openssl rand -hex 32)
EOF

# Set permissions
sudo chown -R www-data:www-data .
```

### Step 3: Database Setup

```bash
# Create database
mysql -u root -p << EOF
CREATE DATABASE cricketiq;
CREATE USER 'cricketiq_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON cricketiq.* TO 'cricketiq_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Initialize
python init_db.py
```

### Step 4: Gunicorn Configuration

Create `/var/www/cricketiq/wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

Test Gunicorn:

```bash
gunicorn --workers 4 --bind localhost:8000 wsgi:app
```

### Step 5: Supervisor Configuration

Create `/etc/supervisor/conf.d/cricketiq.conf`:

```ini
[program:cricketiq]
directory=/var/www/cricketiq
command=/var/www/cricketiq/venv/bin/gunicorn --workers 4 --bind localhost:8000 wsgi:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/cricketiq/error.log
stdout_logfile=/var/log/cricketiq/access.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/cricketiq
sudo chown www-data:www-data /var/log/cricketiq

# Enable supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start cricketiq
```

### Step 6: Nginx Configuration

Create `/etc/nginx/sites-available/cricketiq`:

```nginx
upstream cricketiq {
    server localhost:8000;
}

server {
    listen 80;
    server_name your_domain.com;

    client_max_body_size 20M;

    location /static {
        alias /var/www/cricketiq/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://cricketiq;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cricketiq /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: SSL Certificate (HTTPS)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

Update Nginx to redirect HTTP to HTTPS.

### Step 8: Firewall Setup

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Docker Compose (with MySQL)

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: cricketiq
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  cricketiq:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: root
      MYSQL_DATABASE: cricketiq
    depends_on:
      - mysql
    volumes:
      - .:/app

volumes:
  mysql_data:
```

Build and run:

```bash
docker-compose up --build
```

## Cloud Deployment

### Heroku

1. Install Heroku CLI
2. Create Procfile:

```
web: gunicorn app:app
release: python init_db.py
```

3. Add MySQL addon:

```bash
heroku addons:create jawsdb:kitefin
heroku config:set FLASK_ENV=production
git push heroku main
```

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 cricketiq

# Create environment
eb create cricketiq-prod

# Deploy
eb deploy
```

### Google Cloud Run

```bash
# Authenticate
gcloud auth login

# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/cricketiq

# Deploy
gcloud run deploy cricketiq \
  --image gcr.io/PROJECT-ID/cricketiq \
  --platform managed \
  --region us-central1
```

## Monitoring & Logging

### Check Application Status

```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check logs
tail -f /var/log/cricketiq/error.log
tail -f /var/log/cricketiq/access.log

# Check MySQL connection
mysql -h localhost -u cricketiq_user -p cricketiq
```

### Log Rotation

Create `/etc/logrotate.d/cricketiq`:

```
/var/log/cricketiq/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        supervisorctl restart cricketiq > /dev/null
    endscript
}
```

## Performance Optimization

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_team_id ON players(team_id);
CREATE INDEX idx_player_id ON batting_statistics(player_id);
CREATE INDEX idx_match_date ON matches(match_date);
```

### Caching

Add Redis caching (optional):

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stats')
@cache.cached(timeout=300)
def api_stats():
    # Cache for 5 minutes
    pass
```

### Database Connection Pooling

Update config.py:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

## Backup & Recovery

### Automated Backups

```bash
# Create backup script
cat > /usr/local/bin/cricketiq-backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/cricketiq"
mkdir -p $BACKUP_DIR

mysqldump -u cricketiq_user -p$MYSQL_PASSWORD cricketiq > \
    $BACKUP_DIR/cricketiq_$DATE.sql

# Keep only 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete
EOF

chmod +x /usr/local/bin/cricketiq-backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /usr/local/bin/cricketiq-backup.sh
```

### Recovery

```bash
mysql -u cricketiq_user -p cricketiq < /backups/cricketiq/cricketiq_20240706.sql
```

## Troubleshooting

### Issue: 502 Bad Gateway

```bash
# Check if Gunicorn is running
sudo supervisorctl status cricketiq

# Restart
sudo supervisorctl restart cricketiq

# Check error logs
tail -f /var/log/cricketiq/error.log
```

### Issue: Database Connection Error

```bash
# Test MySQL connection
mysql -h localhost -u cricketiq_user -p cricketiq

# Check .env variables
cat .env

# Restart application
sudo supervisorctl restart cricketiq
```

### Issue: High Memory Usage

```bash
# Check memory usage
ps aux | grep gunicorn

# Reduce workers
# Edit /etc/supervisor/conf.d/cricketiq.conf
# Change: --workers 2

sudo supervisorctl restart cricketiq
```

## Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Use strong MySQL password
- [ ] Enable HTTPS/SSL
- [ ] Setup firewall rules
- [ ] Configure log rotation
- [ ] Use environment variables for secrets
- [ ] Regular database backups
- [ ] Monitor server resources
- [ ] Keep dependencies updated
- [ ] Setup monitoring & alerts

## Support

For issues during deployment:
1. Check logs in `/var/log/cricketiq/`
2. Review configuration in `.env`
3. Test MySQL connectivity
4. Verify file permissions
5. Check firewall rules

---

For more help, check README.md or QUICKSTART.md
