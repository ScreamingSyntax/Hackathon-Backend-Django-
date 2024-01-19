
from django.contrib import admin
from django.urls import path,include
from user import urls as user_urls
from product import urls as product_urls
from django.conf import settings
from chat import urls as chat_urls

from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user_urls),        ),
    path('products/',include(product_urls),),

     path('chatbot/',include(chat_urls),        ),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)