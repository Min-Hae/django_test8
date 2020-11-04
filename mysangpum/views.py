from django.shortcuts import render
from mysangpum.models import Sangdata
import MySQLdb
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def MainFunc(request):
    return render(request, 'main.html')
    
def ListFunc(request):
    '''    
    #sql문 사용
    config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
    }
    conn = MySQLdb.connect(**config)
    sql = "select * from sangdata"
    cursor = conn.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    print(type(datas)) # tuple
    '''
    
    #장고의 ORM 지원메소드 사용
    ''' 페이징처리가 없는 경우
    datas = Sangdata.objects.all() 
    #print(type(datas)) # django.db.models.query.QuerySet
    
    return render(request, 'list.html', {'sangpums':datas})
    '''
    # 페이지 나누기 ----------
    datas = Sangdata.objects.all().order_by('-code') 
    paginator = Paginator(datas, 3) # 한 페이지 당 3행씩 출력
    
    try:
      page = request.GET.get('page')
      
      
    except :    
      page = 1
      
      
    try:
        data = paginator.page(page)
    except PageNotAnInteger : # page 변수가 정수가 아닐 때  
        data = paginator.page(1)   
        
    except EmptyPage: # page가 받아지지 않은 경우
        data = paginator.page(paginator.num_pages())
        
    # 개별 페이지 표시용
    allpage = range(paginator.num_pages + 1)
    
        
    return render(request, 'list2.html', {'sangpums':data, 'allpage':allpage})           
        
def InsertFunc(request):    
    return render(request, 'insert.html')

def InsertOkFunc(request):    
    if request.method == 'POST' :
        #code = request.POST.get("code") ==> 이런 방식으로 가능
        
        # 자료 검증 생략
        # insert into sangdata ... 가능.
         
        Sangdata(
           code = request.POST.get("code"),
           sang = request.POST.get("sang"),
           su = request.POST.get("su"),
           dan = request.POST.get("dan") ,
        ).save()
        return HttpResponseRedirect('/sangpum/list')
        
      
        
        
def UpdateFunc(request):    
    data = Sangdata.objects.get(code = request.GET.get('code'))
    return render(request, 'update.html', {'sang_one':data})

def UpdateOkFunc(request):    
    if request.method == 'POST':
        # update sangdata set ...
        updateRec = Sangdata.objects.get(code = request.POST.get('code'))
   #     updateRec.code = request.POST.get('code')
        updateRec.sang = request.POST.get('sang')
        updateRec.su = request.POST.get('su')
        updateRec.dan = request.POST.get('dan')
        updateRec.save()
        
        return HttpResponseRedirect('/sangpum/list') #  수정 후 상품보기
    
def DeleteFunc(request):    
    delRec = Sangdata.objects.get(code = request.GET.get('code'))
    delRec.delete()
    return HttpResponseRedirect('/sangpum/list') # 삭제 후 상품보기