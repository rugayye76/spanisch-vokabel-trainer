templates/login.html
{% extends "base.html" %}

{% block title %}Anmeldung - Spanisch Trainer{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body p-4">
                <div class="text-center mb-4">
                    <i class="fas fa-sign-in-alt text-primary" style="font-size: 3rem;"></i>
                    <h2 class="card-title mt-3">Anmelden</h2>
                    <p class="text-muted">Willkommen zurück!</p>
                </div>
                
                <form method="post">
                    <div class="mb-3">
                        <label for="username" class="form-label">
                            <i class="fas fa-user me-1"></i>
                            Benutzername
                        </label>
                        <input type="text" class="form-control" id="username" name="username" 
                               placeholder="Ihr Benutzername" required>
                    </div>
                    
                    <div class="mb-4">
                        <label for="password" class="form-label">
                            <i class="fas fa-lock me-1"></i>
                            Passwort
                        </label>
                        <input type="password" class="form-control" id="password" name="password" 
                               placeholder="Ihr Passwort" required>
                    </div>
                    
                    <div class="d-grid mb-3">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            Anmelden
                        </button>
                    </div>
                </form>
                
                <div class="text-center">
                    <p class="mb-0">Noch kein Konto?</p>
                    <a href="{{ url_for('register') }}" class="btn btn-link">
                        <i class="fas fa-user-plus me-1"></i>
                        Jetzt registrieren
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
