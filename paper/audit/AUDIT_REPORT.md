# Аудит доказательной базы статьи «Score-Guided Population Search for High-Support Candidates in Diffusion Models»

**Репозиторий:** `fzllnrml/diffusion-mode-search-total`, ветка `main`, коммит `87c814e` (2026-10-14).
**Дата аудита:** 2026-10-14.
**Статус:** этап 1 завершён. Рукопись не писалась.

Аудит только читал файлы. Новые эксперименты не запускались, код и результаты не менялись. Все числа ниже пересчитаны заново из **per-run** артефактов (`summary.json` каждого метода/запуска, per-run JSON синтетики), а не скопированы из агрегированных CSV, документации, черновика или диссертации. Затем они сверены с агрегатами. Скрипты пересчёта и их полный вывод лежат в `paper/audit/verification/` (`outputs/*.txt`); для работы им нужна только стандартная библиотека Python.

Обозначения источников: **[A]** — архив результатов, **[C]** — код, **[F]** — frozen config, **[Doc]** — документация в корне репозитория, **[Draft]** — старый черновик `MNIST_paper.pdf`, **[Th]** — диссертация.

---

## 0. Краткие выводы

1. **Все headline-числа, на которых держится статья, воспроизводятся из сырых артефактов** с точностью до округления:
   - синтетика 10/30/50D;
   - основная MNIST-серия (15 парных запусков на P=128);
   - pilot (3 запуска);
   - confirmation (10 запусков);
   - stability_v2.

   Ни одной расхождения в средних между per-run файлами и агрегатами не найдено. В том числе нет расхождений между значениями baseline/search, которые повторно использует серия controls, и `publication_main`: 0 несовпадений по 39 строкам × 3 метрики.

2. **Центральный вывод подтверждается.** Dimension-aware search лучше matched-NFE DDIM по обоим co-primary метрикам во всех 15/15 парах. Он также лучше всех трёх reviewer-driven controls во всех 3/3 pilot-парах и во всех 10/10 confirmation-парах. Confirmation-интервалы (99.17 %, семейство 95 %, Bonferroni на 6 контрастов) далеко отстоят от нуля и от заданных практических порогов.

3. **Найдены существенные факты, которые черновик не раскрывает и которые обязательно нужно отразить в статье** (подробно в §9):
   - (a) `alpha=0.03` и радиус merge `0.65` были выбраны **скринингом на model42 по тем же kNN-метрикам**, что используются как исходы. `alpha=0.03` — крайнее значение сетки.
   - (b) MNIST-«v3f2» отличается от синтетического v3f2 не только масштабом шага. В нём нет промежуточного merge, другие schedule, `alpha`, число шагов и правило консолидации.
   - (c) Confirmation **не перезапускала** full search, DDIM-50 и matched-DDIM. Она повторно использовала уже существующие выходы `publication_main` для моделей 43/44. Новыми были только три control-метода и диагностики.
   - (d) Generate-and-select **хуже обычного DDIM-50**. Это слабый baseline выбора, а не «сильная альтернатива».
   - (e) Критерий сжатия в stability_v2 **выполняется и для DDIM**. Search и DDIM различает в основном reference drift.
   - (f) Search увеличивает долю train-close кандидатов с ~0 % (DDIM) до 3.18 %.
   - (g) Class entropy у search систематически немного ниже, чем у matched-DDIM.

4. **Найдены ошибки черновика.** Утверждение об «отдельной evaluation calibration» population-серии неверно. Старый stability 0.994 используется как evidence. Метаданные двух ссылок устарели.

5. **Отсутствует файл `NEXT_EXPERIMENTS.md`**, на который ссылаются код и документация как на «frozen plan». Заранее зафиксированный характер controls подтверждается только кодом (frozen-константы, проверки), конфигами, `decisions.json` и временными метками.

---

## 1. Что именно проверялось

| Объект | Где | Как проверено |
|---|---|---|
| Синтетика v3f2 (10/30/50D) | `results_pareto_validation_all/search_runs/*.json` (270 файлов), `summary_*.csv`, `mixtures/*.json` | Пересчёт recall/SoftError/n_found/NFE по 270 per-run JSON; SD на уровне модели и на уровне запуска; аудит мод; score alignment |
| Реализация синтетики | `src/algorithms/mode_finder_v3_f2.py`, `src/algorithms/clustering.py`, `scripts/run_pareto_validation_experiments.py` | Чтение кода шага, merge, early stopping |
| MNIST основная серия | `paper_results_archive/mnist_experiments/publication_main/` (30 suites, 210 method runs) | Пересчёт из `*/summary.json`; сверка с `publication_summary/{summary,paired_comparisons}.csv` |
| MNIST ablation / population | `.../publication_ablation/` (18 runs), `.../publication_population/` (48 runs) | Пересчёт; сопоставление с main по совпадающим (model, seed) |
| Development-серии | `.../geometry/`, `.../decision_mnist/`, `.../rms_screen/`, `.../diagnostic/` | Восстановление истории выбора `alpha`/радиуса |
| Обучение моделей | `paper_results_archive/mnist{,_seed43,_seed44}/{config.yaml,logs/metrics.jsonl}`, `.../publication_training/` | Сравнение конфигов и кривых loss |
| Pilot controls | `paper_results_archive/mnist_controls/` | Пересчёт из `model42_seed*/*/summary.json`; `decisions.json`; `stability_v2*.csv` |
| Confirmation | `paper_results_archive/mnist_controls_confirmation/` | Пересчёт из `model4{3,4}/model4*_seed*/*/summary.json`; `summary/paired_comparisons.csv`; `decisions.json`; `combined/provenance.json` |
| Определения controls | `src/mnist_controls/{controls,protocol,aggregate,confirmation_analysis}.py`, `configs/mnist_controls*.yaml`, `confirmation_manifest.json` | Сверка с формулировками задания |
| Метрики | `src/mnist_experiments/{evaluation,publication_evaluation,geometry}.py` | Определения kNN, percentile, memorization |
| Документация | `MNIST_PUBLICATION.md`, `MNIST_CONTROLS.md`, `MNIST_CONTROLS_CONFIRMATION.md`, `MNIST_EXPERIMENTS.md`, `MNIST_DIMENSION_STUDY.md` | Сверка утверждений с данными |
| Черновик и диссертация | `/mnt/user-data/uploads/MNIST_paper.pdf`, `master_thesis.pdf` | Сверка каждого числа |
| Библиография (4 ключевые новые ссылки) | веб-поиск | Проверка названий и площадок |

---

## 2. Карта экспериментальных серий

| Серия | Путь | Статус | Роль в статье |
|---|---|---|---|
| Синтетическая контрольная валидация v3f2 | `results_pareto_validation_all/` | Завершена: 90 смесей × 3 init = 270 запусков | **Основная** синтетическая часть |
| Прочие синтетические серии (1D/2D, v1–v3f3, sweeps, Levine) | `results_{1d,2d,10d,30d,50d}/`, `results_levine13/`, `levine/` | Завершены (диссертация) | В статью не входят, кроме, возможно, одной фразы о происхождении v3f2 |
| MNIST diffusion: обучение seeds 42/43/44 | `paper_results_archive/mnist*/` | 30 эпох каждая, одинаковый конфиг, кроме `seed` | Модели |
| Независимый evaluator (CNN) | `paper_results_archive/mnist_evaluator/history.json` | val. accuracy 0.9892 | Feature-space и semantic diagnostics |
| `diagnostic`, `geometry`, `decision_mnist`, `rms_screen` | `paper_results_archive/mnist_experiments/` | Exploratory, только model42 | **Development**: выбор геометрии шага, `alpha`, радиуса. Обязательно раскрыть (§6) |
| `publication_main` | `.../publication_main/` | 30 suites (3 модели × 5 seeds × P∈{64,128}), все `complete.json` на месте | **Основная MNIST-серия** |
| `publication_ablation` | `.../publication_ablation/` | 3 suites (model42, seeds 0–2, P=128) | Ablation merge (mean / every-level) |
| `publication_population` | `.../publication_population/` | 12 suites (model42, seeds 0–2, P∈{32,64,128,256}) | Population size |
| Pilot controls | `paper_results_archive/mnist_controls/` | 9 quality + 6 diagnostic + 3 input jobs, все complete (13.10.2026, 20:14–20:16 UTC) | Reviewer-driven pilot |
| Confirmation | `paper_results_archive/mnist_controls_confirmation/` | 30 quality + 20 diagnostic + 10 input jobs, все complete (14.10.2026, 09:54–10:01 UTC) | Независимое подтверждение |
| `mnist_dimension_smoke` (PCA d=2/4 и pixel 784) | `paper_results_archive/mnist_dimension_smoke/` | Smoke-run по одному запуску, с флагами `retained_variance_below_0.90` и др. | **Не использовать** (smoke, PCA-ветка исключена) |
| `mnist_smoke` | `paper_results_archive/mnist_smoke/` | Тренировочный smoke | Не использовать |

---

## 3. Синтетическая часть (10D/30D/50D, v3f2)

### 3.1. Постановка (проверено по [A] и [C])

- **Смеси.** Изотропные гауссианы, K=2…7, по 5 смесей на каждую пару (d, K), 30 обученных моделей на каждую размерность и 3 инициализации поиска → 90 запусков на размерность.
- **Параметры, одинаковые для всех 270 запусков** (`search_comparison.parameters` в каждом JSON):
  - P=150 частиц DDIM-50;
  - уровни `[800,600,400,300,200,150,100,70,50,30,15,5,0]`, 10 шагов на уровень, `step_size=0.08`, `normalize_score=True` (полная L2-длина шага 0.08);
  - 100 refine-шагов при t=0 с шагом 0.008;
  - merge после **каждого** уровня: complete linkage, представитель — **mean**, радиус `max(0.2, 1.0·σ_t)`, финальный радиус 0.2;
  - box [−10,10]^d с clip;
  - early stop при `max_shift < 1e-6` (`mode_finder_v3_f2.py:66–92`).
- **Matched-NFE DDIM:** `N = floor(NFE_v3f2/50)` образцов DDIM-50 без merge (`ddim_equal_nfe_raw`). Варианты с merge (`ddim_equal_nfe_merge_*`) дают практически те же числа (например, 30D: R=0.671, SE=3.381).
- **Метрики** (сверено по `per_true_min_distance` в JSON):
  - Recall — доля истинных мод, у которых ближайший кандидат лежит в пределах ε_hit;
  - **SoftError** — среднее по истинным модам расстояние до ближайшего кандидата. Это recall-side метрика локализации. Она **не штрафует лишних кандидатов**.
  - ε_hit = 2.0 / 3.5 / 4.5 для 10 / 30 / 50D.

### 3.2. Пересчитанные значения

Средние — по 90 запускам. **± — SD по 30 средним на уровне модели**; именно так считала диссертация. SD по 90 запускам немного больше и лежит в `summary_search_metrics.csv`.

| d | Метод | Recall | SoftError | Кандидатов | NFE |
|---|---|---|---|---|---|
| 10 | DDIM-150 (те же старты) | 0.837 ± 0.165 | 1.612 ± 0.444 | 150 | 7 500 |
| 10 | matched-NFE DDIM | **0.913 ± 0.110** | 1.388 ± 0.298 | 372.9 | 18 647 |
| 10 | v3f2, learned | 0.886 ± 0.130 | 1.225 ± 0.489 | 4.7 | 18 664 |
| 10 | v3f2, exact score | 0.995 ± 0.017 | 0.103 ± 0.309 | 4.6 | 7 500 нейр. + 11 564 аналит. |
| 30 | DDIM-150 | 0.593 ± 0.233 | 4.088 ± 1.838 | 150 | 7 500 |
| 30 | matched-NFE DDIM | 0.671 ± 0.223 | 3.381 ± 1.169 | 534.8 | 26 740 |
| 30 | v3f2, learned | **0.943 ± 0.097** | **2.689 ± 1.974** | 20.5 | 26 763 |
| 30 | v3f2, exact | 0.972 ± 0.059 | 0.877 ± 1.942 | 7.7 | 7 500 + 18 418 |
| 50 | DDIM-150 | 0.470 ± 0.257 | 5.817 ± 2.574 | 150 | 7 500 |
| 50 | matched-NFE DDIM | 0.563 ± 0.238 | 5.048 ± 2.100 | 714.4 | 35 722 |
| 50 | v3f2, learned | **0.956 ± 0.083** | **3.170 ± 2.700** | 77.8 | 35 744 |
| 50 | v3f2, exact | 0.966 ± 0.065 | 1.257 ± 2.694 | 36.9 | 7 500 + 25 609 |

Дополнительно проверено:
- **Запуски exact-score с полным покрытием:** 87/90, 77/90 и 72/90 (10/30/50D); SoftError в них 0.0046 / 0.0118 / 0.0280. Совпадает с [Th] и [Draft].
- **Взаимно-однозначный (1:1) F1:**
  - learned: 0.874 / 0.457 / 0.136;
  - exact: 0.984 / 0.762 / 0.279;
  - n_found/K у learned: 1.04 / 4.12 / 18.61.
- **Аудит мод** (`summary_gmm_mode_audit.csv`): во всех 90/90 смесях число строгих локальных мод и число уникальных стационарных точек равно K. Расстояние от центра компоненты до ближайшей моды равно 0.0 с точностью сохранения. Старты — центры плюс 64 точки.
- **Разделение компонент:** отношение минимального расстояния между центрами к максимальному σ равно 18.38 / 36.96 / 48.98. Это **режим очень хорошо разделённых компонент**: моды численно совпадают с центрами. Валидация «истинных мод» здесь корректна, но содержательно почти тривиальна. Трудность задачи — в поиске в высокой размерности, а не в неоднозначности модальной структуры.
- **Score alignment при t=0** (`summary_score_alignment.csv`, `mixtures/*.json`):

  | d | средний cos | доля cos ≥ 0.9 | средний угол | отношение норм learned/exact |
  |---|---|---|---|---|
  | 10 | 0.910 | 0.723 | 22.2° | 3.03 |
  | 30 | 0.872 | 0.612 | 26.3° | 3.14 |
  | 50 | 0.835 | 0.459 | 30.6° | 3.44 |

  При t ≥ 50 средний cos ≥ 0.996.
- **Вероятность пропуска (1−q)^150:** 0.861 при q=0.001 и 0.405 при q=0.006. Арифметика верна.
- **Новый производный анализ существующих артефактов** (`verification/synth_misses_by_weight.py`): **все** пропуски exact-score варианта приходятся на компоненты с весом < 0.03:

  | d | пропусков | медианный вес пропущенных | медианный вес найденных |
  |---|---|---|---|
  | 10 | 3 | 0.008 | 0.162 |
  | 30 | 15 | 0.007 | 0.165 |
  | 50 | 18 | 0.003 | 0.174 |

  Это прямо поддерживает интерпретацию «оставшиеся пропуски — следствие initial coverage». У learned-варианта в 10D пропуски бывают и у тяжёлых компонент (максимальный вес 0.50). В 10D к ошибкам добавляются ошибки learned score и merge.

### 3.3. Выводы по синтетике

- **10D.** Matched-DDIM имеет немного больший recall (0.913 против 0.886) при 373 выходных точках против 4.7. SoftError у search немного меньше (1.225 против 1.388). Результат **смешанный** — сохранить именно так.
- **30D / 50D.** Search лучше matched-DDIM и по recall (+0.272 / +0.393), и по SoftError (−0.69 / −1.88) при почти равном NFE (search использует на 23 / 22 NFE больше, чем matched-DDIM).
- **Exact-score control.** Замена поля резко снижает SoftError, а у представленных целей (запуски с полным покрытием) ошибка почти нулевая. Значительная часть остаточной ошибки learned-search — **ошибка learned score около t≈0**. Recall при exact score растёт мало (30D: 0.943 → 0.972; 50D: 0.956 → 0.966), и все оставшиеся пропуски — компоненты малой массы. Это **initial coverage**.
- **Избыточность.** Exact score снижает число кандидатов (50D: 77.8 → 36.9), но не до K. Это эффект правила merge и/или остаточной ошибки поля, а не только learned score.
- **Ограничение.** Серия по размерности — не чистый причинный эксперимент: вместе с d меняется разделение компонент (18 → 49). Также менялись ε_hit и NFE.

---

## 4. MNIST: основная серия `publication_main`

### 4.1. Модели и протокол (проверено)

- **Модели.** Три unconditional pixel diffusion U-Net (`src/mnist/model.py`, `base_channels=32`, T=1000, линейный β от 1e-4 до 0.02, ε-параметризация, `score = −ε̂/σ_t`). Каждая обучена 30 эпох (Adam, lr 2e-4, batch 64). Split одинаковый: `split_seed=42`, 55 000 train / 5 000 validation. Конфиги `mnist`, `mnist_seed43`, `mnist_seed44` различаются **только** `seed` и `output_dir`. Финальные val. loss: 0.02289 / 0.02272 / 0.02267.
- **Evaluator.** Отдельная CNN на том же split, validation accuracy 0.9892. В поиске не участвует.
- **Протокол** `mnist_rms_publication_v1`, `definition_hash 0de12232d9a259c1`:
  - DDIM-50 (η=0, clip x̂₀) создаёт P стартов;
  - движение по уровням `[800,500,300,200,100,50,20,5,0]`, по 5 шагов на уровень, затем 10 финальных шагов при t=0 с `alpha·0.1`;
  - `alpha=0.03`, clamp в [−1,1], **без merge** в основном методе `rms_v3f2`.
- **«t=0» — это не чистый score.** В метаданных `t_zero_is_clean: false`, `sigma_at_zero ≈ 0.0100`.
- **Шаг** (`geometry.py:8–13`): `l2: α·s/‖s‖`, `rms: α·√d·s/‖s‖`. Направление одинаковое; меняется только длина в √784 = 28 раз. Полная L2-длина RMS-шага — 0.84, у fixed-L2 — 0.03.
- **NFE** считается по изображениям:
  - search: 6 400 (init) + 7 040 (движение) = 13 440;
  - matched-DDIM: 268 × 50 = 13 400; первые 128 его сэмплов совпадают с init search, prefix-hash проверен.
  - Early stopping ни разу не сработал: `movement_nfe = 7040` во всех запусках.
- **Evaluation** (одинакова во всех сериях): kNN с k=5 по полному train (55 000), percentile относительно первых 1024 validation-изображений, pixel-расстояние в RMS-единицах, feature-расстояние — L2 в 64-мерных признаках evaluator.
- **Провенанс.** В `metadata.json` указано `git.commit 2535b22…`, `dirty: true`. Код при запуске был закоммичен не полностью; сохранены `implementation_sha256` и definition-хэши.

### 4.2. Пересчитанные результаты, P = 128

15 запусков на метод (3 модели × 5 seeds), mean ± SD по запускам.

| Метод | NFE | Кандидатов | Pixel kNN ↓ | Feature kNN ↓ | Pixel support ↑ | Feature support ↑ | Классов | Entropy |
|---|---|---|---|---|---|---|---|---|
| DDIM-50 | 6 400 | 128 | 0.3846 ± 0.0148 | 9.110 ± 0.303 | 30.58 | 25.91 | 10 | 2.252 |
| matched-NFE DDIM | 13 400 | 268 | 0.3897 ± 0.0151 | 9.236 ± 0.286 | 29.03 | 24.88 | 10 | 2.262 |
| fixed-L2 movement | 13 440 | 128 | 0.3799 ± 0.0151 | 9.035 ± 0.297 | 32.02 | 26.54 | 10 | 2.252 |
| **dimension-aware (RMS)** | 13 440 | 128 | **0.3204 ± 0.0149** | **7.277 ± 0.369** | **52.37** | **47.12** | 10 | 2.253 |
| RMS + final medoid | 13 440 | 33.6 ± 6.9 | 0.3544 ± 0.0146 | 7.957 ± 0.494 | 42.23 | 41.13 | 9.8 | 2.174 |
| DDIM + cluster | 6 400 | 43.3 ± 6.9 | 0.4144 | 9.704 | 23.35 | 21.76 | 9.93 | 2.168 |
| matched + cluster | 13 400 | 80.5 ± 12.0 | 0.4200 | 9.797 | 21.90 | 21.30 | 10 | 2.199 |

**Парные контрасты** (`publication_summary/paired_comparisons.csv`; иерархический bootstrap — сначала модели, потом seeds; 2 000 повторов; 95 % CI). Пересчёт средних совпал.

| Контраст | Pixel kNN | Feature kNN | Pixel support | Feature support |
|---|---|---|---|---|
| RMS − matched-DDIM | −0.06933 [−0.07200, −0.06650] | −1.9595 [−2.1389, −1.7987] | +23.33 [22.30, 24.45] | +22.25 [20.20, 24.44] |
| RMS − DDIM-50 | −0.06420 [−0.06522, −0.06313] | −1.833 [−1.988, −1.709] | +21.79 | +21.22 |
| RMS − fixed-L2 | −0.05949 [−0.06031, −0.05849] | −1.758 [−1.912, −1.625] | +20.35 | +20.59 |
| RMS+merge − RMS | +0.0340 [0.0224, 0.0478] | +0.680 [0.390, 1.080] | −10.14 | −6.00 |

**Знак эффекта RMS − matched:** 15/15 пар благоприятны по всем четырём метрикам. Диапазоны разностей: pixel от −0.0768 до −0.0621; feature от −2.453 до −1.480.

**По моделям**, matched → RMS (средние по 5 seeds):

| Модель | Pixel kNN | Feature kNN |
|---|---|---|
| 42 | 0.4090 → 0.3397 | 9.563 → 7.737 |
| 43 | 0.3763 → 0.3088 | 9.028 → 7.089 |
| 44 | 0.3838 → 0.3127 | 9.119 → 7.005 |

**Неопубликованное плечо P = 64** (те же 15 пар, в черновик не вошло): matched 0.3855 / 9.138, RMS 0.3244 / 7.380, fixed-L2 0.3822 / 9.108. Тот же качественный результат. Рекомендую упомянуть.

### 4.3. Вторичные диагностики основной серии

- **Масштаб перемещения.** Средний RMS displacement кандидата от его DDIM-предка: 0.307 у RMS-search, 0.025 у fixed-L2. Search **существенно** преобразует изображения: смещение сопоставимо с самими kNN-расстояниями (~0.3–0.4). Это не микроскопическое уточнение.
- **Clipping.** Доля обрезанных предложенных координат: 7.80 % ± 2.88 % у RMS, ≈0.001 % у fixed-L2.
- **Classifier confidence:** 0.953 у RMS, 0.923 у DDIM-50 и 0.923 у matched.
- **Memorization** (`publication_evaluation.py`). Порог «необычно близко к train» — 1 %-квантиль расстояний validation→train.

  | Метод | Доля train-close | Train−test gap percentile |
  |---|---|---|
  | DDIM-50 | **0.00 %** | 59.7 |
  | matched-DDIM | 0.10 % | 60.4 |
  | RMS-search | **3.18 % ± 1.49 %** | 55.0 |
  | RMS + merge | 1.40 % | 51.7 |

  Search заметно увеличивает train-close хвост относительно baseline и смещает gap-percentile к train на ~5 пунктов. При этом средний gap остаётся в типичной для validation области (50 соответствует validation).
- **Интерпретация support percentile.** Значение ~52 означает, что средний кандидат search по kNN-близости к train сопоставим с **медианным реальным validation-изображением**. У DDIM это ~30, то есть хуже 70 % реальных изображений. Search поднимает поддержку генераций до уровня типичных реальных цифр, но не «выше данных». Формулировку «high-support» нужно калибровать относительно этого.
- **Wall time** (одно устройство MPS, с инструментированием, одна оценка): RMS-search 10.6 с на suite, matched-DDIM 9.7 с, DDIM-50 4.8 с. Это описательная величина, не результат по эффективности.

### 4.4. Ablation и population (`publication_ablation`, `publication_population`; model42, seeds 0–2)

**Проверка совпадения с main.** Для совпадающих (model42, seed 0–2, P=128) значения `ddim`, `original_v3f2`, `rms_v3f2` и `rms_v3f2_merge` **бит-в-бит совпадают** с `publication_main`: одинаковые prefix-хэши и checkpoint. `resolved_config` отличается только списком методов, `stability.enabled` и метками серии. Абсолютные значения в этих сериях выше, потому что model42 — худшая из трёх моделей, а не из-за другой калибровки.

| Метод (P = 128) | Кандидатов | Pixel kNN | Feature kNN | Классов | Confidence |
|---|---|---|---|---|---|
| RMS, без merge | 128 | 0.3408 | 7.708 | 10 | 0.957 |
| RMS + final medoid | 40.7 | 0.3601 | 8.193 | 10 | 0.945 |
| RMS + final mean | 40.7 | 0.3512 | **8.955** | 9.67 | **0.879** |
| RMS + every-level medoid | **1.0** | 0.2471 | 4.193 | **1** | 1.000 |

Every-level merge схлопывает популяцию в одну точку при NFE 7 178: число движений падает вместе с размером популяции.

**Population.** Matched → RMS:

| P | NFE (search) | Pixel kNN | Feature kNN | Классов у RMS |
|---|---|---|---|---|
| 32 | 3 360 | 0.4047 → 0.3563 | 9.480 → 8.230 | 9.67 |
| 64 | 6 720 | 0.4036 → 0.3498 | 9.459 → 7.879 | 10 |
| 128 | 13 440 | 0.4078 → 0.3408 | 9.518 → 7.708 | 10 |
| 256 | 26 880 | 0.4073 → 0.3445 | 9.533 → 7.869 | 10 |

Все средние совпадают с [Draft].

---

## 5. Reviewer-driven controls: определения (сверено с [C] и [F])

| Control | Определение в коде | Совпадает с заданием? |
|---|---|---|
| **DDIM-105** | `model.ddim(noise, 105)`; индексы `round(linspace(999, 0, 105))`; проверка отсутствия дубликатов; η=0; те же Gaussian-шумы, что у search (`pairing_type`: «same Gaussian prefix; different DDIM trajectory»); 128 выходов; NFE = 128 × 105 = **13 440** | Да |
| **Low-noise-only** | `refine(refine(init, 45, .03), 10, .003)`. Каждый шаг: `score(x, 0)`, RMS-шаг, clamp. Init — та же DDIM-50 популяция (`pairing_type`: «identical DDIM-50 initialization»). Без merge. NFE 6 400 + 7 040 = **13 440** | Да. «t=0» означает σ ≈ 0.01 |
| **Generate-and-select** (`ddim_pool_representatives`) | Пул — те же 268 DDIM-50 сэмплов, что у matched-DDIM (повторно использованы, 13 400 NFE). Расстояние — CPU float64 pixel-RMS. Первый представитель — глобальный medoid; далее жадно добавляется кандидат, минимизирующий сумму расстояний точек пула до ближайшего выбранного (facility location). При равенстве выбирается наименьший индекс. 128 исходных сэмплов. На вход функции подаётся только пул — evaluator, train и метки ей недоступны | Да. Утечки evaluator нет |
| **stability_v2** | `contraction_diagnostic`: 2 направления на кандидата; масштабы 0.02 и 0.05 RMS (шаг `scale·√d·v`, затем clamp); **фактическое** δ₀ после clamp; невалидно, если δ₀ ≤ 0.01; F = 10 шагов `refine(·, 10, .003)`, применяемых и к x₀, и к y₀; ρ = RMS(F(y₀) − F(x₀)) / δ₀; drift = RMS(F(x₀) − x₀) | Да |

**Заранее зафиксированные правила решений** (`aggregate.py:30–139`, `confirmation_analysis.py:55–138`, `confirmation_manifest.json`):

- **Практические пороги:** 0.0069 (pixel) и 0.196 (feature). Это ≈10 % парного выигрыша основной серии RMS − matched (0.0693 и 1.96).
- **Pilot «clear win»:** во всех парах control − search превышает порог по обоим co-primary метрикам, и для search нет diversity guardrail.
- **Diversity guardrail:**
  - класс-покрытие < 8 хотя бы в одном запуске,
  - **или** среднее падение покрытия > 1 класса относительно DDIM-50,
  - **или** среднее падение entropy > 0.10.
- **Confirmation:**
  - стратифицированный по модели парный bootstrap, 10 000 повторов, seed 20261013, равные веса моделей;
  - 6 co-primary контрастов (3 controls × 2 метрики), центральный интервал 99.1667 % (Bonferroni, семейство 95 %);
  - `search_win`: средние по обеим моделям больше порога **и** нижняя граница > 0;
  - **pilot не входит** в confirmation-интервалы.
- **Stability:** valid ≥ 0.9, median ρ ≤ 0.9, доля ρ < 1 ≥ 0.75 на обоих масштабах, median drift ≤ 0.01; для каждой модели нужно ≥ 4/5 прошедших запусков.

---

## 6. История разработки на model42 (не раскрыта в черновике)

Exploratory-серии в архиве (все на **model42**):

1. `geometry/` — P=32, seed 0, сравнение `step_mode ∈ {l2, raw, rms}` с every-level mean merge.
2. `decision_mnist/` — model42, seeds 0–4, P∈{64,128}: movement и merged matched-NFE варианты RMS-движения. Значения matched-DDIM совпадают с `publication_main` model42: pixel 0.4090, feature 9.563.
3. `rms_screen/` — **model42, seeds 0–1, P=64**:
   - скрининг **alpha ∈ {0.003, 0.005, 0.01, 0.02, 0.03}**: pixel kNN монотонно падает с ростом alpha, с ~0.40 до 0.344 / 0.356 при alpha=0.03;
   - скрининг **радиуса merge ∈ {0.45, 0.55, 0.65, 0.75}**: при 0.75 остаётся 7 классов из 10.
   - Использовались **те же pixel/feature kNN-метрики**, что затем стали исходами. Выбраны `alpha=0.03` (крайняя точка сетки) и радиус 0.65.

**Следствия для статьи:**
- (i) Model42 и её seeds 0–4 — **development data**. Строго независимы от выбора гиперпараметров только модели 43/44. Черновик говорит, что seed 42 «участвовал в development protocol», но о скрининге alpha и радиуса по исходным метрикам не упоминает. Это нужно раскрыть.
- (ii) `alpha=0.03` не показан как оптимум: это граница сетки. Правильная формулировка — «выбранная рабочая точка».
- (iii) Low-noise-only control использует тот же `alpha=0.03`, выбранный для полного search. Это честно по бюджету, но `alpha` для low-noise-only отдельно не настраивался. Это нужно сказать как ограничение control.

---

## 7. Pilot и confirmation: пересчитанные результаты

Значения `ddim`, `matched_ddim` и `rms_v3f2` в controls — это **те же запуски `publication_main`**, повторно использованные после проверки хэшей. Сверка по 39 строкам (3 метода × 13 запусков) и трём метрикам: 0 расхождений. Pilot `compute.json`: 99 840 новых NFE; confirmation: 332 800. Оба равны ожидаемой стоимости «только новые controls + диагностики» при повторном использовании старых bundle.

### 7.1. Pilot: model42, seeds 0–2, P = 128

n = 3, mean ± SD.

| Метод | NFE | Pixel kNN | Feature kNN | Pixel sup. | Feature sup. | Классов | Entropy |
|---|---|---|---|---|---|---|---|
| DDIM-50 | 6 400 | 0.4039 ± 0.0054 | 9.466 ± 0.215 | 24.7 | 22.3 | 10 | 2.244 |
| matched-DDIM | 13 400 | 0.4078 ± 0.0045 | 9.519 ± 0.204 | 23.6 | 22.0 | 10 | 2.252 |
| DDIM-105 | 13 440 | 0.4045 ± 0.0054 | 9.433 ± 0.226 | 24.6 | 22.7 | 10 | 2.253 |
| Low-noise-only | 13 440 | 0.4079 ± 0.0055 | 9.524 ± 0.222 | 23.5 | 22.1 | 10 | 2.241 |
| Generate-and-select | 13 400 | 0.4379 ± 0.0050 | 10.198 ± 0.044 | 17.1 | 17.6 | 10 | 2.161 |
| **Full search** | 13 440 | **0.3408 ± 0.0058** | **7.709 ± 0.244** | **46.1** | **42.4** | 10 | 2.258 |

Search − control, средние (все пары 3/3 благоприятны по pixel, feature и обоим support):

| Control | Pixel kNN | Feature kNN |
|---|---|---|
| DDIM-105 | −0.0637 | −1.724 |
| Low-noise-only | −0.0672 | −1.816 |
| Generate-and-select | −0.0972 | −2.490 |

`decisions.json`: `pilot_search_clear_win = true` для всех трёх; `stability_pilot_positive = true`; `stability_drift_small = true`; `branch = one_confirmation_all_three_controls`.

### 7.2. Confirmation: models 43/44, seeds 0–4, P = 128

n = 10, mean ± SD.

| Метод | Pixel kNN | Feature kNN | Pixel sup. | Feature sup. | Классов | Entropy |
|---|---|---|---|---|---|---|
| DDIM-50 | 0.3751 ± 0.0054 | 8.942 ± 0.195 | 33.4 | 27.5 | 10 | 2.256 |
| matched-DDIM | 0.3801 ± 0.0061 | 9.073 ± 0.162 | 31.9 | 26.4 | 10 | 2.269 |
| DDIM-105 | 0.3750 ± 0.0053 | 8.907 ± 0.185 | 33.5 | 27.9 | 10 | 2.257 |
| Low-noise-only | 0.3735 ± 0.0052 | 8.972 ± 0.200 | 34.0 | 27.4 | 10 | 2.255 |
| Generate-and-select | 0.4159 ± 0.0036 | 9.743 ± 0.163 | 21.6 | 21.3 | 10 | 2.199 |
| **Full search** | **0.3107 ± 0.0045** | **7.047 ± 0.138** | **55.5** | **49.7** | 10 | 2.252 |

**Confirmation-интервалы** (`mnist_controls_confirmation/summary/paired_comparisons.csv`, `record_type = confirmation_interval`). Знак: **control − search**, положительное значение — в пользу search.

| Control | Pixel kNN: разность [99.17 % CI] | Feature kNN: разность [99.17 % CI] | Средние по моделям 43 / 44 (pixel; feature) | Пар в пользу search |
|---|---|---|---|---|
| DDIM-105 | 0.0643 [0.0626, 0.0656] | 1.860 [1.697, 2.026] | 0.0643 / 0.0643; 1.841 / 1.879 | 10/10 |
| Low-noise-only | 0.0628 [0.0608, 0.0644] | 1.925 [1.755, 2.105] | 0.0632 / 0.0625; 1.893 / 1.957 | 10/10 |
| Generate-and-select | 0.1052 [0.1011, 0.1090] | 2.696 [2.526, 2.859] | 0.1046 / 0.1057; 2.602 / 2.790 | 10/10 |

Пары в пользу search: 10/10 по обеим kNN-метрикам и обоим support percentiles для каждого control.

`decisions.json`: для всех трёх controls `search_confirmed = true`, `practical_equivalence = false`, `control_noninferior = false`; diversity guardrails не сработали ни для search, ни для controls; `stability_confirmed = true`.

**Доля выигрыша search над matched-DDIM, воспроизводимая control** (`gain_fraction` = (matched − control) / (matched − search)):

| Control | Pixel (m43 / m44) | Feature (m43 / m44) |
|---|---|---|
| DDIM-105 | 0.048 / 0.097 | 0.050 / 0.112 |
| Low-noise-only | 0.064 / 0.123 | 0.024 / 0.075 |
| Generate-and-select | −0.55 / −0.49 | −0.34 / −0.32 |

Generate-and-select отрицателен: control хуже matched-DDIM.

### 7.3. Что эти данные позволяют и не позволяют утверждать

- **Позволяют.** В данной постановке gain не объясняется:
  - числом обращений к сети;
  - более длинной DDIM-траекторией (DDIM-105 ≈ DDIM-50: разница ≤ 0.0006 pixel);
  - тем же бюджетом движения при t≈0 (low-noise-only ≈ DDIM-50: на model42 немного хуже, на 43/44 немного лучше, разница ≤ 0.004 pixel);
  - данным geometry-only правилом выбора представителей.

  Low-noise-only поддерживает интерпретацию, что ценность создают шаги на зашумлённых уровнях: движение только в поле σ≈0.01 почти не меняет support.
- **Не позволяют.**
  - Generate-and-select **хуже обычного DDIM-50** (pixel 0.4159 против 0.3751). Выбор «центральных» по pixel-геометрии сэмплов снижает близость к train. Это не «сильный» selector, а предварительно заданный простой baseline. Вывод — только «данное правило выбора не воспроизводит gain». Нельзя писать «sampling + selection не помогает».
  - Confirmation подтверждает превосходство **над controls**. Но строки search, DDIM-50 и matched-DDIM — это **те же запуски**, что в основной серии для моделей 43/44. Новые наблюдения — только controls.
  - Интервалы условны на фиксированных моделях 43/44: bootstrap только по search seeds внутри модели.
  - **Entropy.** Search − matched-DDIM = −0.017 в среднем, отрицательно в **10/10** парах (−0.046 … −0.001). Это мало (ln 10 = 2.303; порог guardrail 0.10), но систематично. Корректно: «нет грубого collapse по coverage/entropy при небольшом систематическом снижении entropy относительно matched-DDIM».

---

## 8. Stability_v2

Сводка из `stability_v2.csv`; фактические δ₀ из per-candidate CSV. Скрипт: `verification/stability_summary.py`.

| Фаза | Объект | Номинал | Фактическое δ₀ (медиана) | Median ρ, среднее [диапазон] | Доля ρ < 1 | Reference drift, среднее [диапазон] |
|---|---|---|---|---|---|---|
| pilot m42 | search | 0.02 | 0.0172 | 0.377 [0.374, 0.380] | 1.000 | 0.0065 [0.0065, 0.0066] |
| pilot m42 | search | 0.05 | 0.0383 | 0.530 [0.527, 0.533] | 1.000 | 0.0065 |
| pilot m42 | DDIM init | 0.02 | 0.0166 | 0.531 [0.528, 0.535] | 1.000 | 0.0163 [0.0161, 0.0166] |
| pilot m42 | DDIM init | 0.05 | 0.0386 | 0.617 [0.607, 0.621] | 1.000 | 0.0163 |
| conf m43/44 | search | 0.02 | 0.0156 | 0.423 [0.416, 0.430] | 1.000 | 0.0065 [0.0061, 0.0070] |
| conf m43/44 | search | 0.05 | 0.0373 | 0.585 [0.566, 0.604] | 1.000 | 0.0065 |
| conf m43/44 | DDIM init | 0.02 | 0.0155 | 0.539 [0.521, 0.560] | 1.000 | 0.0145 [0.0129, 0.0160] |
| conf m43/44 | DDIM init | 0.05 | 0.0379 | 0.650 [0.613, 0.694] | 1.000 | 0.0145 |

Валидны 100 % возмущений.

**Интерпретация:**
- Заранее заданный stability-критерий выполнен для search: 5/5 запусков на каждой модели, а также в pilot.
- Однако **критерии по ρ формально выполнила бы и DDIM-инициализация**: 100 % ρ < 1, медианы 0.52–0.69. Это наше применение того же правила к DDIM; само правило оценивалось только для search.
- DDIM не прошла бы **критерий drift ≤ 0.01**: все её drift лежат в диапазоне 0.0129–0.0166.
- Отличие search — **меньший drift (≈2.2×)** и **умеренно меньший ρ**.
- Горизонт конечен: суммарная длина 10 шагов ≤ 0.03 RMS.
- Корректная формулировка: «search-кандидаты лежат там, где заданное локальное отображение при t≈0 сильно сжимает малые возмущения, а сам кандидат почти не смещается. DDIM-точки тоже сжимаются, но заметно дрейфуют». Не «только search-точки — аттракторы». Не «доказанные моды».
- Фактические возмущения после clamp на 20–25 % меньше номинальных (0.0156 вместо 0.02 и 0.037 вместо 0.05). Об этом нужно сказать.

**Старый stability** (`stability_return_rate`, 0.994): perturbation 0.005 / 0.01, радиус возврата 0.01. Возмущение 0.005 изначально лежит внутри радиуса. Как evidence **не использовать**; можно упомянуть в методологической сноске, почему он заменён.

---

## 9. Реестр несоответствий

| # | Где | Суть | Что верно (по артефактам) | Действие |
|---|---|---|---|---|
| D1 | [Draft] Abstract, Table 2, §5.7, §5.10, Conclusion | Old stability 0.994 и разность +0.913 используются как evidence | Методологически слабый тест; заменён stability_v2 (§8) | Удалить как evidence |
| D2 | [Draft] §5.5 | «Population series имеет собственную evaluation calibration» | Evaluation та же; значения бит-в-бит совпадают с main для общих запусков; отличие абсолютных чисел — подвыборка model42 seeds 0–2 | Исправить формулировку |
| D3 | [Draft] §3.2, §3.5, Fig. 1; задание | MNIST-метод описан как synthetic v3f2 с одним изменением — длиной шага | Отличия: нет промежуточного merge (synthetic — every-level mean merge); schedule 9×5 против 13×10; alpha 0.03 RMS против 0.08 L2; 10 против 100 final steps; final merge — опциональный medoid с константным радиусом 0.65 против mean с `max(0.2, σ_t)`; every-level merge на MNIST схлопывает популяцию до 1 | В статье описать как два инстанса одного принципа; в MNIST-части явно указать отличия. «Fixed-L2» на MNIST — ablation длины шага при **том же** MNIST-протоколе, а не перенос полного thesis-протокола (это признаёт и `MNIST_PUBLICATION.md`) |
| D4 | [Draft] §5.4, §6.4 | Не раскрыт скрининг alpha и радиуса по outcome-метрикам на model42 | `rms_screen/`: alpha ∈ {0.003…0.03}, радиус ∈ {0.45…0.75}, model42, seeds 0–1, P=64 | Раскрыть в Methods и Limitations; model42 обозначить как development |
| D5 | [Doc] `MNIST_CONTROLS*.md`, [C] `aggregate.py`, `decisions.json` | Ссылка на «frozen `NEXT_EXPERIMENTS.md`» | Файла нет ни в репозитории, ни в инвентаре `PAPER_REPO_INVENTORY.txt` | Добавить в репозиторий, если есть, или описывать pre-specification через код и конфиги |
| D6 | Задание («независимая confirmation») | Можно прочитать как полностью новые запуски | Full search, DDIM-50 и matched-DDIM для 43/44 повторно использованы из `publication_main`; новые только controls и диагностики | Сформулировать точно |
| D7 | Задание («честный baseline») | Generate-and-select подаётся как сильная альтернатива | Он хуже DDIM-50 по обеим kNN-метрикам в 13/13 запусках (pilot и confirmation; проверено) | Описать как простой pre-specified selector, ухудшающий support; выводы ограничить им |
| D8 | [Th] Табл. 4.5–4.6, [Draft] Table 1 и `summary_search_metrics.csv` | SD различаются | Средние идентичны; [Th]/[Draft] дают SD по 30 моделям, CSV — по 90 запускам | Явно указать тип SD |
| D9 | [Draft] §3.2, §5.7 | «t=0» без оговорки | σ(t=0) ≈ 0.01; `t_zero_is_clean: false` | Указать |
| D10 | [A] `publication_main/*/metadata.json` | `git.dirty: true` | Код закоммичен не полностью; есть implementation и definition-хэши | Упомянуть в reproducibility statement; при возможности восстановить точный коммит |
| D11 | [Draft] References [12], [14] | Устаревшие названия | arXiv 2406.02017 v3 переименована в «On the Hardness of Sampling from Mixture Distributions via Langevin Dynamics»; arXiv 2512.10524 сейчас называется «Inverse problems with diffusion models: MAP estimation via mode-seeking loss» и есть в листинге ICML 2026 | Проверить и обновить метаданные на этапе 2 |
| D12 | [Draft] §5.3 | Плечо P=64 основной серии не упомянуто | Есть 15 пар; качественно тот же результат | Упомянуть кратко |
| D13 | [Draft] §5.8 | Train-close 3.18 % дан без baseline | DDIM 0 %, matched 0.10 % | Дать сравнение |
| D14 | [Draft] §5.6, §5.10 | «Unmerged population сохраняет 10 классов» | Верно при P=64 и 128; при P=32 — 9.67 | Уточнить |
| D15 | [Draft] — | Снижение entropy против matched-DDIM не упомянуто | −0.017, 10/10 пар confirmation (основная серия: −0.009) | Упомянуть |
| D16 | [Draft] §5.3 | «Увеличение независимых DDIM samples почти вдвое не улучшает support» | Верно, а matched даже немного хуже DDIM-50 (0.3897 против 0.3846) | Сохранить |
| D17 | [Draft] Table 1 и §4 | Колонка «Exact-score search error» без NFE | Exact использует 7 500 нейронных NFE на старты плюс аналитический score; по NFE не сравним | Пометить в таблице |
| D18 | Stability_v2: правило и интерпретация | «Search проходит» можно прочитать как специфичность | Критерий по ρ выполнила бы и DDIM; различает drift | Описать честно (§8) |

**Подтверждено без расхождений (выборочно):**
- Все числа синтетики в [Th] и [Draft] Table 1, включая отношения норм 3.03 / 3.44, separation 18.38 → 48.98 и full-coverage SE.
- Все числа основной MNIST-серии в [Draft] Table 2, кроме stability: средние, SD, CI (11)–(14), 15/15, средние по моделям.
- Population-числа [Draft] и consolidation: 33.6 ± 6.9, 80.53 ± 12.05, mean против medoid.
- Clipping 7.8 %, memorization 55-й percentile и 3.18 %.
- NFE: 13 440 / 13 400 / 268.

---

## 10. Реестр утверждений: claim → artifact → config → code → doc

Статус: ✅ подтверждено; ⚠️ подтверждено с обязательной оговоркой; ❌ не подтверждается или удалить.

| Утверждение | Artifact | Config | Code | Статус |
|---|---|---|---|---|
| 10D: matched-DDIM recall немного выше search | `results_pareto_validation_all/search_runs/dim10_*.json` | `parameters` в JSON; `configs/presets/dim10.yaml` | `mode_finder_v3_f2.py` | ✅ |
| 30D/50D: search лучше matched-DDIM по recall и SoftError при ≈ равном NFE | `search_runs/dim{30,50}_*.json` | то же | то же | ✅ (оговорка: разделение компонент меняется с d) |
| Exact score почти устраняет ошибку локализации у представленных целей | `search_runs/*` (`v3f2_exact`) | — | `run_pareto_validation_experiments.py` | ✅ |
| Пропуски при exact score — компоненты малой массы (initial coverage) | производный анализ `search_runs/*` + `mixture.weights` | — | `verification/synth_misses_by_weight.py` | ✅ (новый расчёт по существующим данным) |
| Learned score теряет точность при t≈0 | `summary_score_alignment.csv`, `mixtures/*.json` | — | — | ✅ |
| Истинные моды = центры (90/90) | `summary_gmm_mode_audit.csv` | — | — | ✅ (оговорка: очень хорошее разделение) |
| Fixed-L2 перенос слаб на MNIST | `publication_main/*/original_v3f2/summary.json` | `publication.py` (definitions) | `geometry.py:step_delta` | ✅ (это ablation длины шага в MNIST-протоколе) |
| Dimension-aware search лучше matched-DDIM, 15/15, обе метрики | `publication_main/*/{rms_v3f2,matched_ddim}/summary.json`; `publication_summary/paired_comparisons.csv` | `configs/mnist_experiments/publication_main.yaml` | `publication.py`, `publication_aggregate.py` | ✅ |
| Эффект воспроизводится на трёх независимо обученных моделях | то же + `mnist_seed4{3,4}/config.yaml` | `publication_train.yaml` | `src/mnist/train.py` | ✅ (оговорка: model42 — development) |
| Эффект не зависит от выбора P | `publication_population/*` | `publication_population.yaml` | — | ⚠️ только model42 и 3 seeds; P=128 — не оптимум |
| DDIM-105 не воспроизводит gain | `mnist_controls{,_confirmation}/**/ddim_105/summary.json`; CI в `.../summary/paired_comparisons.csv` | `configs/mnist_controls*.yaml`, `confirmation_manifest.json` | `controls.py:ddim_105` | ✅ |
| Low-noise-only не воспроизводит gain → вклад зашумлённых уровней | `**/low_noise_only/summary.json` | то же | `controls.py:low_noise_only` | ✅ (оговорка: alpha не настраивался под control; σ=0.01, а не 0) |
| Generate-and-select не воспроизводит gain | `**/ddim_pool_representatives/summary.json` | то же | `controls.py:select_representatives` | ⚠️ selector хуже DDIM-50 — вывод только про это правило |
| Pilot → confirmation без перенастройки | `mnist_controls/summary/decisions.json`; `confirmation_manifest.json`; временные метки `status.json` | frozen-константы в `protocol.py`; проверки ключей | `protocol.py:load_config` | ⚠️ `NEXT_EXPERIMENTS.md` отсутствует |
| Confirmation — независимые модели 43/44 | `mnist_controls_confirmation/model4{3,4}/` | — | `confirmation.py` | ⚠️ search/DDIM-строки повторно использованы из main |
| Search-кандидаты локально устойчивы (stability_v2) | `**/summary/stability_v2{,_per_candidate}.csv` | `stability_v2` в manifest | `controls.py:contraction_diagnostic` | ⚠️ ρ < 1 и у DDIM; различает drift |
| Old stability 0.994 | `publication_main/*/rms_v3f2/summary.json` | — | — | ❌ как evidence |
| Нет грубого collapse по классам | `class_coverage`, `class_entropy` во всех сериях | guardrail в `aggregate.py` | — | ⚠️ малое систематическое снижение entropy против matched |
| Population-wide gain не объясняется копированием train | `fraction_unusually_close_train`, `train_test_gap_percentile` | `unusually_close_quantile=.01` | `publication_evaluation.py` | ⚠️ train-close хвост вырос с 0 % до 3.2 % |
| Consolidation — компромисс, а не источник gain | `rms_v3f2_merge`, ablation | — | — | ✅ |
| Every-level merge → collapse | `publication_ablation/*/rms_v3f2_every_level` | `publication_ablation.yaml` | — | ✅ |
| Clipping ≈ 7.8 % координат | `clipping_fraction_mean` | — | `geometry.py:project` | ✅ |
| NFE ≠ wall-clock | `search_wall_seconds` | — | — | ✅ (wall time сопоставим, одно устройство) |
| √d-scaling — универсальный закон | — | — | — | ❌ не утверждать |
| Найдены «истинные моды MNIST» | — | — | — | ❌ не утверждать |

---

## 11. Ограничения и отрицательные результаты, которые обязательно должны быть в статье

1. **10D.** Matched-DDIM имеет немного больший recall; универсального превосходства нет.
2. **Синтетика.** Режим очень хорошо разделённых компонент. Серия по d не изолирует размерность: меняются разделение, ε_hit и NFE.
3. **Избыточность.** В 50D learned-search даёт 77.8 кандидата на K = 2…7 (1:1 F1 = 0.136). Exact score уменьшает избыточность, но не устраняет.
4. **Fixed-L2 на MNIST почти бесполезен.** Это отрицательный результат переноса, а не сравнение двух нормировок.
5. **Development.** alpha и радиус выбраны скринингом на model42 по тем же метрикам; alpha — граница сетки.
6. **MNIST-кандидаты — не доказанные моды.** «t=0» — это σ≈0.01. Labels — только semantic guardrail.
7. **Support percentile ≈ 52** — уровень типичных реальных изображений, а не «экстремальная плотность».
8. **Масштаб перемещения.** RMS 0.31 на пиксель — кандидаты существенно отличаются от исходных сэмплов.
9. **Clipping 7.8 %** — проекция является частью динамики.
10. **Train-close хвост.** 3.18 % против 0 % у DDIM; memorization не исключён.
11. **Entropy.** Малое систематическое снижение против matched-DDIM; within-class collapse не исследован.
12. **Generate-and-select** — слабый selector (хуже DDIM-50); выводы ограничены им.
13. **Low-noise-only.** alpha не настраивался отдельно; поле при σ≈0.01, а не чистый score.
14. **Confirmation.** Новые только controls; модели 43/44 уже были в основной серии; CI условны на двух моделях.
15. **Stability_v2.** Сжатие есть и у DDIM; ключевое различие — drift; горизонт ≤ 0.03 RMS; фактические возмущения меньше номинальных.
16. **Три модели.** Ограниченная оценка вариативности обучения; только MNIST.
17. **NFE ≠ wall-clock.** Evaluator, kNN и clustering в NFE не входят.
18. **Провенанс.** `git dirty`; отсутствует `NEXT_EXPERIMENTS.md`.

---

## 12. Рекомендуемый набор таблиц для рукописи (только проверенные числа)

- **T1. Синтетика** (§3.2 этого отчёта): 10/30/50D × {matched-DDIM, learned search, exact search}. Колонки: recall, SoftError, кандидаты, NFE, 1:1 F1. Опционально строка DDIM-150. Явно указать, что SD — на уровне модели.
- **T2. MNIST main, P=128** (§4.2): DDIM-50, matched-DDIM, fixed-L2, dimension-aware. Колонки: обе kNN-метрики, оба support percentile, классы. Парные CI — в тексте или в отдельной строке.
- **T3. Strong controls:** два блока — **pilot (model42, n=3, descriptive)** и **confirmation (models 43/44, n=10, 99.17 % CI)**. Строки: DDIM-50, matched-DDIM, DDIM-105, low-noise-only, generate-and-select, full search.
- **T4. Stability_v2** (§8): компактно, search против DDIM, ρ и drift по фазам.
- Population, consolidation, memorization — в тексте или в одной вспомогательной таблице (§4.3–4.4).

---

## 13. Вопросы к автору перед этапом 2

1. Есть ли где-то `NEXT_EXPERIMENTS.md` (или другой документ с датой фиксации плана)? Если есть, его стоит добавить в репозиторий. Если нет, pre-specification опишу через код, конфиги и временные метки.
2. Согласны ли вы раскрыть скрининг alpha и радиуса на model42 в Methods (D4)? Рекомендую: это сильно снижает риск претензий рецензента TMLR.
3. Включать ли плечо P=64 основной серии (D12) — кратко, одним предложением или строкой?
4. Подтвердите формулировку для generate-and-select (D7): «простой предварительно заданный geometry-only selector, который сам по себе снижает support относительно DDIM-50».
