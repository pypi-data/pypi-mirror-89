from orionframework.media.services import MediaService
from orionframework.media.settings import OnlineDocument


class OnlineDocumentService(MediaService):
    """
    Service used to manage the lifecycle of the Remote document model.
    """

    model_class = OnlineDocument
