#!/usr/bin/env python3
"""
Скрипт для тестирования всех модулей проекта MAT_CSCM_CONCRETE_NOVOZHILOV
Должен запускаться в виртуальном окружении venv312
"""

import sys
import os

def test_environment():
    """Проверка виртуального окружения"""
    print("🔍 Проверка окружения...")
    print(f"Python версия: {sys.version}")
    print(f"Python путь: {sys.executable}")
    
    # Проверяем, что мы в правильном venv
    if 'venv312' in sys.executable:
        print("✅ Используется правильное виртуальное окружение venv312")
    else:
        print("⚠️  ВНИМАНИЕ: Не используется venv312!")
        print("   Активируйте окружение: source activate.sh")
        return False
    return True

def test_imports():
    """Тестирование импортов модулей"""
    print("\n📦 Тестирование импортов...")
    
    modules_to_test = [
        ('numpy', 'np'),
        ('matplotlib.pyplot', 'plt'),
        ('collections', None),
        ('CEB', None),
        ('CapModel', None),
        ('plotcurves', None),
        ('d3py', None),
        ('transformation', None)
    ]
    
    failed_imports = []
    
    for module_name, alias in modules_to_test:
        try:
            if alias:
                exec(f"import {module_name} as {alias}")
            else:
                exec(f"import {module_name}")
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_basic_functionality():
    """Тестирование основной функциональности"""
    print("\n🧪 Тестирование основной функциональности...")
    
    try:
        import numpy as np
        from CEB import CEB, DIF_c, DIF_t
        from CapModel import alpha, lamda, Q_2, TXC, TXE
        from d3py import CSCM
        
        # Тест CEB модуля
        f_c = 40.0
        data = CEB(f_c)
        print(f"✅ CEB: f_c={data['f_c']}, f_t={data['f_t']:.2f}")
        
        # Тест DIF функций
        dif_c = DIF_c(f_c)
        dif_t = DIF_t(f_c)
        print(f"✅ DIF: compression shape={dif_c.shape}, tension shape={dif_t.shape}")
        
        # Тест CapModel функций
        alpha_val = alpha(f_c, rev=3)
        lambda_val = lamda(f_c, rev=3)
        print(f"✅ CapModel: alpha={alpha_val:.2f}, lambda={lambda_val:.2f}")
        
        # Тест функций с массивами
        I = np.array([0, 10, 20])
        q2_vals = Q_2(f_c, I, rev=1)
        txc_vals = TXC(f_c, I, rev=1)
        txe_vals = TXE(f_c, I, rev=1)
        print(f"✅ Функции с массивами: Q_2 shape={q2_vals.shape}")
        
        # Тест CSCM
        cscm_data = CSCM(f_c=f_c)
        print(f"✅ CSCM: MID={cscm_data['MID']['value']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_notebook_functions():
    """Тестирование исправленных функций из notebook"""
    print("\n📓 Тестирование функций notebook...")
    
    try:
        import numpy as np
        from CapModel import Q_2, TXC, TXE
        
        # Исправленные функции из notebook
        def Q1MC(f_c, I, rev=1):
            return np.sqrt(3)*Q_2(f_c,I,rev)/(1+Q_2(f_c, I, rev))

        def Q2MC(f_c, I, rev=1):
            return TXE(f_c, I, rev)/TXC(f_c, I, rev)

        def Q1WW(f_c, I, rev=1):
            q=(1-pow(Q_2(f_c, I, rev),2))
            return (np.sqrt(3)*q+(2*Q_2(f_c, I, rev)-1)*np.sqrt((3*q)+5*pow(Q_2(f_c, I, rev),2)-4*Q_2(f_c, I, rev)))/(3*q+pow(1-2*Q_2(f_c, I, rev),2))
        
        f_c = 40
        I = np.array([0, 10, 20])
        
        q1mc_result = Q1MC(f_c, I, rev=1)
        q2mc_result = Q2MC(f_c, I, rev=1)
        q1ww_result = Q1WW(f_c, I, rev=1)
        
        print(f"✅ Q1MC: результат получен")
        print(f"✅ Q2MC: shape={q2mc_result.shape}")
        print(f"✅ Q1WW: результат получен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в функциях notebook: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование проекта MAT_CSCM_CONCRETE_NOVOZHILOV")
    print("=" * 60)
    
    # Проверяем окружение
    if not test_environment():
        sys.exit(1)
    
    # Тестируем импорты
    imports_ok = test_imports()
    
    # Тестируем функциональность
    functionality_ok = test_basic_functionality()
    
    # Тестируем функции notebook
    notebook_ok = test_notebook_functions()
    
    # Итоговый результат
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   Импорты: {'✅ ПРОЙДЕНО' if imports_ok else '❌ ОШИБКИ'}")
    print(f"   Основная функциональность: {'✅ ПРОЙДЕНО' if functionality_ok else '❌ ОШИБКИ'}")
    print(f"   Функции notebook: {'✅ ПРОЙДЕНО' if notebook_ok else '❌ ОШИБКИ'}")
    
    if imports_ok and functionality_ok and notebook_ok:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Проект готов к использованию.")
        return 0
    else:
        print("\n⚠️  ЕСТЬ ПРОБЛЕМЫ! Проверьте ошибки выше.")
        return 1

if __name__ == "__main__":
    sys.exit(main())