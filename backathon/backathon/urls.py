
from django.contrib import admin
from django.urls import path,include
from user import urls as user_urls
from product import urls as product_urls
from post import urls as post_urls
from events import urls as event_urls
from django.conf import settings
from django.conf.urls.static import static
from purchase import urls as purchase_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user_urls),        ),
    path('products/',include(product_urls),),
    path('post/',include(post_urls),),
    path('events/',include(event_urls),),
    path('purchase/',include(purchase_urls),),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)