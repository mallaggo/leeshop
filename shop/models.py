
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.urls import reverse


class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("이메일은 필수 입니다.")

        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):   #실제 User 테이블의 field들
    email=models.EmailField(blank=True,default='',unique=True)
    name=models.CharField(max_length=200,blank=True,default='')
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)

    is_active=models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined=models.DateTimeField(default=timezone.now) #기본값이며 생성 시 선택, 편집 가능하다. auto_now_add 랑 조금 다르다
    last_login=models.DateTimeField(blank=True,null=True)

    objects=CustomUserManager()   #모든 개체 필드들을 CustomUserManager를 거쳐서 가져온다.

    USERNAME_FIELD='email'   #manage.py createsuperuser 시 name을 email로 대체
    EMAIL_FIELD='email'     #manage.py cratesuperuser 시 이메일
    REQUIRED_FIELDS = []  # 그외 꼭 넣고 싶은 필드들

    class Meta:
        verbose_name='User'          # 모델 이름을 verbose_name에 모델의 복수명을 verbose_name_plural에 적는다.
        verbose_name_plural='Users'  #왼쪽 Users 를 누르면 등록한 유저들의 리스트가 나오는데 또한, 그 필드 이름이 User인 걸 볼 수 있다.

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]  #name 필드에 이름 값을 채우기 전까지는 admin 관리창 우측 상단에 메일의 아이디만 나올 것이다.


class Category(models.Model):
    name=models.CharField(max_length=50,db_index=True,unique=True)
    slug = models.SlugField(max_length=50, unique=True,allow_unicode=True)  # 데이타로 url(주소)만드는 방식을 지원함, unicode...는 한글도 가능하게

    class Meta:
        ordering = ('name',)  # ordering은 반드시 튜플로 즉, 쉼표 잊지 말길, 내림차순은 ('-name',)
        verbose_name = 'category'
        #db_table = 'category'  실제 mysql에서 디폴트로 생성되는<app_name>_테이블명을 원하는 테이블명으로 바꿔주는 역할을 한다.
    def __str__(self):
        return self.name

    def get_absolute_url(self):  # 주로 list에서 해당 아이템(인스턴스)의 detail 정보를 얻는데 사용된다.
        return reverse('shop:product_list_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True,db_index=True)
    slug = models.SlugField(max_length=50, db_index=True,allow_unicode=True)
    image=models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description=models.TextField(blank=True)
    price=models.IntegerField() #decimal_places은 필수로 소수점 설정
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)

    class Meta:
        ordering=('name',)
        models.Index(fields=['id', 'slug'])  #id 단독 검색 혹은 id와 slug를 동시 검색하는데 유리하다. 하지만 slug를 단독 검색하는데는 불리

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100, null=False)
    email=models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    orderitem=models.JSONField()
    orderstatus=(
        ('pending','pending'),
        ('out for shipping','out for shipping'),
        ('completed','completed'),
    )
    #CharField에 choices 옵션을 이용하여 콤보를 만들고 2차원 튜플로 구성하되, 앞에 값이 DB저장 2번째 값은 템플릿에 보여질 값
    status=models.CharField(max_length=150,choices=orderstatus,default='pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)