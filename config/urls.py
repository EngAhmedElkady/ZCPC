
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework.schemas import get_schema_view
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions # new
from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi # new

schema_view = get_schema_view( # new
    openapi.Info(
    title="ZCPC API",
    default_version="v1",
    description="""
    An ICPC Platform System is software built to handle the primary main functions of an ICPC. Platforms rely on communities and famous road maps. The platform system helps members to train on the open rounds for any community and helps leaders to create communities, as well as members’ subscriptions and profiles.

ICPC Platform systems also involve full automation functions that help communities to follow up the levels for the members like as:

 - Email after each week with the top member
 - Remove a member from the round ( you will put the constraints like as who solved less than 60% from the sheet will remove)
 - After the end week, the system will write a post on your page on Facebook to the top 10 with photos (the community saves the design only on the database)
 - All members will receive an email with an analysis after each round
    """,
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="icpczagazig2020@gmail.com"),
    license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth', include('rest_framework.urls')),
    path("account/", include('modules.accounts.urls')),
    path('', include('modules.community.urls')),
    path('', include('modules.round.urls')),
    path('', include('modules.level.urls')),
    path('', include('modules.content.urls')),
    path('blog/', include('modules.blog.urls')),

   path('', schema_view.with_ui( # new
    'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui( # new
    'redoc', cache_timeout=0), name='schema-redoc'),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

