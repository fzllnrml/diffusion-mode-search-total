# Приложение к рукописи `manuscript_ru.md` (служебное, не для подачи)

Документ сопровождает новую русскую master-версию рукописи. Он опирается на аудит `paper/audit/AUDIT_REPORT.md` и на скрипты проверки `paper/audit/verification/`.

Структура:
- **A** — изменения относительно старого черновика;
- **B** — что добавлено в аргументацию;
- **C** — ослабленные и удалённые утверждения;
- **D** — основные утверждения и источники;
- **E** — исправления по реестру D1–D18;
- **F** — места, требующие проверки человеком перед подачей.

---

## A. Изменения относительно старого черновика (`MNIST_paper.pdf`)

| Раздел | Что было | Что стало |
|---|---|---|
| Аннотация | Главный MNIST-результат — только сравнение с matched-NFE DDIM; stability 0.994 как свидетельство | Добавлены три заранее зафиксированных контроля, схема pilot → confirmation, stability_v2 с честной оговоркой о DDIM. Смешанный результат 10D назван явно; термин *mode candidates* закреплён |
| Введение | Сравнение «search против больше DDIM» как центральный тест; три пункта вклада | Вопрос сформулирован шире: sampling versus search **и** простые альтернативные схемы при том же бюджете. Пять пунктов вклада и отдельный абзац «что работа не утверждает» |
| Связанные работы | По существу сохранены | Уточнены метаданные [12], [14]; добавлена ссылка [17] (Carreira-Perpiñán) из диссертации о модах смесей |
| §3 Метод | Описан как единый алгоритм; MNIST-вариант — «тот же v3f2 с другим масштабом шага» | Общий алгоритм 1 и **табл. 1 с двумя экземплярами** (синтетика и MNIST): разные расписания, шаги, политика объединения. Уточнено, что «$t=0$» — это $\sigma\approx0.01$. Утверждение 1 о покрытии сформулировано с доказательством как доказанное свойство |
| §4 Синтетика | Табл. 1 с learned/exact/matched | Добавлены DDIM-150, 1:1 F1, указан тип SD (по 30 моделям). Строка exact помечена как oracle без matched-NFE. Новый производный анализ весов пропущенных компонент. Явно сказано, что компоненты очень хорошо разделены (отношение 18 → 49) и серия по $d$ не является причинным экспериментом |
| §5.1–5.2 MNIST | Метрики и протокол | Уточнены опорные множества, роль support percentile (≈ 50 = типичное реальное изображение), парность по общему шуму |
| §5.3 (новый) | — | **Раскрыт development-скрининг $\alpha$ и радиуса на модели 42**; модели 43/44 названы свободными от этого выбора |
| §5.4 (бывш. 5.2) | «Прямой перенос synthetic rule почти не работает» | Переформулировано как **ablation длины шага внутри MNIST-протокола**. Добавлено фактическое смещение 0.025 против 0.307 и парный ДИ |
| §5.5 (бывш. 5.3–5.4) | Табл. 2 со столбцами stability и консолидации | Табл. 3 без stability; консолидация вынесена в §5.10. Добавлены $P=64$ (15 пар) и интерпретация величины эффекта (support, смещение, проекция) |
| §5.6–5.7 (новые) | — | Определения контролей, заранее зафиксированные правила, pilot и confirmation, табл. 4 с раздельными фазами, интерпретация «позволяет / не позволяет» для каждого контроля |
| §5.8 (бывш. 5.7) | Perturb-and-return, возврат 0.994 | Полностью заменено на stability_v2; старый тест описан только как причина замены |
| §5.9 (бывш. 5.6 и 5.8) | Коллапс и запоминание без baseline | Добавлены baseline запоминания (DDIM 0 %, matched 0.1 %) и систематическое снижение энтропии; формулировка «нет грубого коллапса на уровне классов» |
| §5.10 (бывш. 5.5 и 5.9) | Population с «отдельной калибровкой» | Исправлено: та же оценка, другая подвыборка (model42, seeds 0–2) |
| §5.11 | Цепочка исключённых объяснений | Расширена до 9 пунктов, включая три новых контроля |
| §6 | 11 подразделов | Перестроено: добавлены §6.3 (пределы контролей), §6.7 (разработка на model42), §6.8 (область confirmation), §6.11 (провенанс), §6.12 (дальнейшая работа) |
| Заключение | Опиралось на stability 0.994 | Опирается на контроли и stability_v2 с оговоркой о DDIM |
| Воспроизводимость (новый раздел) | — | Пути к коду и результатам, скрипты проверки, `git dirty`, отсутствие текста протокола в репозитории |

---

## B. Что добавлено в аргументацию

Новых запусков при подготовке рукописи не было. Ниже — эксперименты, уже выполненные в репозитории, но отсутствовавшие в черновике, а также новые расчёты по существующим результатам.

1. **DDIM-105** (pilot model42, seeds 0–2; confirmation models 43/44, seeds 0–4).
2. **Low-noise-only** (те же фазы).
3. **Generate-and-select** (`ddim_pool_representatives`, те же фазы).
4. **Stability_v2** для кандидатов поиска и для DDIM-инициализации (те же фазы).
5. **Плечо $P=64$ основной серии** (было выполнено, но не описано в черновике).
6. **Development-скрининг $\alpha$ и радиуса** (`rms_screen/`). Выполнен до основной серии; теперь раскрыт.
7. **Производные расчёты по существующим артефактам:**
   - веса компонент, пропущенных при точном score;
   - фактические $\delta_0$ после проекции в stability_v2;
   - сравнение drift DDIM с порогом;
   - энтропия поиска против matched-DDIM по парам;
   - число запусков, где generate-and-select хуже DDIM-50.

   Скрипты: `paper/audit/verification/{synth_misses_by_weight,stability_summary,controls,rms_screen}.py`.

---

## C. Ослабленные или удалённые утверждения

| Утверждение черновика | Решение |
|---|---|
| Stability 0.994 и разность +0.913 как свидетельство «аттракторов» | **Удалено** как свидетельство. Заменено на stability_v2 с оговоркой: сжатие есть и у DDIM, отличие — drift |
| «Candidates … ведут себя как устойчивые точки притяжения learned field намного чаще, чем обычные DDIM samples» | **Удалено.** По stability_v2 сжимаются обе группы |
| «Unmerged population сохраняет десять semantic classes» (общая формулировка) | **Сужено:** верно при $P=64$ и $128$; при $P=32$ — 9.67 класса; энтропия систематически немного ниже matched-DDIM; «нет грубого коллапса на уровне классов» |
| «Population-wide gap не смещён к train; небольшой tail» | **Уточнено:** train-close хвост вырос с ~0 % (DDIM) до 3.18 %; gap-перцентиль сдвинулся к train на ~5 пунктов |
| Population series «имеет собственную evaluation calibration» | **Удалено** как ошибочное |
| Fixed-$L_2$ как «исходное правило движения synthetic setup» | **Сужено:** это ablation длины шага внутри MNIST-протокола |
| $\alpha=0.03$ без указания происхождения | **Раскрыто:** выбор на model42 по исходным метрикам, край сетки |
| «Эффект сохраняется across independently trained models» без оговорки | **Уточнено:** model42 — development; свободны от выбора параметров только 43/44 |
| Высокая поддержка как «плотные области» | **Откалибровано:** support ≈ 52 — уровень типичного реального изображения |
| Неявное «$t=0$ — чистое распределение» | **Исправлено:** $\sigma_0\approx0.01$ |
| Exact score в одной таблице с NFE-сравнением | **Помечено** как oracle без matched-NFE |

---

## D. Основные утверждения рукописи и их источники

Все пути — относительно корня репозитория. Колонка «Проверка» указывает скрипт и файл вывода в `paper/audit/verification/`.

| # | Утверждение (раздел) | Источник | Определение / код | Проверка |
|---|---|---|---|---|
| 1 | 90/90 смесей: число строгих мод = $K$, центры = моды (§4.2) | `results_pareto_validation_all/summary_gmm_mode_audit.csv` | `scripts/run_pareto_validation_experiments.py` | ручная проверка в аудите §3.2 |
| 2 | Отношение разделения 18.4 / 37.0 / 49.0 (§4.2) | `results_pareto_validation_all/mixtures/*.json` | — | аудит §3.2 (расчёт по `mixture.mus`, `sigmas`) |
| 3 | Табл. 2: recall, SoftError, кандидаты, 1:1 F1, NFE (§4.3) | `results_pareto_validation_all/search_runs/*.json`; `summary_search_metrics.csv` | `src/algorithms/mode_finder_v3_f2.py` | `synth.py` → `outputs/synth.txt` |
| 4 | Согласование learned/exact score по $t$ (§4.4) | `summary_score_alignment.csv`; `mixtures/*.json` (`norm_ratio`) | — | аудит §3.2 |
| 5 | Full-coverage SoftError 0.0046 / 0.0118 / 0.0280 (§4.4) | `search_runs/*.json` | — | `outputs/synth.txt` |
| 6 | Все пропуски exact — компоненты весом < 0.03 (§4.4) | `search_runs/*.json` (+ `mixture.weights`) | — | `synth_misses_by_weight.py` → `outputs/synth_misses_by_weight.txt` |
| 7 | Протокол MNIST, $\sigma_0\approx0.01$, NFE 13 440 / 13 400 (§5.2) | `paper_results_archive/mnist_experiments/publication_main/*/metadata.json`, `*/summary.json` | `src/mnist_experiments/publication.py`, `geometry.py:step_delta` | `main_check.py` → `outputs/main_check.txt` |
| 8 | Модели 42/43/44 отличаются только seed (§5.2) | `paper_results_archive/mnist{,_seed43,_seed44}/config.yaml`, `logs/metrics.jsonl` | `src/mnist/train.py` | аудит §4.1 |
| 9 | Development-скрининг $\alpha$ и радиуса (§5.3) | `paper_results_archive/mnist_experiments/rms_screen/` | `configs/mnist_experiments/rms_screen.yaml` | `rms_screen.py` → `outputs/rms_screen.txt` |
| 10 | Fixed-$L_2$ ablation: значения, смещение, ДИ (§5.4) | `publication_main/*/original_v3f2/summary.json`; `publication_summary/paired_comparisons.csv` | `geometry.py:step_delta` | `outputs/main_check.txt`; CSV |
| 11 | Табл. 3; парные ДИ; 15/15; по моделям (§5.5) | `publication_main/*/{ddim,matched_ddim,original_v3f2,rms_v3f2}/summary.json`; `publication_summary/{summary,paired_comparisons}.csv` | `publication_aggregate.py` | `outputs/main_check.txt` |
| 12 | $P=64$: 15/15, значения (§5.5) | те же файлы ($P=64$) | — | `outputs/main_check.txt`; CSV |
| 13 | Clipping 7.8 %, смещение 0.307, support ≈ 52 (§5.5) | `publication_main/*/rms_v3f2/summary.json` | `geometry.py:project` | `outputs/main_check.txt` |
| 14 | Определения контролей (§5.6) | `paper_results_archive/mnist_controls_confirmation/confirmation_manifest.json` | `src/mnist_controls/controls.py`, `protocol.py` | аудит §5 |
| 15 | Правила решений, пороги 0.0069 / 0.196, guardrails (§5.6) | `mnist_controls/summary/decisions.json`; `mnist_controls_confirmation/summary/decisions.json` | `src/mnist_controls/aggregate.py`, `confirmation_analysis.py` | аудит §5 |
| 16 | Хронология pilot → confirmation (§5.6) | `**/status.json` (`finished_at`) | — | аудит §7 |
| 17 | Табл. 4, блок pilot (§5.7) | `paper_results_archive/mnist_controls/model42_seed*/*/summary.json` | `controls.py` | `controls.py` → `outputs/controls.txt` |
| 18 | Табл. 4, блок confirmation и 99.17 %-интервалы (§5.7) | `mnist_controls_confirmation/model4{3,4}/*/*/summary.json`; `summary/paired_comparisons.csv` (`record_type=confirmation_interval`) | `confirmation_analysis.py:intervals` | `outputs/controls.txt`; CSV |
| 19 | Повторное использование search/DDIM/matched в confirmation (§5.7) | `**/inputs/summary.json` (`source_directory`); `summary/compute.json` | `protocol.py:usable_source_files` | `controls.py` (0 расхождений с main) |
| 20 | Generate-and-select хуже DDIM-50 в 13/13 (§5.7) | как 17–18 | `controls.py:select_representatives` | аудит §7 (расчёт) |
| 21 | Доли выигрыша, воспроизводимые контролями (§5.7) | `mnist_controls_confirmation/summary/paired_comparisons.csv` (`gain_fraction`) | `aggregate.py` | CSV |
| 22 | Табл. 5 stability_v2; DDIM сжимает, drift выше (§5.8) | `mnist_controls{,_confirmation}/summary/stability_v2{,_per_candidate}.csv` | `controls.py:contraction_diagnostic`, `stability_v2` | `stability_summary.py` → `outputs/stability_summary.txt` |
| 23 | Энтропия поиска < matched-DDIM в 10/10 (§5.9) | как 18 | — | `outputs/controls.txt` |
| 24 | Табл. 6 запоминание (§5.9) | `publication_main/*/{ddim,matched_ddim,rms_v3f2,rms_v3f2_merge}/summary.json` | `src/mnist_experiments/publication_evaluation.py:memorization_metrics` | `outputs/main_check.txt` |
| 25 | Every-level merge → 1 кандидат (§5.9) | `publication_ablation/*/rms_v3f2_every_level/summary.json` | — | `abl_pop.py` → `outputs/abl_pop.txt` |
| 26 | Population $P=32\ldots256$ (§5.10) | `publication_population/*/*/summary.json` | — | `outputs/abl_pop.txt` |
| 27 | Совпадение population/ablation с main бит-в-бит (§5.10) | `publication_{ablation,population,main}/*` | — | аудит §4.4 |
| 28 | Консолидация 128 → 33.6, ухудшение, matched-cluster 80.5, mean против medoid (§5.10) | `publication_main/*/{rms_v3f2_merge,matched_cluster}`; `publication_ablation/*/rms_v3f2_mean` | — | `outputs/main_check.txt`, `outputs/abl_pop.txt`; CSV |
| 29 | Wall time 10.6 и 9.7 с (§6.9) | `publication_main/*/*/summary.json` (`search_wall_seconds`) | — | аудит §4.3 |
| 30 | `git dirty = true` (§6.11) | `publication_main/*/metadata.json` | — | аудит §4.1 |

---

## E. Исправления по реестру аудита D1–D18

| # | Несоответствие | Где исправлено |
|---|---|---|
| D1 | Old stability 0.994 как свидетельство | Удалено отовсюду; stability_v2 в §5.8; старый тест упомянут только как причина замены |
| D2 | «Отдельная калибровка» population-серии | §5.10: та же оценка, совпадение бит-в-бит, другая подвыборка |
| D3 | MNIST-метод как synthetic v3f2 с одним изменением | §3.7, табл. 1 (два экземпляра); §5.4 (ablation внутри протокола); §6.1 |
| D4 | Скрининг $\alpha$ и радиуса не раскрыт | §5.3 (Methods) и §6.7, §6.5 (Limitations) |
| D5 | Ссылка на отсутствующий `NEXT_EXPERIMENTS.md` | В рукописи файл не упоминается; провенанс — через код, конфиги, `decisions.json`, временные метки (§5.6, §6.11) |
| D6 | Объём confirmation | §5.7 и §6.8: новые — три контроля и stability; search/DDIM/matched повторно использованы после проверок |
| D7 | Generate-and-select как сильный baseline | §5.6–5.7: «простой заранее заданный geometry-only selector», сам ухудшает kNN-близость; вывод ограничен этим правилом |
| D8 | Тип SD в синтетике | Подпись табл. 2: SD по 30 средним на уровне модели |
| D9 | «$t=0$» без оговорки | §3.7, §5.2, §5.6, §5.8, §6.4 |
| D10 | `git dirty` | §6.11 и раздел «Воспроизводимость» |
| D11 | Устаревшие метаданные [12], [14] | Список литературы: [12] — текущее название v3 с указанием названия v1; [14] — название v2 и workshop ICML 2026 |
| D12 | $P=64$ не упомянут | §5.5, абзац «$P=64$» |
| D13 | Запоминание без baseline | §5.9, табл. 6 |
| D14 | 10 классов «всегда» | §5.9, §5.10 (9.67 при $P=32$) |
| D15 | Снижение энтропии не упомянуто | §5.9; §5.11, п. 7; заключение |
| D16 | «Больше образцов не улучшает support» | Сохранено с уточнением, что matched немного хуже DDIM-50 (§5.5) |
| D17 | Exact score в NFE-таблице | Подпись табл. 2: oracle, NFE «—» |
| D18 | Stability-критерий как специфичный признак | §5.8: критерий определён для поиска; ρ < 1 и у DDIM; различает drift; применение порога к DDIM — наше сопоставление |

---

## F. Что требует проверки человеком перед подачей

**Провенанс и формулировки о предрегистрации**

1. **§5.6, абзац о провенансе.** Формулировка «зафиксированы до реализации контролей и до запуска pilot» опирается на ваше утверждение и на косвенные признаки: frozen-константы и временные метки. Если исходный текст протокола будет восстановлен в `paper/audit/provenance/`, его нужно упомянуть как **recovered pre-run chat protocol**, а не как файл, который тогда был закоммичен. Решите, упоминать ли это в рукописи.
2. **§6.11 и «Воспроизводимость».** Желательно восстановить точный коммит, соответствующий `implementation_sha256` основной серии, или явно оставить формулировку о `git dirty`.

**Обоснование выбора параметров**

3. **§5.3.** Правило выбора радиуса 0.65 из данных скрининга не следует однозначно: при 0.65 теряется в среднем один класс, при 0.55 — нет. Сейчас текст описывает выбор как компромисс без формального правила. Проверьте, нет ли у вас записанного критерия.
4. **§5.3.** Скрининг радиуса выполнялся при $\alpha=0.01$, а не 0.03. В тексте это указано; проверьте, что это не вызывает претензий к консолидации в основной серии.

**Интерпретации, которые стоит перечитать**

5. **§5.7, интерпретация generate-and-select.** Фраза «по-видимому, смещается к изображениям, менее похожим на конкретные обучающие примеры» — гипотеза. Она не проверялась визуально или количественно. Можно удалить или явно пометить как гипотезу.
6. **§5.8.** «Это согласуется с тем, что кандидаты находятся вблизи устойчивых точек learned-поля в этом смысле» — проверьте, достаточно ли осторожно.

**Библиография и терминология**

7. **Литература [12], [14], [15], [16].** Метаданные проверены веб-поиском 14.10.2026, но статус площадок мог измениться. Перед подачей перепроверьте: финальная площадка для [12] (на arXiv venue не указан); основной трек или только workshop для [14]; том и страницы для [15].
8. **Ссылка [17]** взята из диссертации; проверьте библиографию по первоисточнику.
9. **Терминология.** В тексте смешаны русские и английские термины (score, NFE, recall, pilot, confirmation, guardrail). Для журнальной версии решите, какие оставить.

**Подготовка к подаче**

10. **Figures 1–3** описаны, но не построены. Их нужно построить по указанным CSV, без новых запусков.
11. **Объём.** Текст не сокращён под ограничения TMLR и не переведён. Сокращать в первую очередь стоит §6, где часть ограничений повторяет §4–5.
