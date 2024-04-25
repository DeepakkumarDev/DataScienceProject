from authorization.viewsets import ProfileViewset,FileViewset,DataUploadViewset
from core.viewsets import UserViewset
from rest_framework import routers




router=routers.DefaultRouter()
router.register('profile',ProfileViewset)

router.register('users',UserViewset)
router.register('files',FileViewset)
router.register('data',DataUploadViewset)