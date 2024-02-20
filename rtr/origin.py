from bs4 import BeautifulSoup


def get_origin(content):
    soup = BeautifulSoup(content, 'html.parser')

    tables = soup.find_all("tr")
    origin = None
    for t in tables:
        for th in t.find_all("th"):
            if th.next_element == "Origin":
                origin = t.find("td").get_text()

    return origin


def get_birthplace(content):
    soup = BeautifulSoup(content, 'html.parser')

    tables = soup.find_all("tr")
    born = None
    for t in tables:
        for th in t.find_all("th"):
            if th.next_element == "Born":
                if t.find("td").find('a'):
                    born = ", ".join([element.get_text() for element in t.find("td").find_all('a')])

    return born

