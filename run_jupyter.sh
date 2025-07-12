#!/bin/bash
# Скрипт для запуска Jupyter Notebook с правильным виртуальным окружением
# Использование: ./run_jupyter.sh

# Проверяем, что мы в правильной директории
if [ ! -d "venv312" ]; then
    echo "❌ Ошибка: Директория venv312 не найдена!"
    echo "   Убедитесь, что вы находитесь в корневой директории проекта"
    exit 1
fi

# Активируем виртуальное окружение
source venv312/bin/activate

echo "🚀 Запуск Jupyter Notebook..."
echo "✅ Виртуальное окружение: venv312"
echo "🐍 Python версия: $(python --version)"
echo ""
echo "📓 Открывается cscm.ipynb..."
echo "   Для остановки нажмите Ctrl+C"
echo ""

# Запускаем Jupyter с CSCM keyword generator
jupyter notebook cscm.ipynb