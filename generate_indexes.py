import os
import re

# Define the HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent-color: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.4);
            --secondary-accent: #818cf8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(129, 140, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(167, 139, 250, 0.15) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(45, 212, 191, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-color);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 80px 20px;
        }}

        .container {{
            max-width: 1000px;
            width: 100%;
        }}

        header {{
            text-align: center;
            margin-bottom: 50px;
            animation: slideDown 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #38bdf8, #818cf8, #a78bfa);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            color: transparent;
            letter-spacing: -1px;
        }}

        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: #94a3b8;
            font-size: 1.1rem;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .back-link:hover {{
            color: var(--accent-color);
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}

        .file-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            text-decoration: none;
            color: var(--text-color);
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.5s ease forwards;
        }}

        .file-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2), 0 0 15px var(--accent-glow);
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .file-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; bottom: 0;
            width: 4px;
            background: linear-gradient(to bottom, var(--accent-color), var(--secondary-accent));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .file-card:hover::before {{
            opacity: 1;
        }}

        .icon {{
            font-size: 1.8rem;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .file-name {{
            font-size: 1.1rem;
            font-weight: 500;
            font-family: monospace;
            word-break: break-all;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <a href="../../index.html" class="back-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                Back to Coursework
            </a>
        </header>
        <div class="grid">
            {file_items}
        </div>
    </div>
</body>
</html>
"""

FILE_ITEM_TEMPLATE = """
            <a href="{filename}" class="file-card">
                <div class="icon">{icon}</div>
                <div class="file-name">{filename}</div>
            </a>
"""

def get_icon(filename):
    ext = filename.split('.')[-1].lower()
    if ext in ['html', 'htm']:
        return '📄'
    elif ext in ['jpg', 'jpeg', 'png', 'gif', 'jfif']:
        return '🖼️'
    elif ext in ['css']:
        return '🎨'
    elif ext in ['js']:
        return '📜'
    else:
        return '📎'

def format_title(dir_name):
    parts = dir_name.replace('week ', '').split('_')
    if len(parts) == 2:
        week = parts[0]
        day = 'Monday' if parts[1] == '1' else ('Friday' if parts[1] == '2' else f'Session {parts[1]}')
        return f'Week {week} ({day})'
    return dir_name.title()

def custom_sort_key(filename):
    match = re.match(r'([a-zA-Z]+)[-_]?(\d+)?', filename)
    if match:
        prefix = match.group(1).lower()
        num_str = match.group(2)
        num = int(num_str) if num_str else 0
        
        # Priority: topics (1), exercises/ex (2), others (3)
        if 'topic' in prefix:
            priority = 1
        elif 'ex' in prefix or 'exercise' in prefix:
            priority = 2
        else:
            priority = 3
            
        return (priority, num, filename)
    return (4, 0, filename)

def generate_indexes(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Only process subdirectories that look like 'week X_Y'
        dir_name = os.path.basename(root)
        if dir_name.startswith('week') and '_' in dir_name:
            print(f"Processing {root}...")
            
            # Get all files except index.html
            valid_files = [f for f in files if f != 'index.html']
            valid_files.sort(key=custom_sort_key)
            
            file_items = ""
            for f in valid_files:
                icon = get_icon(f)
                file_items += FILE_ITEM_TEMPLATE.format(filename=f, icon=icon)
                
            if not valid_files:
                file_items = '<div class="file-card" style="color: #94a3b8;">No files found.</div>'
                
            title = format_title(dir_name)
            html_content = HTML_TEMPLATE.format(title=title, file_items=file_items)
            
            index_path = os.path.join(root, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Created {index_path}")

if __name__ == "__main__":
    import sys
    # Prevent IndexError if no arg is passed
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_indexes(target_dir)
