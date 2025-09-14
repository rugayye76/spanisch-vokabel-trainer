templates/admin_login.html
{% extends "base.html" %}

{% block title %}Admin Anmeldung - Spanisch Trainer{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body p-4">
                <div class="text-center mb-4">
                    <i class="fas fa-shield-alt text-danger" style="font-size: 3rem;"></i>
                    <h2 class="card-title mt-3">Admin Anmeldung</h2>
                    <p class="text-muted">Nur für Administratoren</p>
                </div>
                
                <form method="post">
                    <div class="mb-3">
                        <label for="username" class="form-label">
                            <i class="fas fa-user me-1"></i>
                            Admin Benutzername
                        </label>
                        <input type="text" class="form-control" id="username" name="username" 
                               placeholder="Admin Benutzername" required>
                    </div>
                    
                    <div class="mb-4">
                        <label for="password" class="form-label">
                            <i class="fas fa-lock me-1"></i>
                            Admin Passwort
                        </label>
                        <input type="password" class="form-control" id="password" name="password" 
                               placeholder="Admin Passwort" required>
                    </div>
                    
                    <div class="d-grid mb-3">
                        <button type="submit" class="btn btn-danger btn-lg">
                            <i class="fas fa-shield-alt me-2"></i>
                            Als Admin anmelden
                        </button>
                    </div>
                </form>
                
                <div class="text-center">
                    <a href="{{ url_for('index') }}" class="btn btn-link">
                        <i class="fas fa-arrow-left me-1"></i>
                        Zurück zur Website
                    </a>
                </div>
                
                <div class="alert alert-info mt-3" role="alert">
                    <i class="fas fa-info-circle me-2"></i>
                    <small><strong>Standard Admin-Daten:</strong><br>
                    Benutzername: admin<br>
                    Passwort: admin123</small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}