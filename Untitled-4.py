static/style.css
/* Modernes Design für Spanisch Trainer mit Dark/Light Mode */

/* CSS Variables für Theme System */
:root {
    /* Light Theme (Standard) */
    --bg-color: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --text-color: #2d3748;
    --text-muted: #718096;
    --border-color: #e2e8f0;
    --primary-color: #4f46e5;
    --primary-hover: #4338ca;
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --card-bg: #ffffff;
    --header-bg: #ffffff;
    --footer-bg: #f8f9fa;
    --shadow: rgba(0, 0, 0, 0.1);
    --success-bg: #d4edda;
    --success-border: #c3e6cb;
    --success-text: #155724;
    --error-bg: #f8d7da;
    --error-border: #f5c6cb;
    --error-text: #721c24;
    --warning-bg: #fff3cd;
    --warning-border: #ffeaa7;
    --warning-text: #856404;
    --info-bg: #d1ecf1;
    --info-border: #bee5eb;
    --info-text: #0c5460;
    --text-inverse: #ffffff;
    --primary-color-alpha: rgba(0, 102, 204, 0.1);
    --secondary-color: #6c757d;
    --secondary-hover: #5a6268;
    --success-color: #28a745;
    --success-hover: #218838;
    --warning-color: #ffc107;
    --warning-hover: #e0a800;
    --danger-color: #dc3545;
    --danger-hover: #c82333;
    --success-light: #f0fff4;
    --warning-light: #fffef0;
    --shadow-strong: rgba(0, 0, 0, 0.15);
    --warning-contrast: #000000;
}

/* Dark Theme */
[data-theme="dark"] {
    --bg-color: #0f0f23;
    --bg-secondary: #1a1a2e;
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --text-color: #e4e4e4;
    --text-muted: #b0b0b0;
    --border-color: #404040;
    --primary-color: #4da6ff;
    --primary-hover: #3399ff;
    --card-bg: #2d2d2d;
    --header-bg: #1a1a1a;
    --footer-bg: #2d2d2d;
    --shadow: rgba(0, 0, 0, 0.3);
    --success-bg: #155724;
    --success-border: #28a745;
    --success-text: #d4edda;
    --error-bg: #721c24;
    --error-border: #dc3545;
    --error-text: #f8d7da;
    --warning-bg: #856404;
    --warning-border: #ffc107;
    --warning-text: #fff3cd;
    --info-bg: #0c5460;
    --info-border: #17a2b8;
    --info-text: #d1ecf1;
    --text-inverse: #ffffff;
    --primary-color-alpha: rgba(77, 166, 255, 0.1);
    --secondary-color: #4a4a4a;
    --secondary-hover: #5a5a5a;
    --success-color: #20c997;
    --success-hover: #1aa179;
    --warning-color: #ffc107;
    --warning-hover: #ffcd39;
    --danger-color: #e74c3c;
    --danger-hover: #c0392b;
    --success-light: #1a4a3a;
    --warning-light: #4a3a1a;
    --shadow-strong: rgba(0, 0, 0, 0.4);
    --warning-contrast: #000000;
}

/* Reset und Basis */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
    line-height: 1.7;
    color: var(--text-color);
    background: var(--bg-color);
    font-size: 16px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* Light mode gradient background */
body:not([data-theme="dark"]) {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Dark mode gradient background */
[data-theme="dark"] body {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header/Navigation */
.header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 20px 0;
    position: sticky;
    top: 0;
    z-index: 100;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 28px;
    font-weight: 800;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: -0.5px;
}

.nav {
    display: flex;
    list-style: none;
    gap: 30px;
}

.nav-link {
    color: var(--text-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.nav-link:hover {
    color: var(--primary-color);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 15px;
    font-size: 14px;
    color: var(--text-muted);
    transition: color 0.3s ease;
}

.logout-btn {
    background: none;
    border: 1px solid var(--border-color);
    padding: 5px 10px;
    border-radius: 4px;
    color: var(--text-color);
    text-decoration: none;
    font-size: 12px;
    transition: background-color 0.2s;
}

.logout-btn:hover {
    background-color: var(--bg-secondary);
}

/* Main Content */
.main-content {
    min-height: calc(100vh - 200px);
    padding: 40px 0;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 24px;
    background: var(--primary-gradient);
    color: white;
    text-decoration: none;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    letter-spacing: 0.025em;
    position: relative;
    overflow: hidden;
}

.btn:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
}

.btn:active {
    transform: translateY(0) scale(0.98);
    transition: all 0.1s ease;
}

.btn-secondary {
    background-color: var(--secondary-color);
}

.btn-secondary:hover {
    background-color: var(--secondary-hover);
}

.btn-success {
    background-color: var(--success-color);
}

.btn-success:hover {
    background-color: var(--success-hover);
}

.btn-warning {
    background-color: var(--warning-color);
    color: var(--warning-contrast);
}

.btn-warning:hover {
    background-color: var(--warning-hover);
}

.btn-danger {
    background-color: var(--danger-color);
}

.btn-danger:hover {
    background-color: var(--danger-hover);
}

.btn-outline {
    background-color: transparent;
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}

.btn-outline:hover {
    background-color: var(--primary-color);
    color: var(--text-inverse);
}

.btn-large {
    padding: 15px 30px;
    font-size: 16px;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--primary-gradient);
}

.card-header {
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 15px;
    padding-bottom: 15px;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 5px;
}

/* Forms */
.form-group {
    margin-bottom: 20px;
}

.form-label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: var(--text-color);
}

.form-input {
    width: 100%;
    padding: 16px 20px;
    border: 2px solid transparent;
    border-radius: 12px;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: var(--text-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    outline: none;
}

.form-input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1), 0 4px 20px rgba(79, 70, 229, 0.2);
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.2);
}

/* Alerts */
.alert {
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    border: 1px solid transparent;
}

.alert-success {
    background-color: var(--success-bg);
    border-color: var(--success-border);
    color: var(--success-text);
}

.alert-error {
    background-color: var(--error-bg);
    border-color: var(--error-border);
    color: var(--error-text);
}

.alert-warning {
    background-color: var(--warning-bg);
    border-color: var(--warning-border);
    color: var(--warning-text);
}

.alert-info {
    background-color: var(--info-bg);
    border-color: var(--info-border);
    color: var(--info-text);
}

/* Tables */
.table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}

.table th,
.table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-color);
}

.table th {
    background-color: var(--bg-secondary);
    font-weight: 600;
    color: var(--text-color);
}

/* Flexbox utilities */
.flex {
    display: flex;
}

.flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.flex-wrap {
    flex-wrap: wrap;
}

.gap-10 {
    gap: 10px;
}

.gap-20 {
    gap: 20px;
}

/* Text utilities */
.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.text-muted {
    color: var(--text-muted);
}

.text-small {
    font-size: 12px;
}

.text-large {
    font-size: 18px;
}

.font-bold {
    font-weight: 600;
}

/* Spacing */
.mt-10 { margin-top: 10px; }
.mt-20 { margin-top: 20px; }
.mt-30 { margin-top: 30px; }
.mb-10 { margin-bottom: 10px; }
.mb-20 { margin-bottom: 20px; }
.mb-30 { margin-bottom: 30px; }
.ml-10 { margin-left: 10px; }
.mr-10 { margin-right: 10px; }

/* Grid System */
.grid {
    display: grid;
    gap: 20px;
}

.grid-2 {
    grid-template-columns: 1fr 1fr;
}

.grid-3 {
    grid-template-columns: 1fr 1fr 1fr;
}

.grid-4 {
    grid-template-columns: 1fr 1fr 1fr 1fr;
}

/* Flashcard Stack */
.flashcard-stack {
    position: relative;
    width: 100%;
    max-width: 400px;
    height: 350px;
    margin: 0 auto;
    overflow: hidden;
}

.flashcard {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 24px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    cursor: grab;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.08);
    touch-action: pan-x;
    user-select: none;
    position: relative;
    overflow: hidden;
}

.flashcard::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.5s;
}

.flashcard:hover::before {
    left: 100%;
}

.flashcard:active {
    cursor: grabbing;
}

.flashcard.dragging {
    transition: none;
    z-index: 10 !important;
}

.flashcard.swiping-right {
    border-color: var(--success-color);
    background-color: var(--success-light);
}

.flashcard.swiping-left {
    border-color: var(--warning-color);
    background-color: var(--warning-light);
}

.flashcard:nth-child(1) { transform: translateY(0px) scale(1); z-index: 3; }
.flashcard:nth-child(2) { transform: translateY(6px) scale(0.97); z-index: 2; opacity: 0.9; }
.flashcard:nth-child(3) { transform: translateY(12px) scale(0.94); z-index: 1; opacity: 0.8; }

.flashcard.flipped {
    background-color: var(--bg-secondary);
    border-color: var(--primary-color);
}

.flashcard-word {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 15px;
    color: var(--text-color);
}

.flashcard-translation {
    font-size: 24px;
    color: var(--primary-color);
    margin-bottom: 15px;
    font-weight: 600;
}

.flashcard-hint {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
}

.swipe-indicator {
    position: absolute;
    top: 20px;
    font-size: 48px;
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.swipe-indicator.right {
    right: 20px;
    color: var(--success-color);
}

.swipe-indicator.left {
    left: 20px;
    color: var(--warning-color);
}

.swipe-indicator.visible {
    opacity: 1;
}

/* Progress Bar */
.progress {
    background-color: var(--border-color);
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-bar {
    background-color: var(--primary-color);
    height: 100%;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 14px;
    color: var(--text-muted);
    text-align: center;
    margin-top: 5px;
}

/* Footer */
.footer {
    background-color: var(--footer-bg);
    border-top: 1px solid var(--border-color);
    padding: 30px 0;
    margin-top: 50px;
    text-align: center;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.student-attribution {
    background-color: var(--info-bg);
    border: 1px solid var(--info-border);
    border-radius: 8px;
    padding: 15px;
    margin: 20px 0;
    text-align: center;
    font-size: 14px;
    color: var(--info-text);
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .header .container {
        flex-direction: column;
        gap: 15px;
    }
    
    .nav {
        gap: 20px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .grid-2,
    .grid-3,
    .grid-4 {
        grid-template-columns: 1fr;
    }
    
    .flashcard-stack {
        max-width: 320px;
        height: 280px;
    }
    
    .flashcard {
        padding: 20px;
    }
    
    .flashcard-word {
        font-size: 22px;
    }
    
    .flashcard-translation {
        font-size: 20px;
    }
    
    .swipe-indicator {
        font-size: 36px;
        top: 15px;
    }
}

/* Theme Toggle Button */
.theme-toggle-btn {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
    padding: 8px;
    border-radius: 50%;
    color: var(--text-color);
    cursor: pointer;
    font-size: 18px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.theme-toggle-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1) rotate(180deg);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    border-color: var(--primary-color);
}

#theme-icon {
    transition: transform 0.3s ease;
}

.theme-toggle-btn:active #theme-icon {
    transform: rotate(180deg);
}

/* Utilities */
.hidden {
    display: none;
}

.visible {
    display: block;
}

.no-select {
    user-select: none;
}

.pointer {
    cursor: pointer;
}

/* Animation */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.slide-up {
    animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Review Flashcards */
.review-flashcard {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px var(--shadow);
}

.review-flashcard:hover {
    box-shadow: 0 4px 8px var(--shadow-strong);
    transform: translateY(-2px);
}

.review-flashcard .flashcard-word {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
}

.review-flashcard .flashcard-hint {
    font-size: 12px;
    color: var(--text-muted);
    font-style: italic;
}

.review-flashcard .flashcard-translation {
    font-size: 16px;
    color: var(--text-muted);
    margin-top: 8px;
}

.btn-small {
    padding: 6px 12px;
    font-size: 12px;
    border-radius: 4px;
}

/* Admin Badge */
.badge-admin {
    background-color: var(--danger-color);
    color: var(--text-inverse);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 500;
    display: inline-block;
}