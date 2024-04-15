В рамках данного задания был реализован ассистент, основанный на статистической языковой модели. В исходный код были внесены следующие изменения:

1. Модель обучается на 3 датасетах: Den4ikAI/russian_dialogues, IgorVolochay/russian_jokes и SiberiaSoft/SiberianPersonaChat.
2. Добавлено top-k семплирование.
3. Теперь в словаре остаются только те слова, которые встретились в обучающем датасете не менее 10 раз.
4. Выбраны оптимальные гиперпараметры: temperature: 0.5, max_tokens: 8, sample_top_p: 0.9 sample_top_k: 10, decoding_strategy: top-p.

В боте реализованы следуюдие функции:
1. Логирование запросов с очисткой файлов
2. Уведомление в ЛС о запуске бота

Для тестирования бота необходимо:
1. Загрузить файлы stat_lm.py, llm_assistant.py, model_wrapper.py
2. Загрузить архив https://drive.google.com/file/d/1LNNQEMidpzj_dK6qJnQ7HJjZdx6HtmS-/view?usp=sharing и извлечь его в папку с относительным путем /models/stat_lm