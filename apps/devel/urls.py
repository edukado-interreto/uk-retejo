from django.urls import path
from apps.devel import views


def not_implemented(request):
    raise NotImplementedError


urlpatterns = [
    path("checkcode", views.checkcode),
    path("loaddata", views.loaddata),
    path("getRegistration", views.get_registration),
    path("participants", views.participants),
    path("saveform", views.saveform),
    path("directpayment", views.directpayment),
    path("invitation", views.invitation),
    path("clearcache", views.clearcache),
    path("query", views.query),
    path("confirmparticipations", views.confirmparticipations),
    path("checkmembersdata", views.checkmembersdata),
    path("updatediscountlist", views.updatediscountlist),
    path("kongresanoj.num", views.kongresanoj_num),
    path("admin/login", views.login),
    path("admin/getcache", views.getcache),
    path("admin/deletecachefile", views.deletecachefile),
    path("admin/getchangestoconfirm", views.getchangestoconfirm),
    path("admin/previewchangeconfirmationemail", views.previewchangeconfirmationemail),
    path("admin/sendchangeconfirmationemails", views.sendchangeconfirmationemails),
    path("admin/registermanually", views.registermanually),
]
