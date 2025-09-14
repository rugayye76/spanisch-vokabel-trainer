templates/quiz.html
{% extends "base.html" %}

{% block title %}Quiz - Spanisch Trainer{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <div class="flex flex-between">
            <div>
                <h2 class="card-title">Schreibquiz</h2>
                {% if chapter_name %}
                <p class="text-muted">{{ chapter_name }}</p>
                {% endif %}
            </div>
            <div class="text-right">
                {% if progress_text %}
                <div style="background-color: #f0f8ff; padding: 8px 12px; border-radius: 4px; border: 1px solid #cce7ff;">
                    <span style="font-size: 14px; color: #0066cc; font-weight: 500;">{{ progress_text }} gelernt</span>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <div style="max-width: 600px; margin: 0 auto;">
        {% if result %}
            <div class="alert alert-{{ result_class }}" style="margin-bottom: 20px;">
                <strong>{{ result }}</strong>
            </div>
        {% endif %}
        
        <div class="alert alert-info" style="margin-bottom: 30px;">
            <strong>Anleitung:</strong> Übersetzen Sie das deutsche Wort ins Spanische. 
            Geben Sie die spanische Übersetzung ein und klicken Sie auf "Prüfen".
        </div>
        
        {% if current_vocab %}
        <div style="background-color: #f8f9fa; border-radius: 12px; padding: 40px; text-align: center; margin-bottom: 30px; border: 2px solid #e9ecef;">
            <h1 style="font-size: 36px; font-weight: 600; color: #333; margin-bottom: 10px;">
                {{ current_vocab.deutsch }}
            </h1>
            <p class="text-muted" style="font-size: 16px;">Was heißt das auf Spanisch?</p>
        </div>
        
        <form method="post">
            <input type="hidden" name="vocab_index" value="{{ vocab_index }}">
            
            <div class="form-group">
                <label for="spanisch" class="form-label">
                    <strong>Spanische Übersetzung</strong>
                </label>
                <input type="text" class="form-input" id="spanisch" name="spanisch" 
                       placeholder="Ihre Antwort..." required autofocus 
                       style="font-size: 18px; padding: 15px;">
            </div>
            
            <div style="text-align: center; margin-bottom: 30px;">
                <button type="submit" class="btn btn-success btn-large">
                    Antwort prüfen
                </button>
            </div>
        </form>
        {% endif %}
        
        <div style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 1px solid #e0e0e0;">
            <a href="{{ url_for('chapter_overview') }}" class="btn btn-outline mr-10">
                Zurück zur Übersicht
            </a>
            <a href="{{ url_for('flashcards') }}" class="btn btn-secondary">
                Zu den Karteikarten
            </a>
        </div>
    </div>
</div>

<script>
// Auto-focus on Spanish input
document.addEventListener('DOMContentLoaded', function() {
    const spanishInput = document.getElementById('spanisch');
    if (spanishInput) {
        spanishInput.focus();
    }
});
</script>
{% endblock %}