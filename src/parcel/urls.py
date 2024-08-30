from rest_framework.routers import DefaultRouter

from parcel.views import AddressViewSet, ArticleViewSet, UserShipmentViewSet


router = DefaultRouter()

router.register("addresses", AddressViewSet)
router.register("articles", ArticleViewSet)
router.register("user-shipments", UserShipmentViewSet)

urlpatterns = router.urls
