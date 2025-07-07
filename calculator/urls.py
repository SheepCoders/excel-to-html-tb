from django.urls import path
from calculator.views import (
    CombinedActivityIndicatorView,
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    MeasurementCreateView,
    MeasurementUpdateView,
    MeasurementDeleteView
)

urlpatterns = [
   path("",
        CombinedActivityIndicatorView.as_view(),
        name="activity_list"),
   path(
        "activity/create/",
        ActivityCreateView.as_view(),
        name="activity_create"
   ),
    path(
        "activity/<int:pk>/delete/",
        ActivityDeleteView.as_view(),
        name="activity_delete"
    ),
    path(
        "activity/<int:pk>/update/",
        ActivityUpdateView.as_view(),
        name="activity_update"
    ),
    path(
        "measurement/create/",
        MeasurementCreateView.as_view(),
        name="measurement_create"
   ),
    path(
        "measurement/<int:pk>/update/",
        MeasurementUpdateView.as_view(),
        name="measurement_update"
   ),
    path(
        "measurement/<int:pk>/delete/",
        MeasurementDeleteView.as_view(),
        name="measurement_delete"
   ),
]

app_name = "calculator"
