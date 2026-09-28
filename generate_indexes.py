import os

# Define the HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg-color: #f4f1ea;
            --text-color: #333333;
            --link-color: #2c7a7b;
            --border-color: #d8d0c0;
            --hover-bg: #eae3d3;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}

        .container {{
            max-width: 800px;
            width: 100%;
        }}

        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
        }}

        h1 {{
            font-size: 2rem;
            font-weight: 300;
            color: #2c3e50;
            margin: 0;
        }}

        .back-link {{
            text-decoration: none;
            color: #718096;
            font-weight: 500;
            display: flex;
            align-items: center;
            transition: color 0.2s;
        }}
        
        .back-link:hover {{
            color: var(--link-color);
        }}

        .back-link::before {{
            content: '←';
            margin-right: 8px;
            font-size: 1.2em;
        }}

        .file-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }}

        .file-item {{
            border-bottom: 1px solid var(--border-color);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
        }}

        .file-item:last-child {{
            border-bottom: none;
        }}

        .file-item:hover {{
            background-color: rgba(255,255,255, 0.9);
            transform: translateX(4px);
        }}

        .file-link {{
            display: flex;
            align-items: center;
            padding: 16px 24px;
            text-decoration: none;
            color: var(--link-color);
            font-size: 1.05rem;
            font-weight: 500;
            width: 100%;
            font-family: monospace;
        }}

        .icon {{
            margin-right: 12px;
            font-size: 1.2rem;
            color: #a0aec0;
        }}

    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <a href="../../index.html" class="back-link">Back to Coursework</a>
        </div>
        <ul class="file-list">
            {file_items}
        </ul>
    </div>
</body>
</html>
"""

FILE_ITEM_TEMPLATE = """
            <li class="file-item">
                <a href="{filename}" class="file-link">
                    <span class="icon">{icon}</span> {filename}
                </a>
            </li>
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

def generate_indexes(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Only process subdirectories that look like 'week X_Y'
        dir_name = os.path.basename(root)
        if dir_name.startswith('week') and '_' in dir_name:
            print(f"Processing {root}...")
            
            # Get all files except index.html
            valid_files = [f for f in files if f != 'index.html']
            valid_files.sort()
            
            file_items = ""
            for f in valid_files:
                icon = get_icon(f)
                file_items += FILE_ITEM_TEMPLATE.format(filename=f, icon=icon)
                
            if not valid_files:
                file_items = '<li class="file-item" style="padding: 16px 24px; color: #a0aec0;">No files found.</li>'
                
            title = format_title(dir_name)
            html_content = HTML_TEMPLATE.format(title=title, file_items=file_items)
            
            index_path = os.path.join(root, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Created {index_path}")

if __name__ == "__main__":
    import sys
    generate_indexes(sys.argv[1])
