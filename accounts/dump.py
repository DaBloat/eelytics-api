"""NOT SUPPOSED TO BE RUN!"""

@app.route('/api/admin/raw-data')
def admin_raw_data():
    db = get_db()
    # Force a checkpoint so external viewers stay updated
    db.execute("PRAGMA wal_checkpoint(PASSIVE);")
    
    cur = db.execute("SELECT id, username, email, password FROM accounts ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    
    # Return as a simple list for the monitor to display
    return render_template('admin_list.html', accounts=rows)

# 2. The Auto-Refreshing Dashboard
@app.route('/api/admin/monitor')
def monitor():
    return """
    <html>
        <head>
            <title>Eelytics Admin Monitor</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body { background: #1e1e1e; color: #d4d4d4; font-family: 'Consolas', monospace; padding: 20px; }
                .card { border: 1px solid #333; padding: 10px; margin-bottom: 5px; border-radius: 4px; }
                .username { color: #4ec9b0; font-weight: bold; }
                h2 { color: #ce9178; }
            </style>
        </head>
        <body>
            <h2>Recent Eels in the Tank</h2>
            <iframe src="/api/admin/raw-data" style="width:100%; height:80vh; border:none;"></iframe>
        </body>
    </html>
    """
