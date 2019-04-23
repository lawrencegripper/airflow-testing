from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient


class CognitiveServicesHook(BaseHook):
    """
    Interacts with cognitive servies https:// protocol.

    Example `export AIRFLOW_CONN_COG_SERVICES_DEFAULT="https://azure:<YOUR_KEY_HERE>@<YOUR_ENDPOINT_HERE>:443"`

    :param conn_id: Reference to the https connection.
    :type _conn_id: str
    """

    def __init__(self, conn_id='cognitive_services_default'):
        self.conn_id = conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        """Return the BlockBlobService object."""
        conn = self.get_connection(self.conn_id)
        if conn.port is None:
            conn.port = 443
        return ComputerVisionClient(endpoint="https://{}:{}".format(conn.host, conn.port),
                                  credentials=CognitiveServicesCredentials(conn.password))

    def recognize_printed_text(self, image_url):
        """Optical Character Recognition (OCR) detects text in an image and
        extracts the recognized characters into a machine-usable character
        stream.
        Upon success, the OCR results will be returned.
        Upon failure, the error code together with an error message will be
        returned. The error code can be one of InvalidImageUrl,
        InvalidImageFormat, InvalidImageSize, NotSupportedImage,
        NotSupportedLanguage, or InternalServerError.

        :type url: str
        :return: OcrResult or ClientRawResponse if raw=true
        :rtype:
         ~azure.cognitiveservices.vision.computervision.models.OcrResult or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ComputerVisionErrorException<azure.cognitiveservices.vision.computervision.models.ComputerVisionErrorException>`
        """
        return self.connection.recognize_printed_text(image_url)
            
