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
    standard_no: str = Field(None, repr=True)

    class Meta:
        model = Standards
        exclude = ['id', 'standard_number', 'standard', 'year', 'remark']

    @staticmethod
    def resolve_standard_no(obj):
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
    class Meta:
        model = PublishProduct
        exclude = ['id', 'certificate', 'material', 'rmc_producer_code', 'additional_info', 'order']


class Standard1Schema(Schema):
    standard_name: str
    standard_number: str


class CertificateModelSchema(ModelSchema):
    roc_no: str = ""
    category: str = "A"
    CB_ID: str = ""
    start_certificates_date: datetime.date = Field(None)
    expiry_certificates_date: datetime.date = Field("", alias="expiry_date")
    manufacturer_name: str = Field("", alias="manufacturer")
    # standards: List[StandardSchema] = Field(None)
    MODEL_INFOS: List[ProductSchema] = Field(None)
    standards: list
    CERT_STATUS: str = ""

    class Meta:
        model = PublishCertificate
        exclude = ['id', 'country', 'information', 'date_renewal', 'template', 'date_original_issue', 'expiry_date',
                   'draft_certificate', 'qr_image', 'brands', 'plant_identity', 'date_amendment', 'product_description',
                   'manufacturer_country', 'manufacturer_country', 'holder_country', "manufacturer", 'status',
                   'certificate_holder', 'holder_address', 'holder_address2', 'holder_address3', 'holder_city',
                   'holder_state', 'holder_postcode', 'holder_country', 'holder_status', 'product_standard'
                   ]

    # @staticmethod
    # def resolve_standards(obj, context):
    #
    #     standards = obj.draft_certificate.product_standard
    #     return [standards]

    @staticmethod
    def resolve_standards(obj):
        standards = obj.draft_certificate.product_standard.remark

        standard_name = obj.draft_certificate.product_standard.standard_name
        items = standards.split('| ')
        dictonary = {}
        listdictionary = []
        for i in items:

            dictonary['standard_no'] = i
            dictonary['standard_name'] = standard_name
            listdictionary.append(dictonary)
            dictonary = {}
        return listdictionary

    @staticmethod
    def resolve_start_certificates_date(obj):
        if obj.date_renewal is not None:
            return obj.date_renewal
        return obj.date_original_issue

    # @staticmethod
    # def resolve_products(obj):
    #     return obj.publishproduct_set.order_by('order')

    @staticmethod
    def resolve_roc_no(obj, context):
        request = context["request"]
        return request.GET['roc_no']

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


@api.get("/certificate", response=CertificateModelSchema)
def get_certificate(request, certificate_no: str = "", roc_no: str = "", category: str = "", CB_ID: str = ""):
    if not certificate_no or not roc_no or not category or not CB_ID:
        raise BadRequest
    if CB_ID != "IKRAM":
        raise Cert404

    try:
        query = PublishCertificate.objects.get(certificate_no=certificate_no)
    except PublishCertificate.DoesNotExist:
        raise Cert404

    if query:
        if (query.draft_certificate.certificate_holder.roc_no != roc_no) or (category != 'A'):
            raise CertInvalid
    return query
