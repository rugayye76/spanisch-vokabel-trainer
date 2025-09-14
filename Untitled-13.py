templates/index.html
{% extends "base.html" %}

{% block title %}Startseite - Spanisch Trainer{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="card-title">Willkommen, {{ username }}!</h1>
        <p class="text-muted">Wählen Sie ein Kapitel zum Lernen aus</p>
    </div>
    
    <div style="margin-bottom: 30px;">
        <p style="font-size: 16px; line-height: 1.8;">
            Wählen Sie eines der verfügbaren Kapitel aus, um mit dem Spanisch lernen zu beginnen. 
            Jedes Kapitel enthält verschiedene Vokabeln zu einem bestimmten Thema.
        </p>
    </div>
    
    {% if chapters %}
    <div class="grid grid-2">
        {% for chapter_id, chapter in chapters.items() %}
        <div class="card" style="background-color: #f8f9fa; border: 2px solid #e9ecef; transition: all 0.2s;">
            <div style="margin-bottom: 15px;">
                <h3 style="color: #0066cc; margin-bottom: 10px;">{{ chapter.name }}</h3>
                <p class="text-muted text-small">{{ chapter.vocabulary|length }} Vokabeln</p>
            </div>
            
            <div style="margin-top: auto;">
                <a href="{{ url_for('select_chapter', chapter_id=chapter_id) }}" 
                   class="btn btn-large" 
                   style="width: 100%; text-align: center;">
                    Kapitel auswählen
                </a>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="alert alert-info">
        <strong>Keine Kapitel verfügbar</strong><br>
        Es sind noch keine Kapitel erstellt worden. 
        {% if is_admin %}
        Gehen Sie zum Admin Panel, um Kapitel zu erstellen.
        {% else %}
        Kontaktieren Sie den Administrator.
        {% endif %}
    </div>
    {% endif %}
    
    <div style="margin-top: 40px; padding-top: 30px; border-top: 1px solid #e0e0e0;">
        <div class="flex flex-between">
            <div>
                <h3 style="margin-bottom: 10px;">Lerntipps</h3>
                <ul style="color: #666; line-height: 1.8;">
                    <li>Lernen Sie regelmäßig 10-15 Minuten täglich</li>
                    <li>Wiederholen Sie schwierige Vokabeln öfter</li>
                    <li>Nutzen Sie beide Lernmethoden: Karteikarten und Quiz</li>
                </ul>
            </div>
            
            <div class="text-right">
                {% if is_admin %}
                <a href="{{ url_for('admin_panel') }}" class="btn btn-danger mb-10">
                    Admin Panel
                </a>
                <br>
                {% endif %}
                <a href="{{ url_for('show_progress') }}" class="btn btn-outline">
                    Mein Fortschritt
                </a>
            </div>
        </div>
    </div>
</div>

<style>
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
{% endblock %}