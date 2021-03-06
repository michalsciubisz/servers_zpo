#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABC, abstractmethod
import re #biblioteka do poszukiwania patternu

#product skończony najprawdopodobniej
class Product:
    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z] + [0-9]+', name):
            self.name = name
            self.price = price
        else:
            raise ValueError

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class Server(ABC): #klasa abstraktcyjna dziedziczy po abstrakcyjnej klasie ABC
    n_max_returned_entries: int = 3

    def __init__(self, *kwargs, **args):
        super().__init__()

    def get_entries(self, n_letters: int = 1) -> List[Product]: #rozne indeksy moga odnosic się do tych samych produktow
        pattern = '^[a-zA-Z]{{n_lettters}}\\d{{2,3}}&'.format(n_letters=n_letters)
        entries = []
        for p in self.get_all_products(n_letters):
            if re.match(pattern, p.name):
                entries.append(p)

        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted(entries, key=lambda entry: entry.price)

    #klasa abstrakcyjna modyfikowana w zależności od rodzaju podserwera
    def get_all_products(self, n_letters: int = 1):
        return NotImplementedError()

class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każda z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


#dwie funkcje do uzupełnienia
class ListServer:
    def __init__(self):
        pass

    def get_all_products(self, n_letters: int = 1):
        pass


class MapServer:
    def __init__(self):
        pass

    def get_all_products(self, n_letters: int = 1):
        pass


class Client:
    def __init__(self, server: Server):
        self.server: Server = server
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            products_list = self.server.get_all_products(n_letters)
        except TooManyProductsFoundError:
            return None
        if len(products_list) == 0:
            return None
        total_price = 0
        for product in products_list:
            total_price += product.price