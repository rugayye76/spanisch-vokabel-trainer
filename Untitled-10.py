templates/chapter_overwiev.html
{% extends "base.html" %}

{% block title %}{{ chapter.name }} - Spanisch Trainer{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <div class="flex flex-between">
            <div>
                <h1 class="card-title">{{ chapter.name }}</h1>
                <p class="text-muted">{{ progress.total }} Vokabeln insgesamt</p>
            </div>
            <div class="text-right">
                <a href="{{ url_for('index') }}" class="btn btn-outline">
                    Anderes Kapitel wählen
                </a>
            </div>
        </div>
    </div>
    
    <!-- Progress Overview -->
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
        <h3 style="margin-bottom: 20px; color: #333;">Ihr Fortschritt</h3>
        
        <div class="progress">
            <div class="progress-bar" style="width: {{ (progress.known / progress.total * 100) if progress.total > 0 else 0 }}%;"></div>
        </div>
        <div class="progress-text">{{ progress.known }} von {{ progress.total }} gelernt</div>
        
        <div class="grid grid-3 mt-20">
            <div class="text-center">
                <div style="font-size: 24px; font-weight: 600; color: #28a745;">{{ progress.known }}</div>
                <div class="text-small text-muted">Gelernt</div>
            </div>
            <div class="text-center">
                <div style="font-size: 24px; font-weight: 600; color: #ffc107;">{{ progress.review }}</div>
                <div class="text-small text-muted">Wiederholen</div>
            </div>
            <div class="text-center">
                <div style="font-size: 24px; font-weight: 600; color: #6c757d;">{{ progress.total - progress.known - progress.review }}</div>
                <div class="text-small text-muted">Noch zu lernen</div>
            </div>
        </div>
    </div>
    
    <!-- Learning Methods -->
    <h3 style="margin-bottom: 20px;">Lernmethoden</h3>
    
    <div class="grid grid-3 gap-20">
        <!-- Flashcards -->
        <div class="card" style="background-color: #fff5f5; border: 2px solid #fed7d7;">
            <div style="text-align: center;">
                <div style="font-size: 48px; color: #0066cc; margin-bottom: 15px;">📚</div>
                <h4 style="color: #333; margin-bottom: 10px;">Karteikarten</h4>
                <p class="text-muted text-small" style="margin-bottom: 20px;">
                    Interaktive Karteikarten zum Durchblättern und Merken
                </p>
                <a href="{{ url_for('flashcards') }}" class="btn btn-large" style="width: 100%;">
                    Karteikarten starten
                </a>
            </div>
        </div>
        
        <!-- Quiz -->
        <div class="card" style="background-color: #f0fff4; border: 2px solid #c6f6d5;">
            <div style="text-align: center;">
                <div style="font-size: 48px; color: #0066cc; margin-bottom: 15px;">✏️</div>
                <h4 style="color: #333; margin-bottom: 10px;">Schreibquiz</h4>
                <p class="text-muted text-small" style="margin-bottom: 20px;">
                    Aktiv lernen durch Eingabe der spanischen Übersetzung
                </p>
                <a href="{{ url_for('quiz') }}" class="btn btn-success btn-large" style="width: 100%;">
                    Quiz starten
                </a>
            </div>
        </div>
    </div>
    
    {% if progress.review > 0 %}
    <!-- Review Section -->
    <div style="background-color: #fff9c4; border: 2px solid #fad776; border-radius: 8px; padding: 20px; margin-top: 30px;">
        <div class="flex flex-between">
            <div>
                <h4 style="color: #856404; margin-bottom: 5px;">Wiederholung empfohlen</h4>
                <p class="text-small" style="color: #856404; margin-bottom: 0;">
                    Sie haben {{ progress.review }} Vokabeln zum Wiederholen markiert
                </p>
            </div>
            <div>
                <a href="{{ url_for('review_words') }}" class="btn btn-warning">
                    Jetzt wiederholen
                </a>
            </div>
        </div>
    </div>
    {% endif %}
    
    <!-- Chapter Vocabulary Preview -->
    <div style="margin-top: 40px;">
        <h3 style="margin-bottom: 20px;">Vokabeln in diesem Kapitel</h3>
        <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; max-height: 300px; overflow-y: auto;">
            <div class="grid grid-2 gap-10">
                {% for vocab in chapter.vocabulary %}
                <div style="display: flex; justify-content: space-between; padding: 8px 12px; background-color: white; border-radius: 4px; border: 1px solid #e0e0e0;">
                    <span style="font-weight: 500;">{{ vocab.deutsch }}</span>
                    <span style="color: #0066cc;">{{ vocab.spanisch }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}