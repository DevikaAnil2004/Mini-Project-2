// CricketIQ - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    console.log('[v0] CricketIQ application initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    addSmoothScroll();
    
    // Load stats on home page
    if (document.getElementById('stats-container')) {
        loadStats();
    }
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add smooth scrolling to all internal links
 */
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Load statistics from API
 */
function loadStats() {
    fetch('/api/stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load stats');
            }
            return response.json();
        })
        .then(data => {
            console.log('[v0] Stats loaded:', data);
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('[v0] Error loading stats:', error);
        });
}

/**
 * Update statistics display
 */
function updateStatsDisplay(stats) {
    const statsContainer = document.getElementById('stats-container');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="stats-updated">
                <p class="text-muted small">Last updated: ${new Date().toLocaleTimeString()}</p>
            </div>
        `;
    }
}

/**
 * Format large numbers with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Get player role badge color
 */
function getRoleBadgeColor(role) {
    const colors = {
        'Batsman': 'info',
        'Bowler': 'warning',
        'All-rounder': 'success',
        'Wicket-keeper': 'danger'
    };
    return colors[role] || 'secondary';
}

/**
 * Get match status badge color
 */
function getStatusBadgeColor(status) {
    const colors = {
        'completed': 'success',
        'live': 'danger',
        'scheduled': 'secondary',
        'cancelled': 'dark'
    };
    return colors[status] || 'secondary';
}

/**
 * Add event listeners to tables for interactivity
 */
function addTableInteractivity() {
    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

/**
 * Validate form before submission
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        return form.checkValidity() === false ? false : true;
    }
    return true;
}

/**
 * Show loading spinner
 */
function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.className = 'text-center my-4';
    spinner.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
    return spinner;
}

/**
 * Clear table body
 */
function clearTableBody(tableId) {
    const table = document.getElementById(tableId);
    if (table) {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.innerHTML = '';
        }
    }
}

/**
 * Add row to table
 */
function addTableRow(tableId, rowData) {
    const table = document.getElementById(tableId);
    if (table) {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            const row = document.createElement('tr');
            row.innerHTML = rowData;
            tbody.appendChild(row);
        }
    }
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename) {
    const csv = [];
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            const cols = row.querySelectorAll('td, th');
            const csvRow = [];
            cols.forEach(col => {
                csvRow.push(col.innerText);
            });
            csv.push(csvRow.join(','));
        });
    });
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

console.log('[v0] CricketIQ scripts loaded successfully');
