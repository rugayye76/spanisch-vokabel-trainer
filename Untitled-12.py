templates/flashcards.html
{% extends "base.html" %}

{% block title %}Karteikarten - Spanisch Trainer{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <div class="flex flex-between">
            <div>
                <h2 class="card-title">Karteikarten</h2>
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
    
    <div style="text-align: center; margin-bottom: 30px;">
        <p style="color: #666; font-size: 16px; margin-bottom: 10px;">
            Klicken Sie auf die Karte, um die Übersetzung zu sehen.
        </p>
        <p style="color: #0066cc; font-size: 14px; font-weight: 500;">
            💡 <strong>Wischen:</strong> Nach rechts für "Gewusst", nach links für "Wiederholen"
        </p>
    </div>
    
    {% if vokabeln %}
    <!-- Flashcard Stack Container -->
    <div class="flashcard-stack" id="flashcard-stack">
        {% for i in range(vokabeln|length) %}
        <div class="flashcard" data-index="{{ i }}" style="{% if i > 2 %}display: none;{% endif %}">
            <div class="swipe-indicator right">✅</div>
            <div class="swipe-indicator left">🔄</div>
            
            <div class="flashcard-content">
                <div class="german-side">
                    <div class="flashcard-word">{{ vokabeln[i].deutsch }}</div>
                    <div class="flashcard-hint">Tippen für Übersetzung</div>
                </div>
                
                <div class="spanish-side hidden">
                    <div class="flashcard-word" style="color: #0066cc;">{{ vokabeln[i].spanisch }}</div>
                    <div class="flashcard-translation">{{ vokabeln[i].deutsch }}</div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Card Counter -->
    <div style="text-align: center; margin: 20px 0;">
        <span id="card-counter" style="font-size: 14px; color: #666;">
            Karte <span id="current-card">1</span> von {{ vokabeln|length }}
        </span>
    </div>
    
    <!-- Action Buttons -->
    <div style="text-align: center; margin: 30px 0;">
        <div class="flex flex-center gap-20">
            <button id="know-btn" class="btn btn-success" style="padding: 15px 25px;">
                ✅ Gewusst
            </button>
            <button id="review-btn" class="btn btn-warning" style="padding: 15px 25px;">
                🔄 Wiederholen
            </button>
            <button id="skip-btn" class="btn btn-outline" style="padding: 15px 25px;">
                ⏭️ Überspringen
            </button>
        </div>
    </div>
    
    <!-- Progress Stats -->
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-top: 30px;">
        <h4 style="text-align: center; margin-bottom: 20px; color: #333;">Lernfortschritt</h4>
        <div class="grid grid-3">
            <div class="text-center">
                <div id="known-count" style="font-size: 24px; font-weight: 600; color: #28a745;">0</div>
                <div class="text-small text-muted">Gelernt</div>
            </div>
            <div class="text-center">
                <div id="review-count" style="font-size: 24px; font-weight: 600; color: #ffc107;">0</div>
                <div class="text-small text-muted">Wiederholen</div>
            </div>
            <div class="text-center">
                <div id="remaining-count" style="font-size: 24px; font-weight: 600; color: #6c757d;">{{ vokabeln|length }}</div>
                <div class="text-small text-muted">Übrig</div>
            </div>
        </div>
    </div>
    
    {% else %}
    <div class="alert alert-info text-center">
        <strong>Keine Vokabeln verfügbar</strong><br>
        Dieses Kapitel enthält noch keine Vokabeln zum Lernen.
    </div>
    {% endif %}
    
    <!-- Navigation -->
    <div style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 1px solid #e0e0e0;">
        <a href="{{ url_for('chapter_overview') }}" class="btn btn-outline mr-10">
            Zurück zur Übersicht
        </a>
        <a href="{{ url_for('quiz') }}" class="btn btn-secondary mr-10">
            Zum Schreibquiz
        </a>
        <a href="{{ url_for('review_words') }}" class="btn btn-warning">
            🔄 Wiederholen ({{ review_count if review_count else 0 }})
        </a>
    </div>
</div>

<script>
let currentCardIndex = 0;
let totalCards = {{ vokabeln|length }};
let knownCount = 0;
let reviewCount = 0;
let isFlipped = false;

// Touch/Swipe variables
let startX = 0;
let startY = 0;
let currentX = 0;
let currentY = 0;
let isDragging = false;
let currentCard = null;

// Initialize flashcards
document.addEventListener('DOMContentLoaded', function() {
    updateCardVisibility();
    updateStats();
    
    // Add touch event listeners to all cards
    document.querySelectorAll('.flashcard').forEach(card => {
        // Mouse/Touch events for dragging
        card.addEventListener('mousedown', handleStart);
        card.addEventListener('touchstart', handleStart, { passive: false });
        
        // Click for flip functionality
        card.addEventListener('click', function(e) {
            // Only flip if not dragging
            if (!isDragging && this.dataset.index == currentCardIndex) {
                flipCard();
            }
        });
    });
    
    // Global mouse/touch events
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('touchmove', handleMove, { passive: false });
    document.addEventListener('mouseup', handleEnd);
    document.addEventListener('touchend', handleEnd);
    
    // Button event listeners
    document.getElementById('know-btn').addEventListener('click', function() {
        markCard('known');
    });
    
    document.getElementById('review-btn').addEventListener('click', function() {
        markCard('review');
    });
    
    document.getElementById('skip-btn').addEventListener('click', function() {
        nextCard();
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === ' ') {
            e.preventDefault();
            flipCard();
        } else if (e.key === '1') {
            markCard('known');
        } else if (e.key === '2') {
            markCard('review');
        } else if (e.key === '3') {
            nextCard();
        } else if (e.key === 'ArrowRight') {
            markCard('known');
        } else if (e.key === 'ArrowLeft') {
            markCard('review');
        }
    });
});

function handleStart(e) {
    e.preventDefault();
    
    // Only handle the current top card
    if (this.dataset.index != currentCardIndex) return;
    
    currentCard = this;
    isDragging = false;
    
    const touch = e.touches ? e.touches[0] : e;
    startX = touch.clientX;
    startY = touch.clientY;
    currentX = startX;
    currentY = startY;
    
    currentCard.classList.add('dragging');
}

function handleMove(e) {
    if (!currentCard) return;
    
    e.preventDefault();
    const touch = e.touches ? e.touches[0] : e;
    currentX = touch.clientX;
    currentY = touch.clientY;
    
    const deltaX = currentX - startX;
    const deltaY = currentY - startY;
    
    // Start dragging if movement threshold is exceeded
    if (Math.abs(deltaX) > 10 || Math.abs(deltaY) > 10) {
        isDragging = true;
    }
    
    if (isDragging) {
        const rotation = deltaX * 0.1; // Slight rotation based on horizontal movement
        const threshold = 80; // Threshold for swipe indication
        
        // Apply transform
        currentCard.style.transform = `translateX(${deltaX}px) translateY(${deltaY}px) rotate(${rotation}deg)`;
        
        // Show swipe indicators
        const rightIndicator = currentCard.querySelector('.swipe-indicator.right');
        const leftIndicator = currentCard.querySelector('.swipe-indicator.left');
        
        if (deltaX > threshold) {
            // Swiping right (known)
            currentCard.classList.add('swiping-right');
            currentCard.classList.remove('swiping-left');
            rightIndicator.classList.add('visible');
            leftIndicator.classList.remove('visible');
        } else if (deltaX < -threshold) {
            // Swiping left (review)
            currentCard.classList.add('swiping-left');
            currentCard.classList.remove('swiping-right');
            leftIndicator.classList.add('visible');
            rightIndicator.classList.remove('visible');
        } else {
            // Neutral zone
            currentCard.classList.remove('swiping-right', 'swiping-left');
            rightIndicator.classList.remove('visible');
            leftIndicator.classList.remove('visible');
        }
    }
}

function handleEnd(e) {
    if (!currentCard) return;
    
    const deltaX = currentX - startX;
    const swipeThreshold = 120; // Minimum distance for a swipe action
    
    if (isDragging && Math.abs(deltaX) > swipeThreshold) {
        // Perform swipe action
        if (deltaX > 0) {
            // Swiped right - known
            animateCardExit(currentCard, 'right');
            markCard('known');
        } else {
            // Swiped left - review
            animateCardExit(currentCard, 'left');
            markCard('review');
        }
    } else {
        // Return to original position
        currentCard.style.transform = '';
        currentCard.classList.remove('swiping-right', 'swiping-left');
        const indicators = currentCard.querySelectorAll('.swipe-indicator');
        indicators.forEach(indicator => indicator.classList.remove('visible'));
    }
    
    // Reset state
    currentCard.classList.remove('dragging');
    currentCard = null;
    isDragging = false;
}

function animateCardExit(card, direction) {
    const exitX = direction === 'right' ? window.innerWidth : -window.innerWidth;
    card.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
    card.style.transform = `translateX(${exitX}px) rotate(${direction === 'right' ? 30 : -30}deg)`;
    card.style.opacity = '0';
    
    setTimeout(() => {
        card.style.display = 'none';
    }, 300);
}

function updateCardVisibility() {
    const cards = document.querySelectorAll('.flashcard');
    cards.forEach((card, index) => {
        const cardIndex = parseInt(card.dataset.index);
        if (cardIndex < currentCardIndex) {
            card.style.display = 'none';
        } else if (cardIndex === currentCardIndex) {
            card.style.transform = 'translateY(0px) scale(1)';
            card.style.zIndex = '3';
            card.style.display = 'flex';
            card.style.opacity = '1';
        } else if (cardIndex === currentCardIndex + 1) {
            card.style.transform = 'translateY(6px) scale(0.97)';
            card.style.zIndex = '2';
            card.style.display = 'flex';
            card.style.opacity = '0.9';
        } else if (cardIndex === currentCardIndex + 2) {
            card.style.transform = 'translateY(12px) scale(0.94)';
            card.style.zIndex = '1';
            card.style.display = 'flex';
            card.style.opacity = '0.8';
        } else {
            card.style.display = 'none';
        }
    });
    
    document.getElementById('current-card').textContent = currentCardIndex + 1;
}

function flipCard() {
    const currentCardElement = document.querySelector(`[data-index="${currentCardIndex}"]`);
    if (currentCardElement) {
        const germanSide = currentCardElement.querySelector('.german-side');
        const spanishSide = currentCardElement.querySelector('.spanish-side');
        
        if (!isFlipped) {
            germanSide.classList.add('hidden');
            spanishSide.classList.remove('hidden');
            currentCardElement.classList.add('flipped');
            isFlipped = true;
        } else {
            germanSide.classList.remove('hidden');
            spanishSide.classList.add('hidden');
            currentCardElement.classList.remove('flipped');
            isFlipped = false;
        }
    }
}

function markCard(action) {
    const vocabIndex = currentCardIndex;
    
    // Send to server
    fetch('/flashcard_action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `action=${action}&vocab_index=${vocabIndex}`
    });
    
    // Update local counts
    if (action === 'known') {
        knownCount++;
    } else if (action === 'review') {
        reviewCount++;
    }
    
    updateStats();
    nextCard();
}

function nextCard() {
    if (currentCardIndex < totalCards - 1) {
        currentCardIndex++;
        isFlipped = false;
        updateCardVisibility();
    } else {
        // All cards completed
        const message = `Alle Karteikarten durchgegangen! 🎉\n\nErgebnis:\n✅ ${knownCount} gelernt\n🔄 ${reviewCount} zum Wiederholen`;
        alert(message);
        
        // Redirect to review section if there are cards to review
        if (reviewCount > 0) {
            if (confirm('Möchten Sie jetzt die Karten zum Wiederholen ansehen?')) {
                window.location.href = '{{ url_for("review_words") }}';
            }
        }
    }
}

function updateStats() {
    document.getElementById('known-count').textContent = knownCount;
    document.getElementById('review-count').textContent = reviewCount;
    document.getElementById('remaining-count').textContent = Math.max(0, totalCards - currentCardIndex - 1);
}
</script>
{% endblock %}