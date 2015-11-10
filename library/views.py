from django.shortcuts import render
from django.shortcuts import render_to_response
from library.models import Book, Author
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Create your views here.

def index(request):
	return render_to_response('index.html')

def insertbook(request):
    is_book = False
    if request.method == "POST":
        isbn = request.POST["ISBN"]
        title = request.POST["Title"]
        authorid = request.POST["AuthorID"]
        publisher = request.POST["Publisher"]
        publishdate = request.POST["PublishDate"]
        price = request.POST["Price"]
        try:
            Book.objects.get(ISBN = isbn)
        except:
            try:
                Author.objects.get(AuthorID = authorid)
            except:
                return render_to_response("insertauthor.html",{'isbn':isbn,"title":title,
                                                            "publisher":publisher,"price":price,
                                                            "authorID":authorid,"publishdate":publishdate})
            else:
                newbook = Book(ISBN = isbn,
                            Title = title,
                            AuthorID = Author.objects.get(AuthorID = authorid),
                            Publisher = publisher,
                            PublishDate = publishdate,
                            Price = price)
                newbook.save()
                return  HttpResponseRedirect("/booklist/")
        else:
            is_book = True
    return render_to_response("insertbook.html",{"is_book":is_book})

def insertauthor(request):
    if request.method == "POST":
        authorID = request.POST["AuthorID"]
        newauthor = Author(AuthorID = request.POST["AuthorID"],
                           Name = request.POST["Name"],
                           Age = request.POST["Age"],
                           Country = request.POST["Country"])
        newauthor.save()
        newbook = Book(ISBN = request.POST["ISBN"],
                       Title = request.POST["Title"],
                       AuthorID = Author.objects.get(AuthorID = authorID),
                       Publisher = request.POST["Publisher"],
                       PublishDate = request.POST["PublishDate"],
                       Price = request.POST["Price"])
        newbook.save()
        return  HttpResponseRedirect("/booklist/")
    return render_to_response("insertauthor.html")

def booklist(request):
    books = Book.objects.all()  
    for book in books:
        book.PublishDate = str(book.PublishDate)
        book.AuthorID.Age = str(book.AuthorID.Age)
    return render_to_response("library.html",{"books":books})
def update	(request,key):
    book = Book.objects.get(ISBN = key)
    item = book
    if request.method == "POST":
        isbn = request.POST["ISBN"]
        title = request.POST["Title"]
        publisher = request.POST["Publisher"]
        publishdate = request.POST["PublishDate"]
        price = request.POST["Price"]
        authorid = request.POST["AuthorID"]
        book.ISBN = isbn
        book.Title = title
        book.Publisher = publisher
        book.PublishDate = publishdate
        book.Price = price
        book.save()
        try:
            Author.objects.get(AuthorID = authorid)
        except:
            return render_to_response("updateauthor.html",{"title":title,"authorID":authorid,"author_exist":False})
        else:
            author = Author.objects.get(AuthorID = authorid)
            return render_to_response("updateauthor.html",{"title":title,"authorID":authorid,"author_exist":True,"Age":author.Age.strftime('%Y-%m-%d'),"author":author})
    
    return render_to_response("update.html",{"item":item,"PublishDate":item.PublishDate.strftime('%Y-%m-%d')})
def updateauthor(request):
    if request.method == "POST":
        title = request.POST["Title"]
        authorid = request.POST["AuthorID"]
        name = request.POST["Name"]
        age = request.POST["Age"]
        country = request.POST["Country"]
        
        try:
            Author.objects.get(AuthorID = authorid)
        except:
            newauthor = Author(AuthorID = authorid,
                           Name = name,
                           Age = age,
                           Country = country)
            newauthor.save()
            Book.objects.filter(Title = title).update(AuthorID = newauthor)
            return  HttpResponseRedirect("/booklist/")
        else:
            author = Author.objects.get(AuthorID = authorid)
            author.Name = name
            author.Age = age
            author.Country = country
            author.save()
            Book.objects.filter(Title = title).update(AuthorID = author)
            return  HttpResponseRedirect("/booklist/")
def delete(request,key):
    book = Book.objects.get(ISBN = key)
    book.delete()
    return  HttpResponseRedirect("/booklist/")
def search(request):
    if request.method == "GET":
        author = request.GET["search"]
        booklist = Book.objects.filter(AuthorID = Author.objects.filter(Name = author))
        try:
            Author.objects.get(Name = author)
        except:
            is_author = False
            return render_to_response("searchresult.html",{"booklist":booklist,"author":author,"is_author":is_author})
        else:
            is_author = True
            return render_to_response("searchresult.html",{"booklist":booklist,"author":author,"is_author":is_author})


    