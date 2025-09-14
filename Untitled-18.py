templates/review.html
{% extends "base.html" %}

{% block title %}Wiederholen - Spanisch Trainer{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <div class="flex flex-between">
            <div>
                <h2 class="card-title">Vokabeln wiederholen</h2>
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
    
    {% if vokabeln %}
    <div style="text-align: center; margin-bottom: 30px;">
        <div class="alert alert-warning">
            <strong>Wiederholung:</strong> Diese Vokabeln haben Sie zum Wiederholen markiert. 
            Klicken Sie auf eine Karte, um die Antwort anzuzeigen.
        </div>
        <p style="color: #666; font-size: 14px;">
            <strong>{{ vokabeln|length }} Vokabeln</strong> zum Wiederholen verfügbar
        </p>
    </div>
    
    <!-- Review Flashcards Grid -->
    <div class="grid grid-3" style="margin-bottom: 40px;" id="review-container">
        {% for vocab in vokabeln %}
        <div class="review-flashcard" data-index="{{ loop.index0 }}">
            <div class="flashcard-content">
                <div class="german-side">
                    <div class="flashcard-word">{{ vocab.deutsch }}</div>
                    <div class="flashcard-hint">Klicken für Übersetzung</div>
                </div>
                
                <div class="spanish-side hidden">
                    <div class="flashcard-word" style="color: #0066cc;">{{ vocab.spanisch }}</div>
                    <div class="flashcard-translation">{{ vocab.deutsch }}</div>
                </div>
            </div>
            
            <div class="review-actions" style="margin-top: 15px;">
                <div class="flex gap-10">
                    <button class="btn btn-success btn-small know-btn" data-action="known" data-index="{{ loop.index0 }}">
                        ✅ Gelernt
                    </button>
                    <button class="btn btn-warning btn-small review-btn" data-action="review" data-index="{{ loop.index0 }}">
                        🔄 Nochmal
                    </button>
                </div>
                <button class="btn btn-outline btn-small reset-btn" style="margin-top: 8px; width: 100%;">
                    Zurück zur Frage
                </button>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Progress Stats -->
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-top: 30px;">
        <h4 style="text-align: center; margin-bottom: 20px; color: #333;">Wiederholungsfortschritt</h4>
        <div class="grid grid-3">
            <div class="text-center">
                <div id="mastered-count" style="font-size: 24px; font-weight: 600; color: #28a745;">0</div>
                <div class="text-small text-muted">Gemeistert</div>
            </div>
            <div class="text-center">
                <div id="still-review-count" style="font-size: 24px; font-weight: 600; color: #ffc107;">{{ vokabeln|length }}</div>
                <div class="text-small text-muted">Noch zu üben</div>
            </div>
            <div class="text-center">
                <div style="font-size: 24px; font-weight: 600; color: #0066cc;">{{ vokabeln|length }}</div>
                <div class="text-small text-muted">Gesamt</div>
            </div>
        </div>
    </div>
    
    {% else %}
    <div class="alert alert-info text-center">
        <strong>Keine Vokabeln zum Wiederholen!</strong><br>
        Sie haben alle Vokabeln gelernt oder noch keine zum Wiederholen markiert.
    </div>
    {% endif %}
    
    <!-- Navigation -->
    <div style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 1px solid #e0e0e0;">
        <a href="{{ url_for('flashcards') }}" class="btn btn-outline mr-10">
            Zurück zu den Karteikarten
        </a>
        <a href="{{ url_for('quiz') }}" class="btn btn-secondary mr-10">
            Zum Schreibquiz
        </a>
        <a href="{{ url_for('chapter_overview') }}" class="btn btn-outline">
            Kapitelübersicht
        </a>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    let masteredCount = 0;
    let stillReviewCount = {{ vokabeln|length }};
    
    function updateStats() {
        document.getElementById('mastered-count').textContent = masteredCount;
        document.getElementById('still-review-count').textContent = stillReviewCount;
    }
    
    // Add click handlers to review flashcards
    document.querySelectorAll('.review-flashcard').forEach(card => {
        const germanSide = card.querySelector('.german-side');
        const spanishSide = card.querySelector('.spanish-side');
        const knowBtn = card.querySelector('.know-btn');
        const reviewBtn = card.querySelector('.review-btn');
        const resetBtn = card.querySelector('.reset-btn');
        let isFlipped = false;
        let status = 'review'; // All cards start as review
        
        // Flip card on click
        card.addEventListener('click', function(e) {
            if (e.target.closest('button')) return; // Don't flip if clicking button
            
            if (!isFlipped) {
                germanSide.classList.add('hidden');
                spanishSide.classList.remove('hidden');
                card.style.backgroundColor = '#f8f9fa';
                isFlipped = true;
            }
        });
        
        // Mark as known (mastered)
        knowBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const vocabIndex = this.dataset.index;
            
            fetch('/flashcard_action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=known&vocab_index=${vocabIndex}`
            }).then(() => {
                if (status === 'review') {
                    masteredCount++;
                    stillReviewCount--;
                    status = 'known';
                    card.style.opacity = '0.6';
                    card.style.backgroundColor = '#d4edda';
                    updateStats();
                    
                    // Show success feedback
                    this.textContent = '✅ Gelernt!';
                    this.disabled = true;
                }
            });
        });
        
        // Keep for review
        reviewBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const vocabIndex = this.dataset.index;
            
            fetch('/flashcard_action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=review&vocab_index=${vocabIndex}`
            }).then(() => {
                // Card remains in review state
                card.style.backgroundColor = '#fff3cd';
                this.textContent = '🔄 Markiert';
                setTimeout(() => {
                    this.textContent = '🔄 Nochmal';
                }, 1000);
            });
        });
        
        // Reset card
        resetBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            germanSide.classList.remove('hidden');
            spanishSide.classList.add('hidden');
            card.style.backgroundColor = 'white';
            isFlipped = false;
        });
    });
    
    updateStats();
});
</script>
{% endblock %}