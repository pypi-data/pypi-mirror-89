from __future__ import print_function

# python
import logging
import json
import re
from jsonpath_ng import parse
# aws
# common
# app

from .utilx import Util
from halo_app.app.context import HaloContext
from ..errors import status
from ..const import HTTPChoice, ASYNC
from ..exceptions import *
from ..reflect import Reflect
from halo_app.app.request import HaloRequest, HaloQueryRequest, HaloCommandRequest
from halo_app.app.response import HaloResponse
from ..settingsx import settingsx
from ..classes import AbsBaseClass
from .servicex import SAGA,SEQ,FoiBusinessEvent,SagaBusinessEvent
from halo_app.infra.apis import ApiMngr
from .filterx import RequestFilter
from halo_app.providers.providers import get_provider
from halo_app.saga import SagaRollBack, load_saga

settings = settingsx()

# Create your mixin here.

# DRF

# When a service is not responding for a certain amount of time, there should be a fallback path so users are not waiting for the response,
# but are immediately notified about the internal problem with a default response. It is the essence of a responsive design.

logger = logging.getLogger(__name__)


class AbsBaseHandler(AbsBaseClass):
    __metaclass__ = ABCMeta

    business_event = None
    secure = False
    method_roles = None

    def create_response(self,halo_request, payload, headers):
        code = status.HTTP_200_OK
        if halo_request.context.get(HaloContext.method) == HTTPChoice.post.value or halo_request.context.get(HaloContext.method) == HTTPChoice.put.value:
            code = status.HTTP_201_CREATED
        return HaloResponse(halo_request, payload, code, headers)

    def validate_req(self, halo_request):
        logger.debug("in validate_req ")
        if halo_request:
            return True
        raise BadRequestError("Halo Request not valid")

    def validate_pre(self, halo_request):
        if halo_request:
            return True
        raise HaloException("Fail pre validation for Halo Request")

    def set_back_api(self, halo_request, foi=None):
        if foi:
            foi_name = foi["name"]
            foi_op = foi["op"]
            foi_conn = foi["conn"]
            #api = ApiMngr.get_api(foi_name)
            #instance = Reflect.instantiate(api, AbsBaseApi, halo_request.context)
            instance = ApiMngr.get_api_instance(foi_name, halo_request.context)
            instance.op = foi_op
            instance.conn = foi_conn
            return instance
        raise NoApiClassException("api class not defined")

    def set_api_headers(self,halo_request,api, seq=None, dictx=None):
        logger.debug("in set_api_headers ")
        if halo_request and api.api_type == "service":
            return dict(halo_request.headers)
        return {}
        raise HaloException("no headers")

    def set_api_vars(self,halo_request,api, seq=None, dict=None):
        logger.debug("in set_api_vars " + str(halo_request))
        if True:
            ret = {}
            return ret
        raise HaloException("no var")

    def set_api_auth(self,halo_request,api, seq=None, dict=None):
        return None

    def set_api_data(self,halo_request,api, seq=None, dict=None):
        return halo_request.vars

    def execute_api(self,halo_request, back_api, back_vars, back_headers, back_auth, back_data=None, seq=None, dict=None):
        logger.debug("in execute_api "+back_api.name)
        if back_api:
            timeout = Util.get_timeout(halo_request.context)
            try:
                seq_msg = ""
                if seq:
                    seq_msg = "seq = " + seq + "."
                ret = back_api.run(timeout, headers=back_headers,auth=back_auth, data=back_data)
                msg = "in execute_api. " + seq_msg + " code= " + str(ret.status_code)
                logger.info(msg)
                return ret
            except ApiError as e:
                raise HaloError("failed to execute api:"+str(back_api.name),e)
        return None

    def extract_json(self,halo_request,api, back_response, seq=None):
        logger.debug("in extract_json ")
        if back_response:
            try:
                return json.loads(back_response.content)
            except json.decoder.JSONDecodeError as e:
                pass
        return json.loads("{}")

    def create_resp_payload(self, halo_request, dict_back_json):
        logger.debug("in create_resp_payload " + str(dict_back_json))
        if dict_back_json:
            mapping = self.load_resp_mapping(halo_request)
            if mapping:
                try:
                    jsonpath_expression = parse(str(mapping))
                    matchs = jsonpath_expression.find(dict_back_json)
                    for match in matchs:
                        logger.debug( match.value)
                    ret = self.create_resp_json(halo_request, dict_back_json,matchs)
                    return ret
                except Exception as e:
                    logger.debug(str(e))
                    raise HaloException("mapping error for " + halo_request.method_id,e)
            ret = self.create_resp_json(halo_request, dict_back_json)
            return ret
        return {}

    def create_resp_json(self, halo_request, dict_back_json, matchs=None):
        logger.debug("in create_resp_json ")
        if matchs:
            js = {}
            try:
                for match in matchs:
                    logger.debug(match.value)
                    js[match.path] = match.value
                    return js
            except Exception as e:
                pass
        else:
            if type(dict_back_json) is dict:
                if len(dict_back_json) == 1:
                    if 1 in dict_back_json:
                        return dict_back_json[1]
                    return list(dict_back_json.values())[0]
                else:
                    return self.dict_to_json(dict_back_json)
        return dict_back_json

    def dict_to_json(self, dict_back_json):
        return dict_back_json

    def load_resp_mapping1(self, halo_request):
        logger.debug("in load_resp_mapping " + str(halo_request))
        if settings.MAPPING and halo_request.method_id in settings.MAPPING:
            mapping = settings.MAPPING[halo_request.method_id]
            logger.debug("in load_resp_mapping " + str(mapping))
            return mapping
        raise HaloException("no mapping for "+halo_request.method_id)

    def load_resp_mapping(self, halo_request):
        logger.debug("in load_resp_mapping " + str(halo_request))
        if settings.MAPPING:
            for path in settings.MAPPING:
                try:
                    if re.match(path,halo_request.method_id):
                        mapping = settings.MAPPING[path]
                        logger.debug("in load_resp_mapping " + str(mapping))
                        return mapping
                except Exception as e:
                    logger.debug("error in load_resp_mapping " + str(path))
        return None

    def set_resp_headers(self, halo_request, headers=None):
        logger.debug("in set_resp_headers " + str(headers))
        if headers:
            headersx = {}
            for h in headers:
                if h in headers:
                    headersx[h] = headers[h]
            headersx['mimetype'] = 'application/json'
            return headersx
        #raise HaloException("no headers")
        return []

    def validate_post(self, halo_request, halo_response):
        return

    def do_filter(self, halo_request, halo_response):  #
        logger.debug("do_filter")
        request_filter = self.get_request_filter(halo_request)
        request_filter.do_filter(halo_request, halo_response)

    def get_request_filter(self, halo_request):
        if settings.REQUEST_FILTER_CLASS:
            return Reflect.instantiate(settings.REQUEST_FILTER_CLASS, RequestFilter)
        return RequestFilter()

class AbsQueryHandler(AbsBaseHandler):
    __metaclass__ = ABCMeta

    def do_operation(self, halo_request:HaloRequest)->HaloResponse:
        # 1. validate input params
        self.validate_req(halo_request)
        # 2. run pre conditions
        self.validate_pre(halo_request)
        # 3. processing engine
        dict = self.data_engine(halo_request)
        # 4. Build the payload target response structure which is Compliant
        payload = self.create_resp_payload(halo_request, dict)
        logger.debug("payload=" + str(payload))
        # 5. setup headers for reply
        headers = self.set_resp_headers(halo_request)
        # 6. build json and add to halo response
        halo_response = self.create_response(halo_request, payload, headers)
        # 7. post condition
        self.validate_post(halo_request, halo_response)
        # 8. do filter
        #self.do_filter(halo_request,halo_response)
        # 9. return json response
        return halo_response

    def data_engine(self,halo_request:HaloQueryRequest)->dict:
        return self.run(halo_request)

    def run(self, halo_query_request: HaloQueryRequest) -> dict:
        raise HaloMethodNotImplementedException("method run in Query")

    def run_query(self,halo_request:HaloQueryRequest)->HaloResponse:
        ret:HaloResponse = self.do_operation(halo_request)
        return ret

class AbsCommandHandler(AbsBaseHandler):
    __metaclass__ = ABCMeta

    # each handler injects the following:
    # DomainService
    # InfrastructureService
    # Repository

    def do_operation_bq(self, halo_request):
        if halo_request.sub_func is None:
            raise IllegalBQException("missing sub_func value")
        sub_func = halo_request.sub_func.lower()
        return self.do_operation(halo_request)

    def do_operation_bq1(self, halo_request):
        if halo_request.sub_func is None:
            raise IllegalBQException("missing sub_func value")
        try:
            sub_func = halo_request.sub_func.lower()
            # 1. validate input params
            getattr(self, 'validate_req_%s' % sub_func)(halo_request)
            # 2. Code to access the BANK API  to retrieve data - url + vars dict
            getattr(self, 'validate_pre_%s' % sub_func)(halo_request)
            # 3. processing engine
            dict = self.processing_engine(halo_request)
            # 4. Build the payload target response structure which is Compliant
            payload = getattr(self, 'create_resp_payload_%s' % sub_func)(halo_request, dict)
            logger.debug("payload=" + str(payload))
            # 5. setup headers for reply
            headers = getattr(self, 'set_resp_headers_%s' % sub_func)(halo_request,
                                                                                halo_request.headers)
            # 6. build json and add to halo response
            halo_response = self.create_response(halo_request, payload, headers)
            # 7. post condition
            getattr(self, 'validate_post_%s' % sub_func)(halo_request, halo_response)
            # 8. do filter
            #self.do_filter(halo_request, halo_response)
            # return json response
            return halo_response
        except AttributeError as ex:
            raise HaloMethodNotImplementedException("function for "+str(halo_request.sub_func),ex)

    def do_operation_1_bq(self, halo_request, sub_func):  # basic maturity - single request
        logger.debug("do_operation_1_bq")
        if sub_func is None:
            raise IllegalBQException("missing sub_func value")
        logger.debug("do_operation_1")
        # 1. get api definition to access the BANK API  - url + vars dict
        back_api = getattr(self, 'set_back_api_%s' % sub_func)(halo_request)
        # 2. array to store the headers required for the API Access
        back_headers = getattr(self, 'set_api_headers_%s' % sub_func)(halo_request,back_api)
        # 3. set request params
        back_vars = getattr(self, 'set_api_vars_%s' % sub_func)(halo_request,back_api)
        # 4. Sset request auth
        back_auth = getattr(self, 'set_api_auth_%s' % sub_func)(halo_request,back_api)
        # 5. Sset request data
        back_data = getattr(self, 'set_api_data_%s' % sub_func)(halo_request,back_api)
        # 6. Sending the request to the BANK API with params
        back_response = getattr(self, 'execute_api_%s' % sub_func)(halo_request, back_api, back_vars,
                                                                             back_headers, back_auth, back_data)
        # 7. extract from Response stored in an object built as per the BANK API Response body JSON Structure
        back_json = getattr(self, 'extract_json_%s' % sub_func)(halo_request,back_api, back_response)
        dict = {'1': back_json}
        # 8. return json response
        return dict

    def do_operation_2_bq(self, halo_request, sub_func):  # medium maturity - foi
        logger.debug("do_operation_2_bq")
        dict = {}
        for seq in self.business_event.keys():
            # 1. get get first order interaction
            foi = self.business_event.get(seq)
            # 2. get api definition to access the BANK API  - url + vars dict
            back_api = getattr(self, 'set_back_api_%s' % sub_func)(halo_request, foi)
            back_json = self.do_api_work_bq(halo_request, sub_func, back_api, seq)
            # 9. store in dict
            dict[seq] = back_json
        return dict

    def do_operation_3_bq(self, halo_request,sub_func):  # high maturity - saga transactions
        logger.debug("do_operation_3_bq")
        # saga engine
        #@todo implement provider saga
        #if saga_type == "provider":
        #    return get_provider().provider_saga(self.business_event.EVENT_NAME,halo_request, self.business_event.saga)
        sagax = load_saga(self.business_event.EVENT_NAME,halo_request, self.business_event.saga, settings.SAGA_SCHEMA)
        payloads = {}
        apis = {}
        counter = 1
        for state in self.business_event.saga["States"]:
            if 'Resource' in self.business_event.saga["States"][state]:
                api_name = self.business_event.saga["States"][state]['Resource']
                logger.debug(api_name)
                payloads[state] = {"request": halo_request, 'seq': str(counter),"sub_func":sub_func}
                apis[state] = self.do_saga_work_bq
                counter = counter + 1

        try:
            ret = sagax.execute(halo_request.context, payloads, apis)
            return ret
        except SagaRollBack as e:
            logger.error("error in business_event:EVENT_NAME" + str(self.business_event.EVENT_NAME))
            raise HaloError("error in processing", original_exception=e,status_code=500)

    def do_saga_work_bq(self, api, results, payload):
        logger.debug("do_saga_work_bq=" + str(api) + " result=" + str(results) + "payload=" + str(payload))
        set_api = self.set_api_op(api,payload)
        return self.do_api_work_bq(payload['request'],payload['sub_func'], set_api, payload['seq'])

    def do_api_work_bq(self,halo_request,sub_func, back_api, seq):
        # 3. array to store the headers required for the API Access
        back_headers = getattr(self, 'set_api_headers_%s' % sub_func)(halo_request,back_api, seq, dict)
        # 4. set vars
        back_vars = getattr(self, 'set_api_vars_%s' % sub_func)(halo_request,back_api, seq, dict)
        # 5. auth
        back_auth = getattr(self, 'set_api_auth_%s' % sub_func)(halo_request,back_api, seq, dict)
        # 6. set request data
        back_data = getattr(self, 'set_api_data_%s' % sub_func)(halo_request,back_api, seq, dict)
        # 7. Sending the request to the BANK API with params
        back_response = getattr(self, 'execute_api_%s' % sub_func)(halo_request, back_api, back_vars,
                                                                             back_headers, back_auth, back_data,
                                                                             seq, dict)
        # 8. extract from Response stored in an object built as per the BANK API Response body JSON Structure
        back_json = getattr(self, 'extract_json_%s' % sub_func)(halo_request,back_api, back_response, seq)
        # return
        return back_json

    def do_operation(self, halo_request:HaloRequest)->HaloResponse:
        # 1. validate input params
        self.validate_req(halo_request)
        # 2. run pre conditions
        self.validate_pre(halo_request)
        # 3. processing engine
        table = self.processing_engine(halo_request)
        # 4. Build the payload target response structure which is Compliant
        payload = self.create_resp_payload(halo_request, table)
        logger.debug("payload=" + str(payload))
        # 5. setup headers for reply
        headers = self.set_resp_headers(halo_request)
        # 6. build json and add to halo response
        halo_response = self.create_response(halo_request, payload, headers)
        # 7. post condition
        self.validate_post(halo_request, halo_response)
        # 8. do filter
        #self.do_filter(halo_request,halo_response)
        # 9. return json response
        return halo_response

    def do_operation_1(self, halo_request):  # basic maturity - single request
        logger.debug("do_operation_1")
        # 1. get api definition to access the BANK API  - url + vars dict
        back_api = self.set_back_api(halo_request)
        # 2. array to store the headers required for the API Access
        back_headers = self.set_api_headers(halo_request,back_api)
        # 3. Set request params
        back_vars = self.set_api_vars(halo_request,back_api)
        # 4. Set request auth
        back_auth = self.set_api_auth(halo_request,back_api)
        # 5. Set request data
        back_data = self.set_api_data(halo_request,back_api)
        # 6. Sending the request to the BANK API with params
        back_response = self.execute_api(halo_request, back_api, back_vars, back_headers, back_auth,
                                                   back_data)
        # 7. extract from Response stored in an object built as per the BANK API Response body JSON Structure
        back_json = self.extract_json(halo_request,back_api, back_response)
        dict = {'1': back_json}
        # 8. return json response
        return dict

    def do_operation_2(self, halo_request):  # medium maturity - foi
        logger.debug("do_operation_2")
        api_list = []
        dict = {}
        for seq in self.business_event.keys():
            print("seq="+str(seq))
            # 1. get get first order interaction
            foi = self.business_event.get(seq)
            # 2. get api definition to access the BANK API  - url + vars dict
            back_api = self.set_back_api(halo_request, foi)
            api_list.append(back_api)
            if back_api.conn == ASYNC:
                # 2.1 do async api work
                back_json = self.do_api_async_work(halo_request, back_api, seq, dict)
            else:
                # 2.2 do api work
                back_json = self.do_api_work(halo_request, back_api, seq, dict)
            # 3. store in dict
            dict[seq] = back_json
        for api in api_list:
            api.terminate()
        return dict

    def do_api_async_work(self, halo_request, back_api, seq, dict=None):
        # 3. array to store the headers required for the API Access
        back_headers = self.set_api_headers(halo_request,back_api, seq, dict)
        # 4. set vars
        back_vars = self.set_api_vars(halo_request,back_api, seq, dict)
        # 5. auth
        back_auth = self.set_api_auth(halo_request,back_api, seq, dict)
        # 6. set request data
        back_data = self.set_api_data(halo_request,back_api, seq, dict)
        # 7. Sending the request to the BANK API with params
        status = get_provider().add_to_queue(halo_request, back_api, back_vars, back_headers, back_auth,
                                         back_data, seq, dict)
        return {}

    def do_api_work(self,halo_request, back_api, seq, dict=None):
        # 3. array to store the headers required for the API Access
        back_headers = self.set_api_headers(halo_request,back_api, seq, dict)
        # 4. set vars
        back_vars = self.set_api_vars(halo_request,back_api, seq, dict)
        # 5. auth
        back_auth = self.set_api_auth(halo_request,back_api, seq, dict)
        # 6. set request data
        back_data = self.set_api_data(halo_request,back_api, seq, dict)
        # 7. Sending the request to the BANK API with params
        back_response = self.execute_api(halo_request, back_api, back_vars, back_headers, back_auth,
                                              back_data, seq, dict)
        # 8. extract from Response stored in an object built as per the BANK API Response body JSON Structure
        back_json = self.extract_json(halo_request,back_api, back_response, seq)
        # return
        return back_json

    def set_api_op(self, api, payload):
        req = payload['request']
        #if not req.sub_func:# base option
            #if req.request.method == HTTPChoice.put.value:
                #if payload['state'] == 'BookHotel':
                #    api.op = HTTPChoice.post.value
                # if payload['state'] == 'BookCancel':
                #    api.op = HTTPChoice.delete.value
        #else:
            #if req.sub_func == "deposit":
                # if req.request.method == HTTPChoice.put.value:
                    # if payload['state'] == 'BookHotel':
                    #    api.op = HTTPChoice.post.value
                    # if payload['state'] == 'BookCancel':
                    #    api.op = HTTPChoice.delete.value
        return api

    def do_saga_work(self, api, results, payload):
        logger.debug("do_saga_work=" + str(api) + " result=" + str(results) + "payload=" + str(payload))
        set_api = self.set_api_op(api,payload)
        return self.do_api_work(payload['request'], set_api, payload['seq'])

    def do_operation_3(self, halo_request):  # high maturity - saga transactions
        logger.debug("do_operation_3")
        sagax = load_saga("test",halo_request, self.business_event.saga, settings.SAGA_SCHEMA)
        payloads = {}
        apis = {}
        counter = 1
        for state in self.business_event.saga["States"]:
            if 'Resource' in self.business_event.saga["States"][state]:
                api_name = self.business_event.saga["States"][state]['Resource']
                logger.debug(api_name)
                payloads[state] = {"request": halo_request, 'seq': str(counter),"state":state}
                apis[state] = self.do_saga_work
                counter = counter + 1

        try:
            ret = sagax.execute(halo_request.context, payloads, apis)
            return ret
        except SagaRollBack as e:
            raise ApiError(e.message,e,e.detail ,e.data,status_code=500)

    def processing_engine(self, halo_request:HaloCommandRequest)->dict:
        if self.business_event:
            return self.processing_engine_dtl(halo_request)
        else:
            return self.handle(halo_request)

    def processing_engine_dtl(self, halo_request:HaloCommandRequest)->dict:
        if self.business_event:
            if self.business_event.get_business_event_type() == SAGA:
                return self.do_operation_3(halo_request)
            if self.business_event.get_business_event_type() == SEQ:
                if self.business_event.keys():
                    return self.do_operation_2(halo_request)
                else:
                    raise BusinessEventMissingSeqException(self.service_operation)
            else:
                return self.do_operation_1(halo_request)

    def handle(self,halo_command_request:HaloCommandRequest)->dict:
        raise HaloMethodNotImplementedException("method handle in command")

    def processing_engine1(self, halo_request):
        if self.business_event:
            if self.business_event.get_business_event_type() == SAGA:
                if halo_request.sub_func:
                    return self.do_operation_3_bq(halo_request, halo_request.sub_func.lower())
                return self.do_operation_3(halo_request)
            if self.business_event.get_business_event_type() == SEQ:
                if self.business_event.keys():
                    if halo_request.sub_func:
                        return self.do_operation_2_bq(halo_request, halo_request.sub_func.lower())
                    return self.do_operation_2(halo_request)
                else:
                    raise BusinessEventMissingSeqException(self.service_operation)
        else:
            if halo_request.sub_func:
                return self.do_operation_1_bq(halo_request, halo_request.sub_func.lower())
            return self.do_operation_1(halo_request)

    def set_businss_event(self, halo_request, event_category):
       self.service_operation = self.__class__.__name__#request.endpoint
       if not self.business_event:
            if settings.BUSINESS_EVENT_MAP:
                if self.service_operation in settings.BUSINESS_EVENT_MAP:
                    bq = "base"
                    bqs = settings.BUSINESS_EVENT_MAP[self.service_operation]
                    if bq in bqs:
                        service_list = bqs[bq]
                        #@todo add schema to all event config files
                        if service_list and halo_request.method_id in service_list.keys():
                            service_map = service_list[halo_request.method_id]
                            if SEQ in service_map:
                                dict = service_map[SEQ]
                                self.business_event = FoiBusinessEvent(self.service_operation,event_category, dict)
                            if SAGA in service_map:
                                saga = service_map[SAGA]
                                self.business_event = SagaBusinessEvent(self.service_operation, event_category, saga)
                    #   if no entry use simple operation
       return self.business_event

    def get_bq(self,vars):
        if vars and "sub_func" in vars:
            return self.validate_bq(vars["sub_func"]).lower()
        return None

    def validate_bq(self,bq):
        return bq

    ######################################################################

    def run_command(self,halo_request:HaloCommandRequest)->HaloResponse:
        self.set_businss_event(halo_request, "x")
        ret:HaloResponse = self.do_operation(halo_request)
        return ret







