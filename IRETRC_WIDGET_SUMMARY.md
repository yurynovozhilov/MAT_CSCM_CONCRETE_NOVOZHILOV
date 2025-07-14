# Добавление виджета IRETRC

## Выполненные изменения

Успешно добавлен виджет IRETRC по аналогии с виджетом NPLOT в оба Jupyter notebook файла:

### 1. Файл `cscm.ipynb`
- ✅ Добавлен виджет `iretrc_widget` с выпадающим списком
- ✅ Добавлена переменная `iretrc = iretrc_widget.value` в функцию `update_output`
- ✅ Добавлен параметр `itretrc = iretrc` в вызов функции `CSCM()`
- ✅ Добавлен обработчик событий `iretrc_widget.observe(update_output, names='value')`
- ✅ Добавлен виджет в `widgets.VBox` для отображения

### 2. Файл `cscm.ipynb`
- ✅ Добавлен виджет `iretrc_widget` с выпадающим списком
- ✅ Добавлена переменная `iretrc = iretrc_widget.value` в функцию `update_output`
- ✅ Добавлен параметр `itretrc = iretrc` в вызов функции `CSCM()`
- ✅ Добавлен обработчик событий `iretrc_widget.observe(update_output, names='value')`
- ✅ Добавлен виджет в `widgets.VBox` для отображения

## Параметры виджета IRETRC

```python
iretrc_widget = widgets.Dropdown(
    options=[
        ('0: Cap does not retract (default)', 0),
        ('1: Cap retracts', 1)
    ],
    value=0,
    description='IRETRC:',
    disabled=False,
    style={'description_width': 'initial'}
)
```

## Функциональность

- **Значение 0**: Cap does not retract (по умолчанию)
- **Значение 1**: Cap retracts

Виджет полностью интегрирован в интерфейс и будет автоматически обновлять результаты при изменении значения, точно так же как работает виджет NPLOT.

## Статус
✅ **ЗАВЕРШЕНО** - Виджет IRETRC успешно добавлен в оба notebook файла