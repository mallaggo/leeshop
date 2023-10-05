from django.contrib import admin

from .models import User, Category,Product,Order

admin.site.register(User)
admin.site.register(Order)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available', #관리자모드에서 보여질 리스트
                    'created','updated']
    list_filter = ['available','created','updated'] #관리자모드 오른쪽을 보면 필터 목록으로 나옴
    list_editable = ['price','available']  #인스턴스 클릭 후 들어가서 수정하지 않고 바로 수정가능
    prepopulated_fields = {'slug': ('name',)} #name 필드를 이용해 자동으로 슬러그 필드를 채움