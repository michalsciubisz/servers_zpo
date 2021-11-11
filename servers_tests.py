import servers
import unittest
from collections import Counter
from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError, Server

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_passing_limit(self):
        products = [Product('P294', 1)] * (Server.n_max_returned_entries + 1)
        server = ListServer(products)
        self.assertRaises(TooManyProductsFoundError, server.get_entries, 1)



class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_error(self):
        products = [Product('PP234', 2), Product('PP235', 2), Product('PP236', 2), Product('PP237', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_for_zero(self):
        products = [Product('PPC234', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))
if __name__ == '__main__':
    unittest.main()