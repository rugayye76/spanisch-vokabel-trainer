templates/progress.html
{% extends "base.html" %}

{% block title %}Lernfortschritt - Spanisch Trainer{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="text-center mb-5">
            <h1 class="display-4">
                <i class="fas fa-chart-line me-3"></i>
                Ihr Lernfortschritt
            </h1>
            <p class="lead text-muted">Verfolgen Sie Ihren Lernerfolg beim Spanisch lernen</p>
        </div>
    </div>
</div>

<div class="row g-4">
    <!-- Overall Progress -->
    <div class="col-12">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-trophy me-2"></i>
                    Gesamtfortschritt
                </h4>
            </div>
            <div class="card-body">
                <div class="row text-center">
                    <div class="col-md-3">
                        <div class="progress-stat">
                            <div class="display-4 text-primary mb-2">{{ "%.1f"|format(progress_percentage) }}%</div>
                            <h6 class="text-muted">Abgeschlossen</h6>
                        </div>
                    </div>
                    <div class="col-md-9">
                        <div class="d-flex align-items-center h-100">
                            <div class="w-100">
                                <div class="progress mb-3" style="height: 25px;">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: {{ progress_percentage }}%" 
                                         aria-valuenow="{{ progress_percentage }}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {{ known_count }} von {{ total_vocab }} gelernt
                                    </div>
                                </div>
                                <p class="text-muted mb-0">
                                    Sie haben bereits <strong>{{ known_count }}</strong> von <strong>{{ total_vocab }}</strong> Vokabeln gemeistert!
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row g-4 mt-2">
    <!-- Statistics Cards -->
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body text-center">
                <div class="mb-3">
                    <i class="fas fa-check-circle text-success" style="font-size: 3rem;"></i>
                </div>
                <h3 class="display-6 text-success">{{ known_count }}</h3>
                <h6 class="card-title">Gelernte Vokabeln</h6>
                <p class="text-muted">Diese Vokabeln beherrschen Sie bereits</p>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body text-center">
                <div class="mb-3">
                    <i class="fas fa-redo text-warning" style="font-size: 3rem;"></i>
                </div>
                <h3 class="display-6 text-warning">{{ review_count }}</h3>
                <h6 class="card-title">Zu wiederholen</h6>
                <p class="text-muted">Diese Vokabeln sollten Sie nochmal üben</p>
                {% if review_count > 0 %}
                <a href="{{ url_for('review_words') }}" class="btn btn-warning btn-sm">
                    <i class="fas fa-play me-1"></i>
                    Jetzt wiederholen
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body text-center">
                <div class="mb-3">
                    <i class="fas fa-question-circle text-muted" style="font-size: 3rem;"></i>
                </div>
                <h3 class="display-6 text-muted">{{ remaining_count }}</h3>
                <h6 class="card-title">Noch zu lernen</h6>
                <p class="text-muted">Diese Vokabeln sind noch neu für Sie</p>
            </div>
        </div>
    </div>
</div>

<!-- Learning Recommendations -->
<div class="row mt-5">
    <div class="col-12">
        <div class="card shadow">
            <div class="card-header bg-info text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-lightbulb me-2"></i>
                    Lernempfehlungen
                </h4>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="d-flex align-items-start mb-3">
                            <div class="flex-shrink-0">
                                <i class="fas fa-star text-warning fa-2x me-3"></i>
                            </div>
                            <div>
                                <h6 class="mb-1">Regelmäßig lernen</h6>
                                <p class="text-muted mb-0">
                                    Versuchen Sie täglich 10-15 Minuten zu lernen für optimale Ergebnisse.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-start mb-3">
                            <div class="flex-shrink-0">
                                <i class="fas fa-sync-alt text-primary fa-2x me-3"></i>
                            </div>
                            <div>
                                <h6 class="mb-1">Wiederholung ist der Schlüssel</h6>
                                <p class="text-muted mb-0">
                                    {% if review_count > 0 %}
                                    Sie haben {{ review_count }} Vokabeln zum Wiederholen. Beginnen Sie dort!
                                    {% else %}
                                    Alle Vokabeln sind auf dem neuesten Stand. Weiter so!
                                    {% endif %}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <div class="flex-shrink-0">
                                <i class="fas fa-mix text-success fa-2x me-3"></i>
                            </div>
                            <div>
                                <h6 class="mb-1">Verschiedene Lernmethoden nutzen</h6>
                                <p class="text-muted mb-0">
                                    Wechseln Sie zwischen Karteikarten und Schreibübungen ab.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <div class="flex-shrink-0">
                                <i class="fas fa-chart-line text-info fa-2x me-3"></i>
                            </div>
                            <div>
                                <h6 class="mb-1">Fortschritt verfolgen</h6>
                                <p class="text-muted mb-0">
                                    Schauen Sie regelmäßig hier vorbei, um Ihren Fortschritt zu sehen.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="row mt-4">
    <div class="col-12 text-center">
        <h5 class="mb-3">Was möchten Sie als nächstes tun?</h5>
        <div class="btn-group" role="group">
            {% if review_count > 0 %}
            <a href="{{ url_for('review_words') }}" class="btn btn-warning">
                <i class="fas fa-redo me-2"></i>
                Wiederholen ({{ review_count }})
            </a>
            {% endif %}
            <a href="{{ url_for('flashcards') }}" class="btn btn-primary">
                <i class="fas fa-cards-blank me-2"></i>
                Karteikarten
            </a>
            <a href="{{ url_for('quiz') }}" class="btn btn-success">
                <i class="fas fa-edit me-2"></i>
                Schreibquiz
            </a>
            <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">
                <i class="fas fa-home me-2"></i>
                Dashboard
            </a>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const targetWidth = parseFloat(progressBar.style.width);
        progressBar.style.width = '0%';
        
        setTimeout(() => {
            progressBar.style.transition = 'width 2s ease-in-out';
            progressBar.style.width = targetWidth + '%';
        }, 500);
    }
});
</script>
{% endblock %}