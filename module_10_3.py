# Домашнее задание по теме "Блокировки и обработка ошибок"
from threading import Thread, Lock
from random import randint
import requests
from time import sleep


class Bank:

    def __init__(self):
        self.balance = 0
        self.lock = Lock()
        # super().__init__()

    # метод пополнения баланса
    def deposit(self):
        # цикл на 100 операций пополнения баланса
        for i in range(1, 101):
            # условие разблокировки баланса
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            # пополнение баланса на случайное число в диапазоне 50-500
            tranc = randint(50, 500)
            self.balance += tranc
            # вывод на консоль пополнения баланса
            print(f'пополнение №: {i}')
            print(f'Пополнение: {tranc}. Баланс: {self.balance}')
            # пауза в опреации
            sleep(0.001)

    # метод снятия с баланса
    def take(self):
        # цикл на 100 операций снятия с баланса
        for j in range(1, 101):
            # получение случайного числа в диапазоне 50-500 снятия с баланса
            tranc = randint(50, 500)
            # вывод на консоль запроса на снятие
            print(f'запрос на {tranc}')
            # условие проверки, что запрашиваемая сумма не более баланса
            if tranc <= self.balance:
                # уменьшение баланса на запрашиваемое число
                self.balance -= tranc
                # вывод на консоль результатов операции снятия
                print(f'снятие №: {j}')
                print(f'Снятие: {tranc}. Баланс: {self.balance}')
            # если запрашиваемая сумма больше баланса
            else:
                # вывод на консоль отклонения операции
                print(f'Запрос отклонён, недостаточно средств')
                # блокировка (закрытие) дальнейших операций до превышения баланса
                # на запрашиваемое число
                self.lock.acquire()


# объявление переменной обращения к классу Bank
bk = Bank()

# создание потоков операций пополнения th1 и снятия th2
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

# старт потоков
th1.start()
th2.start()
# останов выполнения потоков
th1.join()
th2.join()

# вывод на консоль остатка баланса
print(f'Итоговый баланс: {bk.balance}')