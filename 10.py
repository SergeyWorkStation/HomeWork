# Старый интерфейс, который возвращает данные в старом формате
class OldService:
    def fetch_data(self) -> str:
        return "Данные в старом формате"


#Новый интерфейс, который возвращает данные в новом формате
class NewService:
    def get_data(self) -> str:
        return "Данные в старом формате"


# Адаптер, который позволяет использовать старую систему с новым интерфейсом
class ServiceAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def get_data(self):
        return self.adaptee.fetch_data()

old_service = OldService()
adapter = ServiceAdapter(old_service)

print(adapter.get_data())