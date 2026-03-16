import redis

try:
    # Свързване с локалния Redis сървър
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Записваме тестова стойност
    r.set('test_key', 'Hello from Nevumo!')
    
    # Четем стойността обратно
    value = r.get('test_key')
    
    print(f"Статус: Успешна връзка!")
    print(f"Прочетена стойност: {value}")
    
except Exception as e:
    print(f"Грешка при връзката: {e}")