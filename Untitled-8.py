templates/admin.html
{% extends "base.html" %}

{% block title %}Admin Panel - Spanisch Trainer{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>
                <i class="fas fa-cog me-2"></i>
                Admin Panel
            </h2>
            <span class="badge bg-danger fs-6">Administrator</span>
        </div>
    </div>
</div>

<!-- Statistics Row -->
<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="card bg-primary text-white shadow">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">Kapitel</h6>
                        <h3 class="mb-0">{{ chapters|length }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-book fa-2x opacity-75"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-success text-white shadow">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">Vokabeln</h6>
                        <h3 class="mb-0">{{ total_vocabulary }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-language fa-2x opacity-75"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-info text-white shadow">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">Benutzer</h6>
                        <h3 class="mb-0">{{ total_users }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-users fa-2x opacity-75"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card bg-warning text-dark shadow">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">Gesamt Benutzer</h6>
                        <h3 class="mb-0">{{ users|length }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-user-friends fa-2x opacity-75"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Chapter and Vocabulary Management -->
<div class="row g-4">
    <!-- Add New Chapter -->
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-plus me-2"></i>
                    Neues Kapitel erstellen
                </h4>
            </div>
            <div class="card-body">
                <form method="post">
                    <input type="hidden" name="action" value="add_chapter">
                    
                    <div class="mb-3">
                        <label for="chapter_name" class="form-label">
                            <i class="fas fa-book me-1"></i>
                            <strong>Kapitelname</strong>
                        </label>
                        <input type="text" class="form-control" id="chapter_name" name="chapter_name" 
                               placeholder="z.B. Kapitel 4 - Farben" required maxlength="128">
                    </div>
                    
                    <div class="mb-3">
                        <label for="chapter_description" class="form-label">
                            <i class="fas fa-align-left me-1"></i>
                            Beschreibung (optional)
                        </label>
                        <textarea class="form-control" id="chapter_description" name="chapter_description" 
                                  rows="2" placeholder="Kurze Beschreibung des Kapitels..."></textarea>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-plus me-2"></i>
                            Kapitel erstellen
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <!-- Add New Vocabulary -->
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-success text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-plus me-2"></i>
                    Neue Vokabel hinzufügen
                </h4>
            </div>
            <div class="card-body">
                {% if chapters %}
                <form method="post">
                    <input type="hidden" name="action" value="add_vocabulary">
                    
                    <div class="mb-3">
                        <label for="chapter_id" class="form-label">
                            <i class="fas fa-book me-1"></i>
                            <strong>Kapitel auswählen</strong>
                        </label>
                        <select class="form-select" id="chapter_id" name="chapter_id" required>
                            <option value="">-- Kapitel wählen --</option>
                            {% for chapter in chapters %}
                            <option value="{{ chapter.id }}">{{ chapter.name }} ({{ chapter.vocabularies|length }} Vokabeln)</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="deutsch" class="form-label">
                            <i class="fas fa-flag me-1"></i>
                            <strong>Deutsches Wort</strong>
                        </label>
                        <input type="text" class="form-control" id="deutsch" name="deutsch" 
                               placeholder="z.B. Freundschaft" required maxlength="256">
                    </div>
                    
                    <div class="mb-3">
                        <label for="spanisch" class="form-label">
                            <i class="fas fa-flag me-1" style="color: #C8102E;"></i>
                            <strong>Spanische Übersetzung</strong>
                        </label>
                        <input type="text" class="form-control" id="spanisch" name="spanisch" 
                               placeholder="z.B. Amistad" required maxlength="256">
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-plus me-2"></i>
                            Vokabel hinzufügen
                        </button>
                    </div>
                </form>
                {% else %}
                <div class="alert alert-warning text-center" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Erst Kapitel erstellen!</strong>
                    <p class="mb-0 mt-2">Erstellen Sie zuerst ein Kapitel, bevor Sie Vokabeln hinzufügen können.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<!-- Chapters Management -->
{% if chapters %}
<div class="row mt-4">
    <div class="col-12">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-book me-2"></i>
                    Kapitel-Übersicht ({{ chapters|length }})
                </h4>
            </div>
            <div class="card-body">
                <div class="accordion" id="chaptersAccordion">
                    {% for chapter in chapters %}
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading{{ chapter.id }}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                    data-bs-target="#collapse{{ chapter.id }}" aria-expanded="false" 
                                    aria-controls="collapse{{ chapter.id }}">
                                <div class="d-flex justify-content-between w-100 me-3">
                                    <span>
                                        <i class="fas fa-book me-2"></i>
                                        <strong>{{ chapter.name }}</strong>
                                    </span>
                                    <span class="badge bg-primary">{{ chapter.vocabularies|length }} Vokabeln</span>
                                </div>
                            </button>
                        </h2>
                        <div id="collapse{{ chapter.id }}" class="accordion-collapse collapse" 
                             aria-labelledby="heading{{ chapter.id }}" data-bs-parent="#chaptersAccordion">
                            <div class="accordion-body">
                                {% if chapter.description %}
                                <p class="text-muted mb-3">{{ chapter.description }}</p>
                                {% endif %}
                                
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <span class="text-muted">Erstellt: {{ chapter.created_at.strftime('%d.%m.%Y %H:%M') }}</span>
                                    <form method="post" style="display: inline;" 
                                          onsubmit="return confirm('Kapitel \"{{ chapter.name }}\" und ALLE zugehörigen Vokabeln wirklich löschen?')">
                                        <input type="hidden" name="action" value="delete_chapter">
                                        <input type="hidden" name="chapter_id" value="{{ chapter.id }}">
                                        <button type="submit" class="btn btn-sm btn-outline-danger">
                                            <i class="fas fa-trash me-1"></i>
                                            Kapitel löschen
                                        </button>
                                    </form>
                                </div>
                                
                                {% if chapter.vocabularies %}
                                <div class="table-responsive">
                                    <table class="table table-striped table-sm">
                                        <thead>
                                            <tr>
                                                <th><i class="fas fa-flag me-1"></i> Deutsch</th>
                                                <th><i class="fas fa-flag me-1" style="color: #C8102E;"></i> Spanisch</th>
                                                <th width="100">Aktionen</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {% for vocab in chapter.vocabularies %}
                                            <tr>
                                                <td><strong>{{ vocab.deutsch }}</strong></td>
                                                <td>{{ vocab.spanisch }}</td>
                                                <td>
                                                    <form method="post" style="display: inline;" 
                                                          onsubmit="return confirm('Vokabel \"{{ vocab.deutsch }}\" wirklich löschen?')">
                                                        <input type="hidden" name="action" value="delete_vocabulary">
                                                        <input type="hidden" name="vocab_id" value="{{ vocab.id }}">
                                                        <button type="submit" class="btn btn-sm btn-outline-danger">
                                                            <i class="fas fa-trash"></i>
                                                        </button>
                                                    </form>
                                                </td>
                                            </tr>
                                            {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                                {% else %}
                                <div class="alert alert-info text-center" role="alert">
                                    <i class="fas fa-info-circle me-2"></i>
                                    Dieses Kapitel enthält noch keine Vokabeln.
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="row mt-4">
    <div class="col-12">
        <div class="alert alert-warning text-center" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Keine Kapitel vorhanden!</strong>
            <p class="mb-0 mt-2">Erstellen Sie das erste Kapitel, um mit der Verwaltung zu beginnen.</p>
        </div>
    </div>
</div>
{% endif %}

<!-- User Management -->
<div class="row g-4 mt-2">
    <div class="col-12">
        <div class="card shadow">
            <div class="card-header bg-info text-white">
                <h4 class="card-title mb-0">
                    <i class="fas fa-users me-2"></i>
                    Registrierte Benutzer ({{ users|length }})
                </h4>
            </div>
            <div class="card-body">
                {% if users %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th><i class="fas fa-user me-1"></i> Benutzername</th>
                                <th><i class="fas fa-envelope me-1"></i> E-Mail</th>
                                <th><i class="fas fa-id-badge me-1"></i> ID</th>
                                <th><i class="fas fa-shield-alt me-1"></i> Rolle</th>
                                <th><i class="fas fa-calendar me-1"></i> Thema</th>
                                <th>Aktionen</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for user in users %}
                            <tr>
                                <td>
                                    <strong>{{ user.username }}</strong>
                                    {% if user.is_admin %}
                                    <span class="badge bg-danger ms-1">Admin</span>
                                    {% endif %}
                                </td>
                                <td>{{ user.email or 'Nicht angegeben' }}</td>
                                <td>{{ user.id }}</td>
                                <td>
                                    {% if user.is_admin %}
                                    <span class="text-danger"><i class="fas fa-crown me-1"></i>Administrator</span>
                                    {% else %}
                                    <span class="text-muted"><i class="fas fa-user me-1"></i>Benutzer</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <span class="badge bg-{{ 'dark' if user.theme_preference == 'dark' else 'light' }}">
                                        <i class="fas fa-{{ 'moon' if user.theme_preference == 'dark' else 'sun' }} me-1"></i>
                                        {{ user.theme_preference|title }}
                                    </span>
                                </td>
                                <td>
                                    {% if not user.is_admin %}
                                    <form method="post" style="display: inline;" 
                                          onsubmit="return confirm('Benutzer \"{{ user.username }}\" wirklich löschen?')">
                                        <input type="hidden" name="action" value="delete_user">
                                        <input type="hidden" name="user_id" value="{{ user.id }}">
                                        <button type="submit" class="btn btn-sm btn-outline-danger">
                                            <i class="fas fa-trash"></i> Löschen
                                        </button>
                                    </form>
                                    {% else %}
                                    <span class="text-muted">Geschützt</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="alert alert-warning text-center" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Keine Benutzer gefunden!</strong>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12 text-center">
        <a href="{{ url_for('index') }}" class="btn btn-outline-secondary me-2">
            <i class="fas fa-arrow-left me-1"></i>
            Zurück zum Dashboard
        </a>
        <a href="{{ url_for('logout') }}" class="btn btn-outline-primary">
            <i class="fas fa-sign-out-alt me-1"></i>
            Abmelden
        </a>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Auto-focus on first input
    document.addEventListener('DOMContentLoaded', function() {
        const chapterNameInput = document.getElementById('chapter_name');
        if (chapterNameInput) {
            chapterNameInput.focus();
        }
    });
    
    // Enter key to move between fields in chapter form
    document.getElementById('chapter_name')?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('chapter_description').focus();
        }
    });
    
    // Enter key to move between fields in vocabulary form
    document.getElementById('chapter_id')?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('deutsch').focus();
        }
    });
    
    document.getElementById('deutsch')?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('spanisch').focus();
        }
    });
    
    // Auto-select chapter if only one exists
    document.addEventListener('DOMContentLoaded', function() {
        const chapterSelect = document.getElementById('chapter_id');
        if (chapterSelect && chapterSelect.options.length === 2) { // 1 default + 1 chapter
            chapterSelect.selectedIndex = 1;
        }
    });
</script>
{% endblock %}