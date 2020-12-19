from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
import requests 
import json
import bcrypt
def index(request):
    # POST 통신인 경우 : 로그인 폼을 작성한 경우
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        # 로그인 API 호출 -> 토큰발행
        r = requests.post('http://127.0.0.1:7000/api/auth/login',{'username':username,'password':password})

        print('상태코드',r.status_code)
        print('토큰',r.json().get("token"))

        token=[]
        token.append('Bearer ')
        
        if r.json().get("token"):
            
            token.append(r.json().get("token"))         
            token=''.join(token)
            headers = {'Authorization': token}
            
            # 인증해야 볼 수 있는 게시글 목록 접근
            # API 호출
            r2=requests.get('http://127.0.0.1:7000/api/contacts',headers=headers)
            print('상태코드2',r2.status_code)
            #print('헤더2',r2.headers)
            print('제이선2',r2.json())
            boards=r2.json()

            response=render(request,'boardlist.html',{'boards':boards})
            

            # 관리자라면
            if request.POST.get("username")=='administer':
                admin='administer'
                age=60
                # API 호출
                r2=requests.get('http://127.0.0.1:7000/api/auth/admin',headers=headers)
                print('제이선2',r2.json())
                userlist=r2.json()
                response=render(request,'boardlist.html',{'userlist':userlist,'admin':admin})
                response.set_cookie('admin_cookie','administer',max_age=age)
                response.set_cookie('demo_cookie',r.json().get("token"),max_age=age)
                return response
                
                
            else:
                admin=None
                age=60
                response.set_cookie('demo_cookie',r.json().get("token"),max_age=age)
                return response

        else:
            response=render(request,'index.html')
            return response

    else: # GET 통신인 경우
        demo_cookie=None
        if 'demo_cookie' in request.COOKIES:
            demo_cookie=request.COOKIES['demo_cookie']
 
            token2=[]
            token2.append('Bearer ')
            token2.append(demo_cookie)         
            token2=''.join(token2)
            headers = {'Authorization': token2}

            # 인증해야 볼 수 있는 게시글 목록 접근
            # API 호출
            r2=requests.get('http://127.0.0.1:7000/api/contacts',headers=headers)
            #print('상태코드2',r2.status_code)
            #print('헤더2',r2.headers)
            print('제이선2',r2.json())
            boards=r2.json()
            admin=None
            # 관리자 계정일때
            if 'admin_cookie' in request.COOKIES:
                admin='administer'
                token2=[]
                token2.append('Bearer ')
                token2.append(demo_cookie)         
                token2=''.join(token2)
                headers = {'Authorization': token2}

                # API 호출
                r2=requests.get('http://127.0.0.1:7000/api/auth/admin',headers=headers)
                print('제이선2',r2.json())
                userlist=r2.json()
                return render(request,'boardlist.html',{'userlist':userlist,'admin':admin})
            else:
                admin=None
            response=render(request,'boardlist.html',{'boards':boards,'admin':admin})
            return response
        else :
            # demo_cookie=None
            return render(request,'index.html')
        
        
def signup(request):
    # POST 통신인 경우 : 회원가입 폼을 작성한 경우
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")

        # 이메일 인증 받기

        # 이메일 인증 후 API Register 호출
        r = requests.post('http://127.0.0.1:7000/api/auth/register',
            {'username':username,'password':password,'email':email,'first_name':firstname,'last_name':lastname})
        print('상태코드',r.status_code)
        print('헤더',r.headers['content-type'])
        print('인코딩',r.encoding)
        print('텍스트',r.text)
        print('제이선',r.json())
        #return render(request,'signup.html')
        return HttpResponseRedirect('/')
    else: # GET 통신인 경우
        return render(request,'signup.html')

def delete(request):
    if request.method=='POST':
        print('왔다=====================================')
        if 'demo_cookie' in request.COOKIES:
            print('또왔다=====================================')
            demo_cookie=request.COOKIES['demo_cookie']
        
            token2=[]
            token2.append('Bearer ')
            token2.append(demo_cookie)         
            token2=''.join(token2)
        
            headers = {'Authorization': token2}


            username=request.POST.get("username")
            

            
            r2=requests.delete('http://127.0.0.1:7000/api/auth/'+username,headers=headers)
            print('결과쓰ㅠㅠㅠ==================================',r2.status_code)
    return HttpResponseRedirect('boardlist')

def boardlist(request):
    demo_cookie=None
    if 'demo_cookie' in request.COOKIES:
        demo_cookie=request.COOKIES['demo_cookie']
 
        token2=[]
        token2.append('Bearer ')
        token2.append(demo_cookie)         
        token2=''.join(token2)
        headers = {'Authorization': token2}

        # 인증해야 볼 수 있는 게시글 목록 접근
        # API 호출
        r2=requests.get('http://127.0.0.1:7000/api/contacts',headers=headers)
        #print('상태코드2',r2.status_code)
        #print('헤더2',r2.headers)
        print('제이선2',r2.json())
        boards=r2.json()
        admin=None
        # 관리자 계정일때
        if 'admin_cookie' in request.COOKIES:
            admin='administer'
            token2=[]
            token2.append('Bearer ')
            token2.append(demo_cookie)         
            token2=''.join(token2)
            headers = {'Authorization': token2}

            # API 호출
            r2=requests.get('http://127.0.0.1:7000/api/auth/admin',headers=headers)
            print('제이선2',r2.json())
            userlist=r2.json()
            return render(request,'boardlist.html',{'userlist':userlist,'admin':admin})
        else:
            admin=None
            response=render(request,'boardlist.html',{'boards':boards,'admin':admin})
            return response
    else :
        # demo_cookie=None
        return HttpResponseRedirect('/')

def edit(request):
    if request.method=='GET':
        return HttpResponseRedirect('/')

    else:
        # 폼 입력 정보 받아오기
        username=request.POST.get("username")

        #유저 정보 갱신 api 호출
        print('왔다=====================================')
        if 'demo_cookie' in request.COOKIES:
            print('또왔다=====================================')
            demo_cookie=request.COOKIES['demo_cookie']
        
            token2=[]
            token2.append('Bearer ')
            token2.append(demo_cookie)         
            token2=''.join(token2)
        
            headers = {'Authorization': token2}
            # API 호출
            r2=requests.get('http://127.0.0.1:7000/api/auth/'+username,headers=headers)
            print('제이선2222222222222222',r2.json())
            user=r2.json()
            return render(request,'edit.html',{'user':user})
            
        else:
            admin=None
            
            return HttpResponseRedirect('/')

def update(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    firstname=request.POST.get("firstname")
    lastname=request.POST.get("lastname")
    password=request.POST.get("password")
    print('zzzzzzzzzz')
    print(username,'-',email,'=',firstname,'-',lastname,'-',password)
    # 이메일 인증 후 API Register 호출\
    if 'demo_cookie' in request.COOKIES:
        print('또왔다=====================================')
        demo_cookie=request.COOKIES['demo_cookie']
        
        token2=[]
        token2.append('Bearer ')
        token2.append(demo_cookie)         
        token2=''.join(token2)
        
        headers = {'Authorization': token2}
    
        r = requests.patch('http://127.0.0.1:7000/api/auth/'+username,
            {
                'username': username,
                'first_name': firstname,
                'last_name': lastname,
                'email': email,
                'password': password


            },
            headers=headers)
        print('하',username)
        print('어케됨???',r.status_code)
        return HttpResponseRedirect('boardlist')
    else:
        return HttpResponseRedirect('/')


