from django.shortcuts import render

# Create your views here.
def renderTemplate(request):
    myDict = {"name": "Superman"}
    return render(request, 'templatesApp/firstTemplate.html', context=myDict)


def renderEmployee(request):
    myDict = {"id": 1234, "name": "John", "salary": 100000}
    return render(request, 'templatesApp/employeeTemplate.html', context=myDict)
