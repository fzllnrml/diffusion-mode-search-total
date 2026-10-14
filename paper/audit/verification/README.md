# Скрипты независимой проверки чисел аудита

Скрипты только читают артефакты в `paper_results_archive/` и `results_pareto_validation_all/`.
Они не запускают модели, не меняют результаты и не требуют PyTorch.

Запуск из этой папки (Python ≥3.9; стандартная библиотека, для rms_screen.py — pyyaml):

```bash
python3 main_check.py   # основная MNIST-серия publication_main (P=64, P=128)
python3 abl_pop.py      # publication_ablation и publication_population
python3 controls.py     # pilot (model42) и confirmation (model43/44), сверка с publication_main
python3 synth.py        # синтетика 10D/30D/50D из per-run JSON
python3 synth_misses_by_weight.py  # веса пропущенных компонент (производный анализ)
python3 stability_summary.py      # stability_v2 по фазам, фактические δ0
python3 rms_screen.py             # development-скрининг alpha и радиуса на model42 (нужен pyyaml)
```

Путь к корню репозитория определяется автоматически; его можно переопределить переменной `REPO_ROOT`.
