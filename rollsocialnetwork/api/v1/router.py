"""
api.v1 router
"""
from rest_framework import routers
from .views import (
    SitesViewset,
    UsersViewset,
)

router = routers.DefaultRouter()
router.register(r'sites', SitesViewset)
router.register(r'users', UsersViewset)
