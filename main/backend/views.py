from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Content,Topic,Profile
from .tasks import testing, testingMulti
from celery.result import AsyncResult
from rest_framework import viewsets
from .serializers import ContentSeralizer,TopicSerializer,UserSerializer
from rest_framework import mixins
from django.http import JsonResponse
from celery.result import AsyncResult
import json
from django.views.decorators.csrf import csrf_exempt
import subprocess
from time import sleep
import os
import uuid
import shutil
from django.contrib.auth.models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
@csrf_exempt
def index(request):
    code = request.body.decode("UTF-8")
    print("code: ",code)
    x = testing.delay(code=code) 
    taskid = json.dumps(x.id)
    return JsonResponse(json.loads(taskid), status=201, safe=False)

@csrf_exempt
def multiFile(request):
    json_data = json.loads(request.body)
    itemList = []
    for item in json_data:
        itemList.append([item['label'],item['code']])
    x = testingMulti.delay(itemList=itemList) 
    taskid = json.dumps(x.id)
    return JsonResponse(json.loads(taskid), status=201, safe=False)

def checkResult(request, task_id):
    res = AsyncResult(task_id)
    status = res.status
    result = str(res.result)
    output = {'status': status, 'result': result}
    outputJSON = json.dumps(output)
    print(outputJSON)
    return JsonResponse(data= {'status': 'true', 'output':json.loads(outputJSON)}, status=201, safe=False)

def singleFile(request):
    id = str(uuid.uuid4())
    path = os.path.abspath(id)
    os.mkdir(path)
    content = 'from time import sleep\nx = 9\nfor i in range(x):\n    print(i)\n    sleep(i)'
    filePath = path + "/code.py"
    with open(filePath, 'a') as the_file:
        the_file.write(content)
    pathForShell = f'"{path}"'
    command = f'docker run -d -v {pathForShell}:/the/workdir/path newbackend'
    process = subprocess.check_output(command,shell=True)
    process = process.decode("UTF-8").strip()
    command1 = f'docker ps -a --filter "id={process}"'
    statusStr = ""
    while "Exited" not in statusStr:
        sleep(1)
        print("LOOP")
        statusStr = subprocess.check_output(command1,shell=True).decode("UTF-8")
        if "Exited" in statusStr:
            print("YES!")
            command2 = 'docker logs ' + process 
            res = subprocess.check_output(command2,shell=True).decode("UTF-8")
            outputJSON = json.dumps(res)
            print(outputJSON)
            shutil.rmtree(path)
            return JsonResponse(data= json.loads(outputJSON), status=201, safe=False)


def multipleFile(request):
    id = str(uuid.uuid4())
    path = os.path.abspath(id)
    os.mkdir(path)
    # content = [['code.py','from time import sleep\nfrom test import helloworld\nhelloworld()\nx = 9\nfor i in range(x):\n    print(i)\n    sleep(i)'],['test.py','def helloworld():\n    print("I am in this world poggers")']]
    #codeCode = r'from test import function2\n' + r'def function1():\n' + r'  print("I am a function in file 1!")\n' + r'\n' + r'if name == "main":\n' + r'  function2()'
    #testCode = r'from code import function1\n' + r'def function2():\n' + r'  print("I am a function in file 2!")\n' + r'\n' + r'if name == "main":\n' + r'  function1()'
    # codeCode = 'from test import function2\n' + 'def function1():\n' + '  print("I am a function in file 1!")\n' + '\n' + 'if name == "__main__":\n' + '  function2()'
    # testCode = 'from code import function1\n' + 'def function2():\n' + '  print("I am a function in file 2!")\n' + '\n' + 'if name == "__main__":\n' + '  function1()'
    codeCode = 'from test import function_three\n' + 'print("File one __name__ is set to: {}" .format(__name__))\n' +'def function_one():\n' +'   print("Function one is executed")\n' + 'def function_two():\n' +'   print("Function two is executed")\n' +'if __name__ == "__main__":\n' +'   print("File one executed when ran directly")\n' +'   function_two()\n' +'   function_three()\n' +'else:\n' +'   print("File one executed when imported")'
    testCode = 'print("File two __name__ is set to: {}" .format(__name__))\n' + 'def function_three():\n' +'   print("Function three is executed")\n' +'def function_four():\n' +'   print("Function four is executed")\n' +'if __name__ == "__main__":\n' +'   print("File two executed when ran directly")\n' +'else:\n' +'   print("File two executed when imported")\n'
    content = [['code.py',codeCode],['test.py',testCode]]
    for i in content:
        filePath = path + "/" + i[0]
        with open(filePath, 'a') as the_file:
            the_file.write(i[1])
    pathForShell = '"' + path + '"'
    command = 'docker run -d -v ' + pathForShell + ':/the/workdir/path newbackend'
    process = subprocess.check_output(command,shell=True)
    process = process.decode("UTF-8").strip()
    command1 = 'docker ps -a --filter "id=' + process + '"'
    statusStr = ""
    while "Exited" not in statusStr:
        sleep(1)
        print("LOOP")
        statusStr = subprocess.check_output(command1,shell=True).decode("UTF-8")
        if "Exited" in statusStr:
            print("YES!")
            command2 = 'docker logs ' + process 
            res = subprocess.check_output(command2,shell=True).decode("UTF-8")
            outputJSON = json.dumps(res)
            print(outputJSON)
            shutil.rmtree(path)
            return JsonResponse(data= json.loads(outputJSON), status=201, safe=False)



class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSeralizer
    queryset = Content.objects.all()


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    def get_queryset(self):
        topic = Topic.objects.all()
        return topic

def profile_list(request, username):
    userid = User.objects.get(username=username).id
    profiles = Profile.objects.get(user_id=userid)
    print(profiles)
    # newCompleted = profiles.completed
    # newCompleted.append(10)
    # profiles.completed = newCompleted
    # profiles.save()

    return JsonResponse(data= json.loads(str(profiles.completed)), status=201, safe=False)


@csrf_exempt
def appendCompleted(request):
    json_data = json.loads(request.body)
    print("username: ", json_data["username"])
    print("contentid: ", json_data["contentid"])
    userid = User.objects.get(username=json_data["username"]).id
    profiles = Profile.objects.get(user_id=userid)
    newCompleted = profiles.completed
    print("before: ", profiles.completed)
    newCompleted.append(json_data["contentid"])
    profiles.completed = newCompleted
    print("after: ", profiles.completed)
    profiles.save()
    return HttpResponse(status = 201)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
