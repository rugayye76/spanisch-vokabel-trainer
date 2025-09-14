templates/base.html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Spanisch Trainer{% endblock %}</title>
    
    <!-- Theme Flash Prevention Script -->
    <script>
        // Set theme immediately before CSS loads to prevent flash
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="{{ url_for('index') }}" class="logo">Spanisch Trainer</a>
            
            <nav>
                <ul class="nav">
                    <li><a href="{{ url_for('index') }}" class="nav-link">Startseite</a></li>
                    {% if session.get('username') %}
                    {% if session.get('selected_chapter') %}
                    <li><a href="{{ url_for('chapter_overview') }}" class="nav-link">Tools/Module</a></li>
                    {% endif %}
                    {% endif %}
                    <li><a href="{{ url_for('about') }}" class="nav-link">Über mich</a></li>
                </ul>
            </nav>
            
            {% if session.get('username') %}
            <div class="user-info">
                <span>{{ session['username'] }}</span>
                {% if session.get('username') == 'admin' %}
                <span class="badge-admin">ADMIN</span>
                <a href="{{ url_for('admin_panel') }}" class="logout-btn">Admin Panel</a>
                {% endif %}
                <button onclick="toggleTheme()" class="theme-toggle-btn" title="Zwischen Hell- und Dunkelmodus wechseln">
                    <span id="theme-icon">🌙</span>
                </button>
                <a href="{{ url_for('logout') }}" class="logout-btn">Abmelden</a>
            </div>
            {% endif %}
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <!-- Flash Messages -->
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'error' if category == 'error' else category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="student-attribution">
                Diese Seite wurde von Rugayye Agakoc, Schülerin der EF erstellt
            </div>
            <p class="text-muted text-small">
                Spanisch Trainer - Einfach Spanisch lernen
            </p>
        </div>
    </footer>

    <script>
        // Theme Management
        function initTheme() {
            // Set theme based on user preference or default
            const savedTheme = localStorage.getItem('theme') || 'light';
            
            document.documentElement.setAttribute('data-theme', savedTheme);
            updateThemeIcon(savedTheme);
            
            console.log('Theme initialized:', savedTheme);
        }
        
        function updateThemeIcon(theme) {
            const themeIcon = document.getElementById('theme-icon');
            if (themeIcon) {
                themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
            }
        }
        
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            console.log('Switching theme from', currentTheme, 'to', newTheme);
            
            // Update UI immediately
            document.documentElement.setAttribute('data-theme', newTheme);
            updateThemeIcon(newTheme);
            localStorage.setItem('theme', newTheme);
            
            console.log('Theme switched successfully to:', newTheme);
            
            // Update server-side preference with explicit theme value (only if logged in)
            {% if session.get('username') %}
            fetch('{{ url_for("set_theme") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'theme=' + encodeURIComponent(newTheme)
            }).catch(err => console.warn('Theme preference not saved:', err));
            {% endif %}
        }
        
        // Initialize theme when page loads
        document.addEventListener('DOMContentLoaded', initTheme);
    </script>
    
    {% block scripts %}{% endblock %}
</body>
</html>