# Скрипты независимой проверки чисел аудита

Скрипты только читают артефакты в `paper_results_archive/` и `results_pareto_validation_all/`.
Они не запускают модели, не меняют результаты и не требуют PyTorch.

Запуск из этой папки (Python ≥3.9, только стандартная библиотека):

```bash
python3 main_check.py   # основная MNIST-серия publication_main (P=64, P=128)
python3 abl_pop.py      # publication_ablation и publication_population
python3 controls.py     # pilot (model42) и confirmation (model43/44), сверка с publication_main
python3 synth.py        # синтетика 10D/30D/50D из per-run JSON
```

Путь к корню репозитория определяется автоматически; его можно переопределить переменной `REPO_ROOT`.
