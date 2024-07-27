import ollama
import time
import psutil

models = ['llama3.1:8b']

with open("text_deu.txt", "r", encoding="UTF-8") as f:
  text = list(map(str.strip, f.readlines()))

out = open("answers/answers_deu.txt", "w", encoding="UTF-8")

print(*text)

for model in models:
  print("\n", f"Модель: {model}", "\n", file=out)
  # Запускаем мониторинг системных ресурсов до вызова модели
  start_time = time.time()
  process = psutil.Process()
  cpu_start = process.cpu_percent(interval=None)
  memory_start = process.memory_info().rss

  #sum_response_time = 0
  n = 0
  for message in text:
    print(f"Question: {message}", file=out)
    print("Answers: ", file=out)
    for i in range(3):
      response = ollama.chat(model=model, messages=[
        {
          'role': 'user',
          'content': message,
          'temperature':0.7,
        },
      ])
      print(f"  {response['message']['content']}", file=out)
    print("\n", file=out)
    n+=1
    print(n, "out of 20")
    out.flush()

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
print(f"Время выполнения модели: {response['total_duration']/10**9} с")

out.close()
