import datetime
from typing import Optional, List

from django.http import request
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema, Field, ModelSchema
from ninja.errors import AuthenticationError
from ninja.renderers import JSONRenderer, BaseRenderer
from ninja.responses import NinjaJSONEncoder
from ninja.security import HttpBearer
import json

from certificate.models import PublishCertificate, Standards, PublishProduct


class GlobalAuth(HttpBearer):
    openapi_scheme: str = "token"

    def authenticate(self, request, token):
        if token == "mGuYBIJLbvSo":
            return token
        raise InvalidToken


class MyJsonEncoder(NinjaJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%d/%m/%Y')

        return super().default(o)


class MyRenderer(JSONRenderer):

    def render(self, request, data, *, response_status):
        # print('data', data)
        for x, y in data.items():
            if isinstance(y, datetime.date):
                data[x] = y.strftime('%d/%m/%Y')
        # print('data2', data)
        return json.dumps(data, cls=self.encoder_class, **self.json_dumps_params)


class MyJsonRenderer(JSONRenderer):
    encoder_class = NinjaJSONEncoder


api = NinjaAPI(auth=GlobalAuth(), renderer=MyRenderer())


class InvalidToken(Exception):
    pass


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {
        "RESULT": None,
        "SUCCESS": False,
        "ERROR": [
            {
                "CODE": 401,
                "MESSAGE": "Unauthorized",
                "DETAILS": "Authentication failed",
            },
        ]

    }, status=401)


@api.get("/hello")
def hello(request):
    return {"message": "Hello world"}


class StandardSchema(ModelSchema):
    STANDARD_NO: str = Field(None, repr=True)

    class Meta:
        model = Standards
        exclude = ['id', 'standard_number', 'standard', 'year', 'remark']

    @staticmethod
    def resolve_STANDARD_NO(obj):
        standards = obj.__str__()
        return standards


# class CertificateSchema(Schema):
#     cb_id: Optional[str] = None
#     certificate_no: str
#     # category: str
#     product_name: str
#     start_certificate_dates: datetime.date = Field(None, alias="query.date_original_issue")
#     expiry_certificate_dates: datetime.date = Field(None, alias="query.expiry_date")
#     # standards: StandardSchema = None
#
#     manufacturer_name: str = Field(None, alias="query.manufacturer")
#     manufacturer_address: str
#     manufacturer_address2: str
#     manufacturer_address3: str
#     manufacturer_postcode: str
#     manufacturer_city: str
#     manufacturer_state: str
#     # roc_no: None


class ProductSchema(ModelSchema):
    BRAND: str = Field("", alias="brand")
    MODEL: str = Field("", alias="model")
    RATING: str = Field("", alias="rating")
    TYPE: str = Field("", alias="type")
    SIZE: str = Field("", alias="size")

    class Meta:
        model = PublishProduct
        exclude = ['id', 'certificate', 'material', 'rmc_producer_code', 'additional_info', 'order', 'brand',
                   'model', 'rating', 'type', 'size']


class Standard1Schema(Schema):
    STANDARD_NAME: str = Field("", alias="standard_name")
    STANDARD_NUMBER: str = Field("", alias="standard_number")


class CertificateModelSchema(ModelSchema):
    ROC_NO: str = ""
    CATEGORY: str = "A"
    CB_ID: str = ""
    START_CERTIFICATES_DATE: datetime.date = Field(None)
    EXPIRY_CERTIFICATES_DATE: datetime.date = Field("", alias="expiry_date")
    MANUFACTURER_NAME: str = Field("", alias="manufacturer")
    MANUFACTURER_ADDRESS: str = Field("", alias="manufacturer_address")
    MANUFACTURER_ADDRESS2: str = Field("", alias="manufacturer_address2")
    MANUFACTURER_ADDRESS3: str = Field("", alias="manufacturer_address3")
    MANUFACTURER_POSTCODE: str = Field("", alias="manufacturer_postcode")
    MANUFACTURER_CITY: str = Field("", alias="manufacturer_city")
    MANUFACTURER_STATE: str = Field("", alias="manufacturer_state")
    CERTIFICATE_NO: str = Field("", alias="certificate_no")
    PRODUCT_NAME: str = Field("", alias="product_name")



    # standards: List[StandardSchema] = Field(None)
    MODEL_INFOS: List[ProductSchema] = Field(None)
    STANDARDS: list
    CERT_STATUS: str = ""

    class Meta:
        model = PublishCertificate
        exclude = ['id', 'country', 'information', 'date_renewal', 'template', 'date_original_issue', 'expiry_date',
                   'draft_certificate', 'qr_image', 'brands', 'plant_identity', 'date_amendment', 'product_description',
                   'manufacturer_country', 'manufacturer_country', 'holder_country', "manufacturer", "manufacturer_address",
                   "manufacturer_address2","manufacturer_address3", "manufacturer_city", "manufacturer_state", "manufacturer_postcode",
                   'status', 'certificate_holder', 'holder_address', 'holder_address2', 'holder_address3', 'holder_city', 'product_name',
                   'holder_state', 'holder_postcode', 'holder_country', 'holder_status', 'product_standard', 'certificate_no'
                   ]

    # @staticmethod
    # def resolve_standards(obj, context):
    #
    #     standards = obj.draft_certificate.product_standard
    #     return [standards]

    @staticmethod
    def resolve_STANDARDS(obj):
        standards = obj.draft_certificate.product_standard.remark

        standard_name = obj.draft_certificate.product_standard.standard_name
        items = standards.split('| ')
        dictonary = {}
        listdictionary = []
        for i in items:

            dictonary['STANDARD_NO'] = i
            dictonary['STANDARD_NAME'] = standard_name
            listdictionary.append(dictonary)
            dictonary = {}
        return listdictionary

    @staticmethod
    def resolve_START_CERTIFICATES_DATE(obj):
        if obj.date_renewal is not None:
            return obj.date_renewal
        return obj.date_original_issue

    # @staticmethod
    # def resolve_products(obj):
    #     return obj.publishproduct_set.order_by('order')

    @staticmethod
    def resolve_ROC_NO(obj, context):
        request = context["request"]
        return request.GET['ROC_NO']

    @staticmethod
    def resolve_CB_ID(obj, context):
        request = context["request"]
        return request.GET['CB_ID']

    @staticmethod
    def resolve_MODEL_INFOS(obj):
        return obj.publishproduct_set.order_by('order')

    @staticmethod
    def resolve_CERT_STATUS(obj):
        if obj.status == '2': #Published
            return 'CERTIFIED'
        print(obj.get_status_display())
        return obj.status

class CertInvalid(Exception):
    pass


@api.exception_handler(CertInvalid)
def validate_cert(request, exc):
    return api.create_response(request, {
        "RESULT": None,
        "SUCCESS": False,
        "ERROR": [
            {
                "CODE": 403,
                "MESSAGE": "Forbidden",
                "DETAILS": "You do not have permission to access this resource",
            },
        ]

    }, status=403)


class Cert404(Exception):
    pass


@api.exception_handler(Cert404)
def cert_not_found(request, exc):
    return api.create_response(request, {
        "RESULT": None,
        "SUCCESS": False,
        "ERROR": [
            {
                "CODE": 404,
                "MESSAGE": "Not Found",
                "DETAILS": "The requested resource could not be found",
            },
        ]

    }, status=404)


class BadRequest(Exception):
    pass


@api.exception_handler(BadRequest)
def cert_bad_request(request, exc):
    return api.create_response(request, {
        "RESULT": None,
        "SUCCESS": False,
        "ERROR": [
            {
                "CODE": 403,
                "MESSAGE": "Bad Request",
                "DETAILS": "Invalid request parameters",
            },
        ]

    }, status=403
                               )


class InvalidCBID(Exception):
    pass


@api.exception_handler(InvalidCBID)
def cert_invalid_cbid(request, exc):
    return api.create_response(request, {
        "RESULT": None,
        "SUCCESS": False,
        "ERROR": [
            {
                "CODE": 900,
                "MESSAGE": "Invalid CB ID",
                "DETAILS": "CB ID not match"
            },
        ]

    }, status=404
                               )


@api.get("/certificate", response=CertificateModelSchema)
def get_certificate(request, CERTIFICATE_NO: str = "", ROC_NO: str = "", CATEGORY: str = "", CB_ID: str = ""):
    if not CERTIFICATE_NO or not ROC_NO or not CATEGORY or not CB_ID:
        raise BadRequest
    if CB_ID != "IKRAM":
        raise InvalidCBID

    try:
        query = PublishCertificate.objects.get(certificate_no=CERTIFICATE_NO)
    except PublishCertificate.DoesNotExist:
        raise Cert404

    if query:
        if (query.draft_certificate.certificate_holder.roc_no != ROC_NO) or (CATEGORY != 'A'):
            raise CertInvalid
    return query
