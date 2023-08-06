
from django.urls import path
from .views import (AddCWEandCVE,
                    DNSSearcherView,
                    CVESearchView,
                    CensysHostSearchView,
                    ListVendors,
                    LocalView,
                    login_required_view,
                    CWETop25,
                    CWEData,
                    CWEAllView,
                    CWEDetailsAllView,
                    CVEDetailsAllView,
                    WindowsHardwareView,
                    WindowsRegistryView,
                    NetworkLocalView,
                    SearcherView)

urlpatterns = [
    path('cve/all/<str:page>', CVEDetailsAllView.as_view(), name="cve_all"),
    path('cve/<str:code>', CVESearchView.as_view(), name="get_by_cve"),

    path('cwe', CWETop25.as_view(), name="cwe_top_25"),
    path('cwe/all', CWEAllView.as_view(), name="cwe_all"),
    path('cwe/all/<str:page>', CWEDetailsAllView.as_view(), name="cwe_all_details"),
    path('cwe/add', AddCWEandCVE.as_view(), name="cwe_add"),
    path('cwe/<str:id_cwe>', CWEData.as_view(), name="get_by_cwe"),

    path('list_vendors', ListVendors.as_view()),

    path('censys/<str:ip_address>', CensysHostSearchView.as_view(), name="get_censys_host_data"),
    path('search/<str:host>', SearcherView.as_view(), name="search"),

    path('login_required_view/<str:cve_code>', login_required_view, name="login_required_view"),

    path("dns/<str:host>", DNSSearcherView.as_view(), name="dns_record"),

    path('local', LocalView.as_view(), name="local_windows"),
    path('local/registry', WindowsRegistryView.as_view(), name="registry_windows"),
    path('local/hardware', WindowsHardwareView.as_view(), name="hardware_windows"),
    path('local/network', NetworkLocalView.as_view(), name="network_windows"),
]
