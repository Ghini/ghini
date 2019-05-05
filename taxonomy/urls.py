from django.urls import path
from .views import (RankList, RankDetail,
                    TaxonList, TaxonDetail, TaxonInfobox,
                    index)


urlpatterns = [
    path("taxa/", TaxonList.as_view(), name="taxon-list"),
    path("taxa/<int:pk>/", TaxonDetail.as_view(), name="taxon-detail"),
    path("taxa/<int:pk>/infobox/", TaxonInfobox.as_view(), name="taxon-infobox"),
    path("ranks/", RankList.as_view(), name="rank-list"),
    path("ranks/<int:pk>/", RankDetail.as_view(), name="rank"),
    #path("ranks/<int:pk>/infobox/", RankInfobox.as_view(), name="rank-infobox"),
    #path("taxa/<int:pk>/subtaxa/", SubTaxa.as_view(), name="subtaxa"),
]
