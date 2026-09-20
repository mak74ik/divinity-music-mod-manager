/* =========================================================
   Divinity Music Mod Manager - Client Logic
   Windows 11 Minimalist Fluent Design
   Multi-Language Engine (EN, RU, PL, IT, DE, FR, ES)
   ========================================================= */

// Multi-Language Translations Dictionary
const I18N = {
  en: {
    tabTracks: "Tracks",
    tabQuickFill: "Quick Fill",
    tabInfo: "About & Info",
    searchPlaceholder: "Search track or scene...",
    allTracks: "All Tracks",
    allTracksDesc: "All 106 in-game music tracks. Default tracks retain original audio.",
    quickFillCatBtn: "Fill Category",
    colScene: "Scene / Target",
    colStatus: "Status",
    colAudio: "Assigned Audio",
    colActions: "Actions",
    statusOriginal: "Original",
    statusCustom: "Custom",
    btnReplace: "Replace",
    btnResetAll: "Reset All",
    statModified: "Replaced:",
    statOriginal: "Original:",
    btnBuild: "Build & Save Mod",
    btnApply: "Apply to All Tracks",
    btnCancel: "Cancel",
    btnOpenFolder: "Open Folder",
    btnClose: "Done",
    qfHeroTitle: "Batch Category Assignment",
    qfHeroDesc: "Quickly assign a single audio track to an entire category (e.g. all Combat tracks or Taverns):",
    qfDropzoneText: "Click to select MP3 or drag file here",
    qfModalPrompt: "Select an MP3 file to apply to all tracks in this category:",
    qfTracksCount: "tracks in category",
    qfFillCategory: "Fill this category",
    infoAuthorRole: "Mod Creator & Audio Designer",
    infoIntro: "Creator of modifications for Divinity: Original Sin Enhanced Edition, including the Baldur's Gate 3 Music Overhaul.",
    infoNexusLink: "Nexus Mods Profile",
    infoGithubLink: "GitHub Profile",
    infoGuideTitle: "How it works:",
    infoGuide1: "<strong>Simplicity:</strong> Provide standard MP3 audio files. The program converts them into engine-native Wwise Vorbis with EBU R128 loudness normalization.",
    infoGuide2: "<strong>Partial Replacement:</strong> You only need to replace the tracks you want. All empty/unmodified slots automatically keep their original game music.",
    infoGuide3: "<strong>Installation:</strong> Place the generated <code>z_Custom_Music.pak</code> into your game's <code>Data</code> folder.",
    infoGuide4: "<strong>Uninstallation:</strong> Delete <code>z_Custom_Music.pak</code> from your <code>Data</code> folder. Original game files remain completely untouched.",
    buildModalTitle: "Building Divinity Mod",
    buildPreparing: "Preparing files for conversion...",
    buildPacking: "Packing LSPK archive...",
    buildDone: "Mod successfully built and saved!",
    buildError: "Error during build:",
    resetConfirm: "Are you sure you want to reset all customized tracks back to original audio?",
    noTracksSelected: "Please select at least one audio file to replace before building!"
  },
  ru: {
    tabTracks: "Треки",
    tabQuickFill: "Быстрое заполнение",
    tabInfo: "Об авторе & Инфо",
    searchPlaceholder: "Поиск трека или сцены...",
    allTracks: "Все треки",
    allTracksDesc: "Все 106 треков игры. По умолчанию слоты играют оригинальную музыку.",
    quickFillCatBtn: "Заполнить категорию",
    colScene: "Сцена / Слот",
    colStatus: "Статус",
    colAudio: "Назначенное аудио",
    colActions: "Действия",
    statusOriginal: "Оригинал",
    statusCustom: "Заменено",
    btnReplace: "Заменить",
    btnResetAll: "Сбросить всё",
    statModified: "Заменено:",
    statOriginal: "Оригинал:",
    btnBuild: "Собрать всё воедино и сохранить",
    btnApply: "Применить ко всем трекам",
    btnCancel: "Отмена",
    btnOpenFolder: "Открыть папку",
    btnClose: "Готово",
    qfHeroTitle: "Пакетная замена по категориям",
    qfHeroDesc: "Быстро назначьте один аудиофайл на всю категорию (например, на все битвы или таверны):",
    qfDropzoneText: "Нажмите для выбора MP3 или перетащите файл сюда",
    qfModalPrompt: "Выберите MP3 файл, который будет играть во всех треках категории:",
    qfTracksCount: "треков в категории",
    qfFillCategory: "Заполнить эту категорию",
    infoAuthorRole: "Создатель модов и аудио-дизайнер",
    infoIntro: "Создатель модификаций для Divinity: Original Sin Enhanced Edition, включая саундтрек-мод Baldur's Gate 3 Music Overhaul.",
    infoNexusLink: "Профиль на Nexus Mods",
    infoGithubLink: "GitHub Репозиторий",
    infoGuideTitle: "Как работает программа:",
    infoGuide1: "<strong>Простота:</strong> Приложение принимает обычные MP3 файлы и кодирует их в нативный формат движка Wwise с нормализацией EBU R128.",
    infoGuide2: "<strong>Частичная замена:</strong> Замените хоть один трек — все остальные автоматически сохранят оригинальную музыку из игры.",
    infoGuide3: "<strong>Установка:</strong> Положите созданный <code>z_Custom_Music.pak</code> в папку <code>Data</code> игры.",
    infoGuide4: "<strong>Удаление:</strong> Просто удалите <code>z_Custom_Music.pak</code> из папки <code>Data</code>. Исходные файлы игры не затрагиваются.",
    buildModalTitle: "Сборка мода Divinity",
    buildPreparing: "Подготовка файлов к конвертации...",
    buildPacking: "Сборка архива LSPK...",
    buildDone: "Мод успешно собран и сохранён!",
    buildError: "Ошибка при сборке:",
    resetConfirm: "Вы уверены, что хотите сбросить все замены и вернуть оригинальную музыку?",
    noTracksSelected: "Выберите хотя бы один файл для замены перед сборкой!"
  },
  pl: {
    tabTracks: "Utwory",
    tabQuickFill: "Szybkie wypełnianie",
    tabInfo: "O autorze",
    searchPlaceholder: "Szukaj utworu...",
    allTracks: "Wszystkie utwory",
    allTracksDesc: "Wszystkie 106 utworów. Domyślne zachowują oryginalną muzykę.",
    quickFillCatBtn: "Wypełnij kategorię",
    colScene: "Scena / Cel",
    colStatus: "Status",
    colAudio: "Przypisane audio",
    colActions: "Akcje",
    statusOriginal: "Oryginał",
    statusCustom: "Własny",
    btnReplace: "Zmień",
    btnResetAll: "Resetuj wszystko",
    statModified: "Zmienione:",
    statOriginal: "Oryginalne:",
    btnBuild: "Zbuduj i zapisz mod",
    btnApply: "Zastosuj do wszystkich",
    btnCancel: "Anuluj",
    btnOpenFolder: "Otwórz folder",
    btnClose: "Gotowe",
    qfHeroTitle: "Zbiorcze przypisywanie kategorii",
    qfHeroDesc: "Szybko przypisz jeden plik audio do całej kategorii:",
    qfDropzoneText: "Kliknij, aby wybrać MP3 lub przeciągnij plik tutaj",
    qfModalPrompt: "Wybierz plik MP3 do zastosowania we wszystkich utworach:",
    qfTracksCount: "utworów w kategorii",
    qfFillCategory: "Wypełnij tę kategorię",
    infoAuthorRole: "Twórca modów",
    infoIntro: "Autor modyfikacji do Divinity: Original Sin EE (m.in. Baldur's Gate 3 Music Overhaul).",
    infoNexusLink: "Profil Nexus Mods",
    infoGithubLink: "Profil GitHub",
    infoGuideTitle: "Jak to działa:",
    infoGuide1: "<strong>Prostota:</strong> Używaj zwykłych plików MP3.",
    infoGuide2: "<strong>Częściowa zamiana:</strong> Niezmienione utwory zachowują oryginalną muzykę.",
    infoGuide3: "<strong>Instalacja:</strong> Skopiuj <code>z_Custom_Music.pak</code> do folderu <code>Data</code>.",
    infoGuide4: "<strong>Odinstalowanie:</strong> Usuń plik <code>z_Custom_Music.pak</code>.",
    buildModalTitle: "Kompilacja moda",
    buildPreparing: "Przygotowanie plików...",
    buildPacking: "Pakowanie archiwum LSPK...",
    buildDone: "Mod pomyślnie utworzony!",
    buildError: "Błąd podczas budowania:",
    resetConfirm: "Czy na pewno chcesz zresetować wszystkie zmiany?",
    noTracksSelected: "Wybierz przynajmniej jeden plik przed kompilacją!"
  },
  it: {
    tabTracks: "Brani",
    tabQuickFill: "Riempimento rapido",
    tabInfo: "Informazioni",
    searchPlaceholder: "Cerca brano...",
    allTracks: "Tutti i brani",
    allTracksDesc: "Tutti i 106 brani di gioco. I brani predefiniti mantengono l'audio originale.",
    quickFillCatBtn: "Riempi categoria",
    colScene: "Scena / Destinazione",
    colStatus: "Stato",
    colAudio: "Audio assegnato",
    colActions: "Azioni",
    statusOriginal: "Originale",
    statusCustom: "Personalizzato",
    btnReplace: "Sostituisci",
    btnResetAll: "Ripristina tutto",
    statModified: "Sostituiti:",
    statOriginal: "Originali:",
    btnBuild: "Compila e salva mod",
    btnApply: "Applica a tutti",
    btnCancel: "Annulla",
    btnOpenFolder: "Apri cartella",
    btnClose: "Fatto",
    qfHeroTitle: "Assegnazione in blocco per categoria",
    qfHeroDesc: "Assegna rapidamente un file audio a un'intera categoria:",
    qfDropzoneText: "Fai clic per selezionare MP3 o trascina il file qui",
    qfModalPrompt: "Seleziona un file MP3 per tutti i brani della categoria:",
    qfTracksCount: "brani nella categoria",
    qfFillCategory: "Riempi questa categoria",
    infoAuthorRole: "Creatore di mod",
    infoIntro: "Creatore di mod per Divinity: Original Sin EE.",
    infoNexusLink: "Profilo Nexus Mods",
    infoGithubLink: "Profilo GitHub",
    infoGuideTitle: "Come funziona:",
    infoGuide1: "<strong>Semplicità:</strong> Usa normali file MP3.",
    infoGuide2: "<strong>Sostituzione parziale:</strong> I brani non modificati mantengono l'audio originale.",
    infoGuide3: "<strong>Installazione:</strong> Inserisci <code>z_Custom_Music.pak</code> nella cartella <code>Data</code>.",
    infoGuide4: "<strong>Disinstallazione:</strong> Elimina il file <code>z_Custom_Music.pak</code>.",
    buildModalTitle: "Compilazione mod",
    buildPreparing: "Preparazione dei file...",
    buildPacking: "Creazione archivio LSPK...",
    buildDone: "Mod compilata con successo!",
    buildError: "Errore durante la compilazione:",
    resetConfirm: "Sei sicuro di voler ripristinare tutti i brani all'originale?",
    noTracksSelected: "Seleziona almeno un brano da sostituire!"
  },
  de: {
    tabTracks: "Titel",
    tabQuickFill: "Schnell füllen",
    tabInfo: "Über & Info",
    searchPlaceholder: "Titel suchen...",
    allTracks: "Alle Titel",
    allTracksDesc: "Alle 106 Spielemusiktitel. Standardtitel behalten die Originalmusik.",
    quickFillCatBtn: "Kategorie füllen",
    colScene: "Szene / Ziel",
    colStatus: "Status",
    colAudio: "Zugewiesenes Audio",
    colActions: "Aktionen",
    statusOriginal: "Original",
    statusCustom: "Benutzerdefiniert",
    btnReplace: "Ersetzen",
    btnResetAll: "Alles zurücksetzen",
    statModified: "Ersetzt:",
    statOriginal: "Original:",
    btnBuild: "Mod erstellen & speichern",
    btnApply: "Auf alle anwenden",
    btnCancel: "Abbrechen",
    btnOpenFolder: "Ordner öffnen",
    btnClose: "Fertig",
    qfHeroTitle: "Kategorie-Stapelzuweisung",
    qfHeroDesc: "Weisen Sie einer ganzen Kategorie schnell eine Audiodatei zu:",
    qfDropzoneText: "Klicken Sie, um MP3 auszuwählen, oder ziehen Sie Datei hierher",
    qfModalPrompt: "Wählen Sie eine MP3 für alle Titel in dieser Kategorie:",
    qfTracksCount: "Titel in Kategorie",
    qfFillCategory: "Diese Kategorie füllen",
    infoAuthorRole: "Mod-Entwickler",
    infoIntro: "Entwickler von Modifikationen für Divinity: Original Sin EE.",
    infoNexusLink: "Nexus Mods Profil",
    infoGithubLink: "GitHub Profil",
    infoGuideTitle: "So funktioniert es:",
    infoGuide1: "<strong>Einfachheit:</strong> Verwenden Sie standardmäßige MP3-Dateien.",
    infoGuide2: "<strong>Teilweiser Ersatz:</strong> Unveränderte Titel behalten Originalton.",
    infoGuide3: "<strong>Installation:</strong> <code>z_Custom_Music.pak</code> in <code>Data</code> einfügen.",
    infoGuide4: "<strong>Deinstallation:</strong> <code>z_Custom_Music.pak</code> löschen.",
    buildModalTitle: "Mod erstellen",
    buildPreparing: "Dateien vorbereiten...",
    buildPacking: "LSPK-Archiv wird gepackt...",
    buildDone: "Mod erfolgreich erstellt!",
    buildError: "Fehler beim Erstellen:",
    resetConfirm: "Möchten Sie wirklich alle Anpassungen zurücksetzen?",
    noTracksSelected: "Bitte wählen Sie vor dem Erstellen mindestens eine Datei aus!"
  },
  fr: {
    tabTracks: "Titres",
    tabQuickFill: "Remplissage rapide",
    tabInfo: "À propos",
    searchPlaceholder: "Rechercher...",
    allTracks: "Tous les titres",
    allTracksDesc: "Les 106 pistes audio du jeu. Les pistes par défaut conservent la musique originale.",
    quickFillCatBtn: "Remplir catégorie",
    colScene: "Scène / Cible",
    colStatus: "Statut",
    colAudio: "Audio assigné",
    colActions: "Actions",
    statusOriginal: "Original",
    statusCustom: "Modifié",
    btnReplace: "Remplacer",
    btnResetAll: "Tout réinitialiser",
    statModified: "Modifiés :",
    statOriginal: "Originaux :",
    btnBuild: "Compiler & Enregistrer",
    btnApply: "Appliquer à tous",
    btnCancel: "Annuler",
    btnOpenFolder: "Ouvrir dossier",
    btnClose: "Terminé",
    qfHeroTitle: "Attribution par catégorie",
    qfHeroDesc: "Attribuez rapidement un fichier audio à toute une catégorie :",
    qfDropzoneText: "Cliquez pour sélectionner un MP3 ou glissez le fichier ici",
    qfModalPrompt: "Sélectionnez un MP3 pour toute la catégorie :",
    qfTracksCount: "titres dans la catégorie",
    qfFillCategory: "Remplir cette catégorie",
    infoAuthorRole: "Créateur de mods",
    infoIntro: "Créateur de modifications pour Divinity: Original Sin EE.",
    infoNexusLink: "Profil Nexus Mods",
    infoGithubLink: "Profil GitHub",
    infoGuideTitle: "Fonctionnement :",
    infoGuide1: "<strong>Simplicité :</strong> Utilisez des fichiers MP3 standards.",
    infoGuide2: "<strong>Remplacement partiel :</strong> Les pistes non modifiées restent originales.",
    infoGuide3: "<strong>Installation :</strong> Placez <code>z_Custom_Music.pak</code> dans le dossier <code>Data</code>.",
    infoGuide4: "<strong>Désinstallation :</strong> Supprimez <code>z_Custom_Music.pak</code>.",
    buildModalTitle: "Création du mod",
    buildPreparing: "Préparation des fichiers...",
    buildPacking: "Compression de l'archive LSPK...",
    buildDone: "Mod compilé avec succès !",
    buildError: "Erreur lors de la compilation :",
    resetConfirm: "Voulez-vous réinitialiser toutes les pistes à l'original ?",
    noTracksSelected: "Sélectionnez au moins un fichier avant de compiler !"
  },
  es: {
    tabTracks: "Pistas",
    tabQuickFill: "Llenado rápido",
    tabInfo: "Acerca de",
    searchPlaceholder: "Buscar pista...",
    allTracks: "Todas las pistas",
    allTracksDesc: "Las 106 pistas de música del juego. Las pistas predeterminadas conservan el audio original.",
    quickFillCatBtn: "Llenar categoría",
    colScene: "Escena / Destino",
    colStatus: "Estado",
    colAudio: "Audio asignado",
    colActions: "Acciones",
    statusOriginal: "Original",
    statusCustom: "Personalizado",
    btnReplace: "Reemplazar",
    btnResetAll: "Restablecer todo",
    statModified: "Reemplazadas:",
    statOriginal: "Originales:",
    btnBuild: "Compilar y Guardar",
    btnApply: "Aplicar a todas",
    btnCancel: "Cancelar",
    btnOpenFolder: "Abrir carpeta",
    btnClose: "Listo",
    qfHeroTitle: "Asignación masiva por categoría",
    qfHeroDesc: "Asigna rápidamente un archivo de audio a toda una categoría:",
    qfDropzoneText: "Haz clic para seleccionar MP3 o arrastra el archivo aquí",
    qfModalPrompt: "Selecciona un MP3 para todas las pistas de esta categoría:",
    qfTracksCount: "pistas en la categoría",
    qfFillCategory: "Llenar esta categoría",
    infoAuthorRole: "Creador de mods",
    infoIntro: "Creador de modificaciones para Divinity: Original Sin EE.",
    infoNexusLink: "Perfil de Nexus Mods",
    infoGithubLink: "Perfil de GitHub",
    infoGuideTitle: "Cómo funciona:",
    infoGuide1: "<strong>Simplicidad:</strong> Usa archivos MP3 convencionales.",
    infoGuide2: "<strong>Reemplazo parcial:</strong> Las pistas sin modificar mantienen el audio original.",
    infoGuide3: "<strong>Instalación:</strong> Copia <code>z_Custom_Music.pak</code> a la carpeta <code>Data</code>.",
    infoGuide4: "<strong>Desinstalación:</strong> Elimina <code>z_Custom_Music.pak</code>.",
    buildModalTitle: "Compilación del mod",
    buildPreparing: "Preparando archivos...",
    buildPacking: "Empaquetando archivo LSPK...",
    buildDone: "¡Mod compilado con éxito!",
    buildError: "Error durante la compilación:",
    resetConfirm: "¿Estás seguro de que deseas restablecer todas las pistas?",
    noTracksSelected: "¡Selecciona al menos un archivo antes de compilar!"
  }
};

// State
let currentLang = localStorage.getItem('divinity_lang') || 'en';
let allTracks = [];
let categories = [];
let modifiedTracks = {}; // wid -> { filePath: string, fileName: string }
let currentCategory = 'all';
let searchQuery = '';
let activeQuickFillCat = null;
let currentPlayingWid = null;
let targetWidForFilePicker = null;

const globalAudio = document.getElementById('globalAudioPlayer');
const hiddenFileInput = document.getElementById('hiddenFileInput');

// Initialize
window.addEventListener('DOMContentLoaded', () => {
  initLanguage();
  initTabs();
  initSearch();
  initAudioEvents();
  initHiddenFileInput();

  if (window.pywebview && window.pywebview.api) {
    loadData();
  } else {
    window.addEventListener('pywebviewready', loadData);
  }
});

function t(key) {
  const langObj = I18N[currentLang] || I18N.en;
  return langObj[key] || I18N.en[key] || key;
}

function initLanguage() {
  const select = document.getElementById('langSelect');
  select.value = currentLang;
  select.addEventListener('change', (e) => {
    currentLang = e.target.value;
    localStorage.setItem('divinity_lang', currentLang);
    applyTranslations();
    renderCategories();
    renderTracks();
    renderQuickFillGrid();
  });
  applyTranslations();
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    el.innerHTML = t(key);
  });
  document.getElementById('searchInput').placeholder = t('searchPlaceholder');
}

function loadData() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_initial_data().then(data => {
      categories = data.categories || [];
      allTracks = data.tracks || [];
      renderCategories();
      renderTracks();
      renderQuickFillGrid();
      updateStats();
    }).catch(err => {
      console.error("Failed to load initial data:", err);
    });
  }
}

/* =========================================================
   Tabs Navigation
   ========================================================= */
function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const target = tab.dataset.tab;
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      const activePane = document.getElementById(`tab-${target}`);
      if (activePane) activePane.classList.add('active');
    });
  });
}

/* =========================================================
   Search
   ========================================================= */
function initSearch() {
  const input = document.getElementById('searchInput');
  const clearBtn = document.getElementById('clearSearch');

  input.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim().toLowerCase();
    clearBtn.style.display = searchQuery ? 'block' : 'none';
    renderTracks();
  });

  clearBtn.addEventListener('click', () => {
    input.value = '';
    searchQuery = '';
    clearBtn.style.display = 'none';
    renderTracks();
  });
}

/* =========================================================
   Categories Sidebar
   ========================================================= */
function getCategoryName(cat) {
  const key = `name_${currentLang}`;
  return cat[key] || cat.name_en || cat.id;
}

function renderCategories() {
  const bar = document.getElementById('categoriesBar');
  bar.innerHTML = '';

  // All tracks button
  const allBtn = document.createElement('button');
  allBtn.className = `cat-item ${currentCategory === 'all' ? 'active' : ''}`;
  allBtn.innerHTML = `
    <span>${t('allTracks')}</span>
    <span class="cat-badge">${allTracks.length}</span>
  `;
  allBtn.onclick = () => selectCategory('all');
  bar.appendChild(allBtn);

  // Category buttons
  categories.forEach(cat => {
    const catTracks = allTracks.filter(t => t.category === cat.id);
    const btn = document.createElement('button');
    btn.className = `cat-item ${currentCategory === cat.id ? 'active' : ''}`;
    btn.innerHTML = `
      <span>${getCategoryName(cat)}</span>
      <span class="cat-badge">${catTracks.length}</span>
    `;
    btn.onclick = () => selectCategory(cat.id);
    bar.appendChild(btn);
  });
}

function selectCategory(catId) {
  currentCategory = catId;
  renderCategories();

  const titleEl = document.getElementById('currentCatTitle');
  const descEl = document.getElementById('currentCatDesc');
  const quickFillBtn = document.getElementById('btnQuickFillCat');

  if (catId === 'all') {
    titleEl.textContent = t('allTracks');
    descEl.textContent = t('allTracksDesc');
    quickFillBtn.style.display = 'none';
  } else {
    const cat = categories.find(c => c.id === catId);
    titleEl.textContent = cat ? getCategoryName(cat) : 'Category';
    const descKey = `description_${currentLang}`;
    descEl.textContent = cat ? (cat[descKey] || cat.description_en || '') : '';
    quickFillBtn.style.display = 'inline-flex';
  }

  renderTracks();
}

/* =========================================================
   Structured Tracks Table Rendering (No Overlaps)
   ========================================================= */
function getTrackTitle(track) {
  if (currentLang === 'ru' && track.title_ru) return track.title_ru;
  return track.title_en || track.playlist || track.wid;
}

function renderTracks() {
  const list = document.getElementById('tracksList');
  list.innerHTML = '';

  let filtered = allTracks;
  if (currentCategory !== 'all') {
    filtered = filtered.filter(t => t.category === currentCategory);
  }

  if (searchQuery) {
    filtered = filtered.filter(t =>
      (t.title_ru && t.title_ru.toLowerCase().includes(searchQuery)) ||
      (t.title_en && t.title_en.toLowerCase().includes(searchQuery)) ||
      (t.playlist && t.playlist.toLowerCase().includes(searchQuery)) ||
      t.wid.includes(searchQuery)
    );
  }

  if (filtered.length === 0) {
    list.innerHTML = `
      <div style="padding: 40px; text-align: center; color: var(--text-muted); font-size: 13px;">
        No tracks found
      </div>
    `;
    return;
  }

  filtered.forEach((track, idx) => {
    const isModified = !!modifiedTracks[track.wid];
    const modData = modifiedTracks[track.wid];
    const isPlaying = currentPlayingWid === track.wid;

    const row = document.createElement('div');
    row.className = `track-row ${isModified ? 'modified' : ''}`;
    row.id = `row-${track.wid}`;

    const originalTitle = track.title_en || 'Original Soundtrack';
    const assignedDisplay = isModified
      ? `Custom: ${modData.fileName}`
      : `Original: ${originalTitle}`;

    row.innerHTML = `
      <div class="col-idx">${idx + 1}</div>
      <div class="col-scene">
        <span class="scene-title">${escapeHtml(getTrackTitle(track))}</span>
        <span class="scene-sub">${escapeHtml(track.playlist)} (${track.wid}.wem)</span>
      </div>
      <div class="col-status">
        <span class="badge-status ${isModified ? 'badge-modified' : 'badge-vanilla'}">
          ${isModified ? t('statusCustom') : t('statusOriginal')}
        </span>
      </div>
      <div class="col-audio" title="${escapeHtml(assignedDisplay)}">
        <i class="fa-solid ${isModified ? 'fa-file-audio' : 'fa-music'}" style="font-size: 13px; color: ${isModified ? 'var(--accent-text)' : 'var(--text-muted)'};"></i>
        <span class="audio-slot-text ${isModified ? 'is-custom' : ''}">${escapeHtml(assignedDisplay)}</span>
      </div>
      <div class="col-actions">
        <button class="btn-row" onclick="triggerFilePicker('${track.wid}', event)">
          <i class="fa-solid fa-folder-open"></i> ${t('btnReplace')}
        </button>
        ${isModified ? `
          <button class="btn-row btn-play ${isPlaying ? 'playing' : ''}" onclick="togglePreview('${track.wid}', event)" title="Play preview">
            <i class="fa-solid ${isPlaying ? 'fa-pause' : 'fa-play'}"></i>
          </button>
          <button class="btn-row btn-clear" onclick="resetTrack('${track.wid}', event)" title="Reset to original">
            <i class="fa-solid fa-xmark"></i>
          </button>
        ` : ''}
      </div>
    `;

    // HTML5 Drag and Drop events on the row
    row.addEventListener('dragover', (e) => {
      e.preventDefault();
      row.classList.add('drag-over');
    });

    row.addEventListener('dragleave', () => {
      row.classList.remove('drag-over');
    });

    row.addEventListener('drop', (e) => {
      e.preventDefault();
      row.classList.remove('drag-over');
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleDroppedFile(track.wid, e.dataTransfer.files[0]);
      }
    });

    list.appendChild(row);
  });
}

/* =========================================================
   Dual File Picker & Drag-and-Drop (100% Reliable)
   ========================================================= */
function initHiddenFileInput() {
  hiddenFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0 && targetWidForFilePicker) {
      handleDroppedFile(targetWidForFilePicker, e.target.files[0]);
    }
    hiddenFileInput.value = '';
  });
}

function triggerFilePicker(wid, e) {
  if (e) e.stopPropagation();
  targetWidForFilePicker = wid;

  // 1. Try PyWebView native dialog first
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.pick_audio_file().then(res => {
      if (res && res.filePath) {
        assignTrackFile(wid, res.filePath, res.fileName);
      } else {
        // Fallback to browser file input
        hiddenFileInput.click();
      }
    }).catch(() => {
      hiddenFileInput.click();
    });
  } else {
    hiddenFileInput.click();
  }
}

function handleDroppedFile(wid, file) {
  // If pywebview provided .path
  if (file.path) {
    assignTrackFile(wid, file.path, file.name);
    return;
  }

  // Otherwise read as base64 dataURL and upload to Python backend
  const reader = new FileReader();
  reader.onload = function(evt) {
    const dataUrl = evt.target.result;
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.upload_audio_file(wid, file.name, dataUrl).then(res => {
        if (res && res.filePath) {
          assignTrackFile(wid, res.filePath, res.fileName);
        }
      });
    }
  };
  reader.readAsDataURL(file);
}

function assignTrackFile(wid, filePath, fileName) {
  modifiedTracks[wid] = { filePath, fileName };
  updateStats();
  renderTracks();
}

function resetTrack(wid, e) {
  if (e) e.stopPropagation();
  if (currentPlayingWid === wid) {
    stopAudio();
  }
  delete modifiedTracks[wid];
  updateStats();
  renderTracks();
}

document.getElementById('btnResetAll').addEventListener('click', () => {
  if (Object.keys(modifiedTracks).length === 0) return;
  if (confirm(t('resetConfirm'))) {
    stopAudio();
    modifiedTracks = {};
    updateStats();
    renderTracks();
  }
});

function updateStats() {
  const modCount = Object.keys(modifiedTracks).length;
  const vanillaCount = allTracks.length - modCount;

  document.getElementById('statModified').textContent = modCount;
  document.getElementById('statVanilla').textContent = vanillaCount;

  const buildBtn = document.getElementById('btnBuildMod');
  buildBtn.disabled = modCount === 0;
}

/* =========================================================
   Audio Preview Player
   ========================================================= */
function togglePreview(wid, e) {
  if (e) e.stopPropagation();

  if (currentPlayingWid === wid) {
    stopAudio();
    renderTracks();
    return;
  }

  const modData = modifiedTracks[wid];
  if (!modData || !modData.filePath) return;

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_audio_data_url(modData.filePath).then(dataUrl => {
      if (dataUrl) {
        currentPlayingWid = wid;
        globalAudio.src = dataUrl;
        globalAudio.play();
        renderTracks();
      }
    }).catch(err => {
      console.error("Audio preview failed:", err);
    });
  }
}

function stopAudio() {
  globalAudio.pause();
  globalAudio.src = '';
  currentPlayingWid = null;
}

function initAudioEvents() {
  globalAudio.addEventListener('ended', () => {
    currentPlayingWid = null;
    renderTracks();
  });

  globalAudio.addEventListener('pause', () => {
    currentPlayingWid = null;
    renderTracks();
  });
}

/* =========================================================
   Quick Category Fill View & Modals
   ========================================================= */
function renderQuickFillGrid() {
  const grid = document.getElementById('quickFillGrid');
  grid.innerHTML = '';

  categories.forEach(cat => {
    const count = allTracks.filter(t => t.category === cat.id).length;
    const descKey = `description_${currentLang}`;
    const card = document.createElement('div');
    card.className = 'qf-card';
    card.innerHTML = `
      <div class="qf-card-header">
        <i class="fa-solid ${cat.icon || 'fa-music'}"></i>
        <div class="qf-card-info">
          <h3>${escapeHtml(getCategoryName(cat))}</h3>
          <p>${count} ${t('qfTracksCount')}</p>
        </div>
      </div>
      <p style="font-size: 11px; color: var(--text-muted);">${escapeHtml(cat[descKey] || cat.description_en || '')}</p>
      <button class="btn-win11 btn-secondary" onclick="openQuickFillModal('${cat.id}')">
        <i class="fa-solid fa-bolt"></i> ${t('qfFillCategory')}
      </button>
    `;
    grid.appendChild(card);
  });
}

document.getElementById('btnQuickFillCat').addEventListener('click', () => {
  if (currentCategory !== 'all') {
    openQuickFillModal(currentCategory);
  }
});

let qfChosenFilePath = null;
let qfChosenFileName = null;

function openQuickFillModal(catId) {
  activeQuickFillCat = catId;
  const cat = categories.find(c => c.id === catId);
  document.getElementById('qfModalTitle').textContent = `${t('quickFillCatBtn')}: ${cat ? getCategoryName(cat) : ''}`;
  document.getElementById('qfSelectedFile').textContent = '';
  document.getElementById('qfBtnApply').disabled = true;
  qfChosenFilePath = null;
  qfChosenFileName = null;

  document.getElementById('quickFillModal').style.display = 'flex';
}

function closeQuickFillModal() {
  document.getElementById('quickFillModal').style.display = 'none';
  activeQuickFillCat = null;
}

function triggerQuickFillPicker() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.pick_audio_file().then(res => {
      if (res && res.filePath) {
        qfChosenFilePath = res.filePath;
        qfChosenFileName = res.fileName;
        document.getElementById('qfSelectedFile').textContent = res.fileName;
        document.getElementById('qfBtnApply').disabled = false;
      }
    });
  }
}

function applyQuickFill() {
  if (!activeQuickFillCat || !qfChosenFilePath) return;

  const catTracks = allTracks.filter(t => t.category === activeQuickFillCat);
  catTracks.forEach(t => {
    modifiedTracks[t.wid] = {
      filePath: qfChosenFilePath,
      fileName: qfChosenFileName
    };
  });

  updateStats();
  renderTracks();
  closeQuickFillModal();
}

/* =========================================================
   Building the Mod & Progress Modal
   ========================================================= */
let lastSavedPakPath = null;

document.getElementById('btnBuildMod').addEventListener('click', () => {
  const modCount = Object.keys(modifiedTracks).length;
  if (modCount === 0) {
    alert(t('noTracksSelected'));
    return;
  }

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.pick_save_location("z_Custom_Music.pak").then(savePath => {
      if (!savePath) return;
      startBuildProcess(savePath);
    });
  }
});

function startBuildProcess(savePath) {
  lastSavedPakPath = savePath;
  const modal = document.getElementById('buildModal');
  const statusText = document.getElementById('modalStatusText');
  const bar = document.getElementById('modalProgressBar');
  const percentEl = document.getElementById('modalProgressPercent');
  const countEl = document.getElementById('modalProgressCount');
  const footer = document.getElementById('modalFooter');

  modal.style.display = 'flex';
  footer.style.display = 'none';
  bar.style.width = '0%';
  percentEl.textContent = '0%';
  statusText.textContent = t('buildPreparing');

  const mappings = [];
  for (const [wid, data] of Object.entries(modifiedTracks)) {
    const track = allTracks.find(t => t.wid === wid);
    if (track) {
      mappings.push({
        wid: wid,
        pakPath: track.pak_path,
        inputAudioPath: data.filePath,
        fileName: data.fileName
      });
    }
  }

  countEl.textContent = `0 / ${mappings.length}`;

  window.pywebview.api.build_mod(mappings, savePath).then(res => {
    if (res && res.success) {
      bar.style.width = '100%';
      percentEl.textContent = '100%';
      statusText.innerHTML = `
        <span style="color: var(--accent-green); font-weight: 600;">
          ${t('buildDone')}
        </span><br>
        Size: ${res.sizeMb} MB | Output: <span style="color: var(--accent-text); word-break: break-all;">${escapeHtml(savePath)}</span>
      `;
      footer.style.display = 'flex';
    } else {
      statusText.innerHTML = `<span style="color: #ff6b6b;">${t('buildError')} ${escapeHtml(res.error || 'Unknown error')}</span>`;
      footer.style.display = 'flex';
    }
  }).catch(err => {
    statusText.innerHTML = `<span style="color: #ff6b6b;">Error: ${escapeHtml(err.message || String(err))}</span>`;
    footer.style.display = 'flex';
  });
}

window.onBuildProgress = function(current, total, currentName, percent) {
  const statusText = document.getElementById('modalStatusText');
  const bar = document.getElementById('modalProgressBar');
  const percentEl = document.getElementById('modalProgressPercent');
  const countEl = document.getElementById('modalProgressCount');

  bar.style.width = `${percent}%`;
  percentEl.textContent = `${percent}%`;
  countEl.textContent = `${current} / ${total}`;
  statusText.textContent = `Converting: ${currentName}...`;
};

document.getElementById('modalBtnOpenFolder').addEventListener('click', () => {
  if (lastSavedPakPath && window.pywebview && window.pywebview.api) {
    window.pywebview.api.open_folder(lastSavedPakPath);
  }
});

document.getElementById('modalBtnClose').addEventListener('click', () => {
  document.getElementById('buildModal').style.display = 'none';
});

/* =========================================================
   External Links
   ========================================================= */
function openExternal(url) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.open_external_url(url);
  } else {
    window.open(url, '_blank');
  }
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
