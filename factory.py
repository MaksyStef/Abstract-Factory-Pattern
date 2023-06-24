from abc import ABC, abstractmethod

class Book:
  def __init__(self, title, author, **kwargs):
    self.title = title
    self.author = author
    self.__dict__.update(kwargs)

  def __repr__(self):
    return "<Book %s: %s>" % (self.author.name, self.title)


class Author:
  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return "<Author %s, %s>" % (self.name, self.email)


class BookFactory(ABC):
  books = []

  def create_book(self, title, author):
    book = Book(title, author)
    self.books.append(book)
    return book

  def retrieve_book(self, title):
    try:
      return list(filter(lambda book: book.title == title, self.books))[0]
    except IndexError:
      return None


class AuthorFactory(ABC):
  authors = []

  def create_author(self, name, email):
    author = Author(name, email)
    self.authors.append(author)
    return author

  def retrieve_author(self, name):
    try:
      return list(filter(lambda author: author.name == name, self.authors))[0]
    except IndexError:
      return None

  def retrieve_books(self, author, book_factory: BookFactory):
    books = [book if book.author == author else None for book in book_factory.books]
    return books if len(books) > 0 else None


class CousineBookFactory(BookFactory):
  recipes = set([])

  def create_book(self, title, author, *recipes):
    book = Book(title, author, recipes=recipes)
    self.books.append(book)
    self.recipes.add(book)
    return book

  def retrieve_books_by_recipes(self, *recipes):
    books = set([])
    for book in self.books:
      if any(map(lambda recipe: recipe in book.recipes, recipes)):
        books.add(book)
    return books if len(books) > 0 else None

  
class CousineAuthorFactory(AuthorFactory):

  def retrieve_authors_by_recipes(self, book_factory: CousineBookFactory, *recipes):
    books = book_factory.retrieve_books_by_recipes(*recipes)
    authors = set(map(lambda book: book.author, books))
    return authors if len(authors) > 0 else None

if __name__ == '__main__':
  book_factory = CousineBookFactory()
  author_factory = CousineAuthorFactory()

  a = author_factory.create_author('Alex', 'alex@gmail.com')
  b1 = book_factory.create_book('How to cook Vol 1', a, 'Lasagna')
  b2 = book_factory.create_book('How to cook Vol 2', a, 'Cheese Lasagna')
  b3 = book_factory.create_book('How to cook Vol 3', a, 'Cheese Lasagna', 'Lasagna')

  print('Get author by name:', author_factory.retrieve_author('Alex'))
  print('Get book by title:', book_factory.retrieve_book('How to cook Vol 1'))
  print('Get author by recipes:', author_factory.retrieve_authors_by_recipes(book_factory, 'Lasagna'))
  print('Get books by recipes:', book_factory.retrieve_books_by_recipes('Lasagna'))