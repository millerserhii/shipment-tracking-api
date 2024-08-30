from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from parcel.models import Address, Article, UserShipment


for model in [Address, Article, UserShipment]:
    admin.site.register(model, SimpleHistoryAdmin)
