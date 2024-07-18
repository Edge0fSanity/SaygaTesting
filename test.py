import ollama
import time
import psutil

models = ['model-q4_K.gguf:latest', 'model-q8_0.gguf:latest']

with open("text.txt", "r", encoding="UTF-8") as f:
  text = list(map(str.strip, f.readlines()))

out = open("answers.txt", "w", encoding="UTF-8")

print(*text)

for model in models:
  print("\n", model, "\n", file=out)
  # Запускаем мониторинг системных ресурсов до вызова модели
  start_time = time.time()
  process = psutil.Process()

  cpu_start = process.cpu_percent(interval=None)
  memory_start = process.memory_info().rss

  #sum_response_time = 0

  for message in text:
    print(f"Question: {message}", file=out)
    print("Answers: ", file=out)
    for i in range(1):
      response = ollama.chat(model=model, messages=[
        {
          'role': 'user',
          'content': message,
        },
      ])
      print(f"  {response['message']['content']}", file=out)
    print("\n")

  # Запускаем мониторинг системных ресурсов после вызова модели
  cpu_end = process.cpu_percent(interval=None)
  memory_end = process.memory_info().rss
  end_time = time.time()

  # Рассчитываем затраченные ресурсы
  cpu_usage = cpu_end - cpu_start
  memory_usage = memory_end - memory_start
  elapsed_time = end_time - start_time

  # Возвращаем ответ модели и статистику использования ресурсов
  monitor = f"""Использование процессора (i3-10105f): {cpu_usage*100}% 
        Использование памяти: {memory_usage / 1024} мб
        Затраченное время: {elapsed_time} с"""

  print(monitor, file=out)

# Статистика собранная Ollama
#print(f"Время выполнения модели: {response['total_duration']/10**9} с")

out.close()
