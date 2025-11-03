from django.urls import path
from .views import (
    AssistantLiveView,
    AssistantConfigView,
    AssistantPublishView,
    AssistantVersionsListView,
    AssistantRollbackView,
    KnowledgeDocsView,
    KnowledgeEmbedView,
    IntentsView,
    AssistantAskView,
    CreateListingActionView,
    StartJCWBuildActionView,
    StartPrintOrderActionView,
)

urlpatterns = [
    path("api/assistant/live", AssistantLiveView.as_view(), name="assistant-live"),
    path("api/assistant/config", AssistantConfigView.as_view(), name="assistant-config"),
    path("api/assistant/publish", AssistantPublishView.as_view(), name="assistant-publish"),
    path("api/assistant/versions", AssistantVersionsListView.as_view(), name="assistant-versions"),
    path("api/assistant/rollback/<int:version>", AssistantRollbackView.as_view(), name="assistant-rollback"),
    path("api/assistant/kb", KnowledgeDocsView.as_view(), name="knowledge-docs"),
    path("api/assistant/kb/embed", KnowledgeEmbedView.as_view(), name="knowledge-embed"),
    path("api/assistant/intents", IntentsView.as_view(), name="assistant-intents"),
    path("api/assistant/ask", AssistantAskView.as_view(), name="assistant-ask"),
    
    # Actions (CTAs)
    path("api/assistant/actions/create_listing", CreateListingActionView.as_view(), name="assistant-action-create-listing"),
    path("api/assistant/actions/start_jcw_build", StartJCWBuildActionView.as_view(), name="assistant-action-start-jcw"),
    path("api/assistant/actions/start_print_order", StartPrintOrderActionView.as_view(), name="assistant-action-start-print"),
]