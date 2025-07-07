#!/bin/bash
# Скрипт для активации виртуального окружения проекта
# Использование: source activate.sh

# Проверяем, что мы в правильной директории
if [ ! -d "venv312" ]; then
    echo "Ошибка: Директория venv312 не найдена!"
    echo "Убедитесь, что вы находитесь в корневой директории проекта MAT_CSCM_CONCRETE_NOVOZHILOV"
    return 1
fi

# Активируем виртуальное окружение
source venv312/bin/activate

echo "✅ Виртуальное окружение venv312 активировано"
echo "Python версия: $(python --version)"
echo "Путь к Python: $(which python)"
echo ""
echo "Доступные команды:"
echo "  jupyter notebook curves.ipynb  - запуск основного notebook"
echo "  python test_modules.py         - тестирование модулей"
echo "  deactivate                     - деактивация окружения"