#!/bin/bash
set -e

echo "🥊 Встановлення Boxer..."

# Створюємо директорії
INSTALL_DIR="$HOME/.local/share/boxer"
BIN_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Завантажуємо останній реліз з GitHub
echo "⬇️  Завантаження останньої версії з GitHub..."
URL="https://github.com/davidykmisha2015-prog/Boxer/releases/download/mid/Boxer-Linux-x86_64.tar.gz"
curl -sL "$URL" -o /tmp/boxer.tar.gz

# Розпаковуємо
echo "📦 Розпакування файлів..."
tar -xzf /tmp/boxer.tar.gz -C "$INSTALL_DIR" --strip-components=1 2>/dev/null || tar -xzf /tmp/boxer.tar.gz -C "$INSTALL_DIR"
rm /tmp/boxer.tar.gz

# Створюємо посилання, щоб програма запускалась командою boxer
ln -sf "$INSTALL_DIR/boxer" "$BIN_DIR/boxer"
ln -sf "$INSTALL_DIR/boxer_app" "$BIN_DIR/boxer_app"

# Встановлюємо ярлик та іконку для меню програм
mkdir -p "$HOME/.local/share/applications"
mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps"

cp "$INSTALL_DIR/app_icon.png" "$HOME/.local/share/icons/hicolor/256x256/apps/boxer.png"
cp "$INSTALL_DIR/boxer_app.desktop" "$HOME/.local/share/applications/boxer.desktop"

# Прописуємо правильні шляхи у ярлику
sed -i "s|Exec=.*|Exec=$BIN_DIR/boxer_app|" "$HOME/.local/share/applications/boxer.desktop"
sed -i "s|Icon=.*|Icon=boxer|" "$HOME/.local/share/applications/boxer.desktop"

# Оновлюємо базу іконок та ярликів
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo "✅ Boxer успішно встановлено!"
echo "👉 Тепер ви можете запустити програму, написавши 'boxer' у терміналі, або знайти її у вашому меню додатків."
echo "⚠️  Якщо команда 'boxer' не знайдена, переконайтеся, що $HOME/.local/bin додано до вашого PATH."
