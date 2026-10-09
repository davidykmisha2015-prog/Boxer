import re

# 1. Update style.css
with open('docs/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add light theme variables and fix grid colors
css = css.replace(':root {', """:root {
    /* Dark Theme (Default) */""")

css = css.replace('--text-muted: #A0A0B0;', """--text-muted: #A0A0B0;
    --grid-color: rgba(108, 114, 255, 0.05);
    --grid-glow: rgba(108, 114, 255, 0.4);
    --card-glow: rgba(108, 114, 255, 0.4);
    --terminal-bg: #0D0D12;
    --terminal-header: #1A1A24;
}

[data-theme="light"] {
    --bg-color: #F8F9FA;
    --card-bg: #FFFFFF;
    --card-border: #D1D5DB;
    --accent: #5A62D8;
    --text-main: #111827;
    --text-muted: #4B5563;
    --grid-color: rgba(90, 98, 216, 0.08);
    --grid-glow: rgba(90, 98, 216, 0.25);
    --card-glow: rgba(90, 98, 216, 0.2);
    --terminal-bg: #1E1E1E;
    --terminal-header: #2D2D2D;""")

css = css.replace('rgba(108, 114, 255, 0.05)', 'var(--grid-color)')
css = css.replace('rgba(108, 114, 255, 0.4)', 'var(--grid-glow)')
css = css.replace('background: #0D0D12;', 'background: var(--terminal-bg);')
css = css.replace('background: #1A1A24;', 'background: var(--terminal-header);')
css = css.replace('rgba(30, 30, 38, 0.5)', 'transparent')

# Add guide specific styles and theme toggle styles
css += """

/* Theme Toggle */
.icon-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: var(--text-main);
    padding: 4px 8px;
    transition: transform 0.2s;
}
.icon-btn:hover {
    transform: scale(1.1);
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
}

/* Documentation Content */
.guide-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 40px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
[data-theme="dark"] .guide-container {
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.guide-container h1 {
    font-size: 36px;
    margin-bottom: 30px;
    text-align: left;
}

.guide-container h2 {
    font-size: 24px;
    margin-top: 40px;
    margin-bottom: 16px;
    color: var(--accent);
}

.guide-container h3 {
    font-size: 20px;
    margin-top: 24px;
    margin-bottom: 12px;
}

.guide-container p, .guide-container li {
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 16px;
    color: var(--text-main);
}

.guide-container ul {
    margin-left: 24px;
    margin-bottom: 24px;
}

.guide-container pre {
    background: var(--terminal-bg);
    color: #E2E2E2;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 24px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    border: 1px solid var(--card-border);
}

.guide-container code {
    background: rgba(108, 114, 255, 0.1);
    color: var(--accent);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
}
"""
with open('docs/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update index.html
with open('docs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<div class="nav-links">', """<div class="nav-links">
            <a href="guide.html">Документація</a>""")
html = html.replace('<a href="https://github.com/davidykmisha2015-prog/Boxer" target="_blank">GitHub</a>', """<a href="https://github.com/davidykmisha2015-prog/Boxer" target="_blank">GitHub</a>
            <button id="theme-toggle" class="icon-btn" title="Змінити тему">☀️</button>""")

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update script.js
with open('docs/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

js += """

// Theme Switcher
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') || 'dark';

if (currentTheme === 'light') {
    document.body.setAttribute('data-theme', 'light');
    if(themeToggle) themeToggle.innerHTML = '🌙';
}

if(themeToggle) {
    themeToggle.addEventListener('click', () => {
        if (document.body.getAttribute('data-theme') === 'light') {
            document.body.removeAttribute('data-theme');
            localStorage.setItem('theme', 'dark');
            themeToggle.innerHTML = '☀️';
        } else {
            document.body.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            themeToggle.innerHTML = '🌙';
        }
    });
}
"""
with open('docs/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

