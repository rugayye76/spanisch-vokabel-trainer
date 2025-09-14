templates/disclaimer.html
{% extends "base.html" %}

{% block title %}Haftungsausschluss - Spanisch Trainer{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow">
            <div class="card-body text-center p-5">
                <div class="mb-4">
                    <i class="fas fa-exclamation-triangle text-warning" style="font-size: 4rem;"></i>
                </div>
                
                <h2 class="card-title mb-4">Haftungsausschluss</h2>
                
                <div class="alert alert-info" role="alert">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Wichtiger Hinweis</strong>
                </div>
                
                <p class="lead mb-4">
                    Diese Website dient ausschließlich zu Lern- und Bildungszwecken. 
                </p>
                
                <div class="text-start mb-4">
                    <h5>Bitte beachten Sie:</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2">
                            <i class="fas fa-check text-success me-2"></i>
                            Es gibt keine Garantie auf Richtigkeit der Inhalte
                        </li>
                        <li class="mb-2">
                            <i class="fas fa-check text-success me-2"></i>
                            Die Anwendung speichert Daten nur temporär
                        </li>
                        <li class="mb-2">
                            <i class="fas fa-check text-success me-2"></i>
                            Ihre Privatsphäre wird respektiert
                        </li>
                    </ul>
                </div>
                
                <p class="text-muted mb-4">
                    Durch die Nutzung dieser Anwendung stimmen Sie diesen Bedingungen zu.
                </p>
                
                <a href="{{ url_for('accept') }}" class="btn btn-success btn-lg">
                    <i class="fas fa-check me-2"></i>
                    Akzeptieren und Fortfahren
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
