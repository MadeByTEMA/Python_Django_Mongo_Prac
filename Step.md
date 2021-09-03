# Python Django Framework & Mongo DB Practice  
  
## Django  

Django란 Python Web Server Framework이다.    
다른 frame work의 경우 MVC(Model-View-Controller)의 디자인 패턴을 적용하는데 반해,  
Django는 MTV(Model-Template-View)의 구조를 가진다.  

### Django MTV 
HTTP Request        →   urls(urls.py)  
                            ↓  
model(models.py)    ↔   view(views.py)  →   Response  
                            ↑  
                        template(html)  

MVC모델의 경우 각각의 구성 요소가 다른 요소들에게 영향을 미치지 않아야 한다.  
Model(모델) : 데이터를 가지고 있으며, 데이터를 처리하는 로직

  
### Practice Setting
OS          : window 10  
Python      : 3.9.6  
Django      : 3.2.6  
MongoDB     : 5.0.2  
IDE         : PyCharm  

Django 설치  
$ pip install Django==3.2.6  
$ pip install djangorestframework

MongoDB 설치 (Django)  
$ pip install djongo

CORS 설치 (API 통신)  
$ pip install django-cors-headers


    
Server Run
$ python manage.py runserver  
+ python manage.py runserver 8020  
+ 위와 같이 포트를 변경할 수 있다.(ex 8020)  
http://localhost:8020/

  
### Django basic file
settings.py
+ 데이터 베이스 설정, 템플릿 항목 설정, 정적 파일 항목 설정, 애플리케이션 등록, 타임존 지정 등 수정

models.py
+ DB에서 가져온 data를 클래스화 하는 모델

urls.py
+ URL과 View를 매핑해준다.

views.py
+ Logic 담당

## Django Super User
$ python manage.py createsuperuser
 + superuser 계정 만들기


## Django Project Create  

$ django-admin startproject web_prac  
 + project 생성  

$ cd web_prac  

$ python manage.py startapp rest_api  
 + rest api 호출을 위한, rest_api라는 폴더를 만듬(app명 변경해도 됨)  

## rest API 설정 (settings.py에 추가)
INSTALLED_APPS = []에 아래 추가
'rest_framework',
'rest_api.apps.RestApiConfig',  
 + rest_framework : rest api 사용을 위해 추가해주어야 하고,  
 + rest_api.apps.RestApiConfig : 위에 rest_api라는 폴더로 start를 했기 때문에, 그 폴더 안에 apps.py 안에 RestApiConfig라는 이미 만들어져 있는 함수를 setting에 추가해준다.  


## TIME ZONE & 언어 설정 (settings.py)
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'  

## 포트 관련 설정 (settings.py에 추가)  
MIDDLEWARE = [] 에 아래 추가  
CORS_ORIGIN_ALLOW_ALL = False  
CORS_ORIGIN_WHITELIST = (  
    'http://localhost:8020',  
)  
+ CORS_ORIGIN_ALLOW_ALL : True면 모든 포트 허용  
+ CORS_ORIGIN_WHITELIST : 해당 포트로 오는 request는 허용  

## DB연결(mongo DB)  
DATABASES = {  
    'default': {  
        'ENGINE': 'djongo',  
        'NAME': 'test_db',  
        'HOST': '127.0.0.1',  
        'PORT': 27017,  
    }  
}    

## models.py 작성
rest_api 안의 models에 model을 작성한 후, migrations을 생성 해준다.

from django.db import models

class Tutorial(models.Model):  
    title = models.CharField(max_length=70, blank=False, default='')  
    description = models.CharField(max_length=200,blank=False, default='')  
    published = models.BooleanField(default=False)  

## migrations 생성(models.py 작성 후)  
$ python manage.py makemigrations rest_api  
이후 rest_api 폴더 안에 migrations 폴더에 파일이 생성된 것을 확인할 수 있다.  
make migrations가 완료된 것이다.  

$ python manage.py migrate rest_api  
migrations을 생성했으면, 이제 migration을 해준다.  


## serializer를 통해 model 관리 (migration 끝낸 후)  
rest_api 폴더 안에 serializer.py를 생성  

from rest_framework import serializers  
from rest_api.models import Tutorial  


class TutorialSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Tutorial  
        fields = ('id',  
                  'title',  
                  'description',  
                  'published')  


## urls 설정
url 예시는 다음과 같이 할 예정  
ex)  
/api/tutorials: GET, POST  
/api/tutorials/:id: GET, POST  
/api/tutorials/published: GET  

rest_api 폴더 안에 urls.py를 아래와 같이 작성한다.

from django.conf.urls import url   
from rest_api import views   
 
urlpatterns = [   
    url(r'^api/tutorials$', views.tutorial_list),  
    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),  
    url(r'^api/tutorials/published$', views.tutorial_list_published)  
]  

또한 project 자체의 urls.py도 수정한다. (Python_Django_Mongo_Prac 안에 urls.py)

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('rest_api.urls')),
]

## view 설정
rest_api안의 views.py도 아래와 같이 수정한다.  

from django.shortcuts import render

from django.http.response import JsonResponse  
from rest_framework.parsers import JSONParser   
from rest_framework import status  
 
from rest_api.models import Tutorial  
from rest_api.serializers import TutorialSerializer  
from rest_framework.decorators import api_view  

@api_view(['GET', 'POST'])  
def tutorial_list(request):  
    if request.method == 'GET':  
        tutorials = Tutorial.objects.all()
        title = request.GET.get('title', None)  
        if title is not None:  
            tutorials = tutorials.filter(title__icontains=title)
        tutorials_serializer = TutorialSerializer(tutorials, many=True)  
        return JsonResponse(tutorials_serializer.data, safe=False)  
        # 'safe=False' for objects serialization  
    elif request.method == 'POST':  
        tutorial_data = JSONParser().parse(request)  
        tutorial_serializer = TutorialSerializer(data=tutorial_data)  
        if tutorial_serializer.is_valid():  
            tutorial_serializer.save()  
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)   
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])  
def tutorial_detail(request, pk):  
    try:   
        tutorial = Tutorial.objects.get(pk=pk)   
    except Tutorial.DoesNotExist:   
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':   
        tutorial_serializer = TutorialSerializer(tutorial)   
        return JsonResponse(tutorial_serializer.data)
    elif request.method == 'POST':   
        tutorial_data = JSONParser().parse(request)   
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)   
        if tutorial_serializer.is_valid():   
            tutorial_serializer.save()   
            return JsonResponse(tutorial_serializer.data)   
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])  
def tutorial_list_published(request):  
    tutorials = Tutorial.objects.filter(published=True)
    if request.method == 'GET':   
        tutorials_serializer = TutorialSerializer(tutorials, many=True)  
        return JsonResponse(tutorials_serializer.data, safe=False)  

## TEMPLATES 사용 
setting.py안에 TEMPLATES = [] 안에 'DIRS' 안에 아래와 같이 수정한다.
'DIRS': [os.path.join(BASE_DIR, 'templates')],

STATIC 파일을 수동으로 지정해주기 위해서 setting.py안에 STATICFILES_DIRS을 아래와같이 추가한다.  
STATIC_URL = '/static/'  
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  


## media 루트 추가 (파일 사용 시 등을 위해)  
setting.py안에 media 루트를 추가한다.(media외 다른 이름으로 다른 용도로 사용 해도 상관 없다.)  
MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  

