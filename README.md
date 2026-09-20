# Divinity Music Mod Manager

Кроссплатформенное приложение для настройки и замены внутриигровой музыки в **Divinity: Original Sin Enhanced Edition** (DOS:EE) с поддержкой частичной замены и пакетного заполнения категорий.

Разработано специально для моддера **[Mizuqa](https://www.nexusmods.com/profile/Mizuqa?gameId=1995)** (автора мода *Baldur's Gate 3 Music Overhaul*).

---

## ✨ Особенности

- 🎨 **Кинематографичный интерфейс**:
  - Арт древних руин Источника из главного меню Divinity.
  - Плавный градиентный переход (Fade) в стильный интерфейс из тёмного матового стекла (*Glassmorphism*).
  - Интерактивные «баблы» (карточки) для каждого из 106 внутриигровых треков.
- 🎵 **Простота и универсальность**:
  - Принимает обычные **MP3** файлы (а также WAV, FLAC, OGG, M4A).
  - Встроенный аудио-плеер для предпрослушивания треков перед сборкой.
  - Drag & Drop: просто перетащите MP3 на карточку нужной сцены.
- ⚡ **Быстрое заполнение категорий**:
  - В один клик примените один трек или альбом на всю категорию (например, на все 12 боевых треков или на все таверны).
- 🧩 **Частичная замена (Partial Replacement)**:
  - Замените хоть один трек главного меню или битвы. Все остальные треки автоматически останутся оригинальными из базовой игры.
- 🔊 **Нативное качество движка Wwise**:
  - Автоматическая нормализация громкости по стандарту **EBU R128** (`-14 LUFS, -1.5 dB True Peak`).
  - Кодирование в **aoTuV Vorbis b6.03** (UID `0xa61035a7`) с шагом seek-таблицы 8192 сэмпла.
  - Полное отсутствие белого шума, щелчков и тишины.
- 📦 **Оптимизированный пакет LSPK v13**:
  - Архивация со сжатием LZ4 и приоритетом 150.
  - Дедупликация: если один и тот же файл назначен нескольким сценам, он сохраняется в `.pak` только один раз.
- 🌐 **Кроссплатформенность**:
  - Работает на **macOS**, **Windows** и **Linux**.

---

## 🚀 Запуск

### Требования:
- Python 3.10+
- `ffmpeg` (установлен в системе, например через `brew install ffmpeg` на Mac или `choco/winget install ffmpeg` на Windows)

### Быстрый старт:

```bash
cd /Users/yoshi/Projects/DivinityMusicManager
./run.sh
```

Или вручную через виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 📂 Установка собранного мода

1. Нажмите в приложении золотую кнопку **«Собрать всё воедино и сохранить»**.
2. Сохраните файл `z_Custom_Music.pak` в папку `Data` вашей игры:
   - **macOS (Steam)**: `~/Library/Application Support/Steam/steamapps/common/Divinity Original Sin Enhanced Edition/Divinity - Original Sin.app/Contents/Data/`
   - **Windows (Steam)**: `C:\Program Files (x86)\Steam\steamapps\common\Divinity Original Sin Enhanced Edition\Data\`
   - **Windows (GOG)**: `<Папка с игрой>\Data\`
3. Для удаления мода достаточно просто удалить файл `z_Custom_Music.pak` из папки `Data`. Исходные файлы игры остаются нетронутыми!

---

## 👤 Автор и ссылки

- **Nexus Mods**: [Mizuqa Profile](https://www.nexusmods.com/profile/Mizuqa?gameId=1995)
- **GitHub**: [divinity-music-mod-manager](https://github.com/mak74ik/divinity-music-mod-manager)
