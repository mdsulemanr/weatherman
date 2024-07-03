from bs4 import BeautifulSoup

with open("html_doc.html") as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())
# print(soup.title)       # <title>The Dormouse's story</title>
# print(soup.title.name)  # title
# print(soup.title.string) # The Dormouse's story
# print(soup.title.parent.name) # head
# print(soup.p)           # <p class="title"><b>The Dormouse's story</b></p>
# print(soup.p.name)      # p
# print(soup.p.parent.name) # body
# print(soup.p.string)    # The Dormouse's story
# print(soup.p['class'])  # ['title']
# print(soup.a)
# soup.find(id="link3")   # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
# all_a_tags = soup.find_all('a')
# for a in all_a_tags:
    # print(a['class'])
    # print(a.string)
    # print(a['href'])
    # print(a.get('href'))
    # print(a['id'])
    # print(a.get('id'))

# all_p_tags = soup.find_all('p')
# print(all_p_tags)

# print(soup.get_text())
# obj1 = soup.find('a', id="link1")
# print(obj1.get('href'))
# print(obj1.string)

# obj2 = soup.find('p', _class='story')
# print(obj2)

# ojb3 = soup.find_all('p')
# for p in ojb3:
#     print(p.string)

first_link = soup.a
print(first_link)
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

print(first_link.find_all_next(string=True))
# ['Elsie', ',\n', 'Lacie', ' and\n', 'Tillie',
#  ';\nand they lived at the bottom of a well.', '\n', '...', '\n']

print(first_link.find_next("p"))
# <p class="story">...</p>

first_story_paragraph = soup.find("p", class_="story")
print(first_story_paragraph)
print(first_story_paragraph.find_next_sibling("p"))

# <p class="story">...</p>