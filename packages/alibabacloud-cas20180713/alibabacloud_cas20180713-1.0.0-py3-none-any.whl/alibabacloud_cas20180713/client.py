# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_cas20180713 import models as cas_20180713_models
from alibabacloud_tea_util import models as util_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self._endpoint_map = {
            'cn-hangzhou': 'cas.aliyuncs.com',
            'ap-northeast-2-pop': 'cas.aliyuncs.com',
            'ap-southeast-1': 'cas.aliyuncs.com',
            'ap-southeast-3': 'cas.aliyuncs.com',
            'ap-southeast-5': 'cas.aliyuncs.com',
            'cn-beijing': 'cas.aliyuncs.com',
            'cn-beijing-finance-1': 'cas.aliyuncs.com',
            'cn-beijing-finance-pop': 'cas.aliyuncs.com',
            'cn-beijing-gov-1': 'cas.aliyuncs.com',
            'cn-beijing-nu16-b01': 'cas.aliyuncs.com',
            'cn-chengdu': 'cas.aliyuncs.com',
            'cn-edge-1': 'cas.aliyuncs.com',
            'cn-fujian': 'cas.aliyuncs.com',
            'cn-haidian-cm12-c01': 'cas.aliyuncs.com',
            'cn-hangzhou-bj-b01': 'cas.aliyuncs.com',
            'cn-hangzhou-finance': 'cas.aliyuncs.com',
            'cn-hangzhou-internal-prod-1': 'cas.aliyuncs.com',
            'cn-hangzhou-internal-test-1': 'cas.aliyuncs.com',
            'cn-hangzhou-internal-test-2': 'cas.aliyuncs.com',
            'cn-hangzhou-internal-test-3': 'cas.aliyuncs.com',
            'cn-hangzhou-test-306': 'cas.aliyuncs.com',
            'cn-hongkong': 'cas.aliyuncs.com',
            'cn-hongkong-finance-pop': 'cas.aliyuncs.com',
            'cn-huhehaote': 'cas.aliyuncs.com',
            'cn-north-2-gov-1': 'cas.aliyuncs.com',
            'cn-qingdao': 'cas.aliyuncs.com',
            'cn-qingdao-nebula': 'cas.aliyuncs.com',
            'cn-shanghai': 'cas.aliyuncs.com',
            'cn-shanghai-et15-b01': 'cas.aliyuncs.com',
            'cn-shanghai-et2-b01': 'cas.aliyuncs.com',
            'cn-shanghai-finance-1': 'cas.aliyuncs.com',
            'cn-shanghai-inner': 'cas.aliyuncs.com',
            'cn-shanghai-internal-test-1': 'cas.aliyuncs.com',
            'cn-shenzhen': 'cas.aliyuncs.com',
            'cn-shenzhen-finance-1': 'cas.aliyuncs.com',
            'cn-shenzhen-inner': 'cas.aliyuncs.com',
            'cn-shenzhen-st4-d01': 'cas.aliyuncs.com',
            'cn-shenzhen-su18-b01': 'cas.aliyuncs.com',
            'cn-wuhan': 'cas.aliyuncs.com',
            'cn-yushanfang': 'cas.aliyuncs.com',
            'cn-zhangbei-na61-b01': 'cas.aliyuncs.com',
            'cn-zhangjiakou': 'cas.aliyuncs.com',
            'cn-zhangjiakou-na62-a01': 'cas.aliyuncs.com',
            'cn-zhengzhou-nebula-1': 'cas.aliyuncs.com',
            'eu-west-1': 'cas.aliyuncs.com',
            'eu-west-1-oxs': 'cas.aliyuncs.com',
            'rus-west-1-pop': 'cas.aliyuncs.com',
            'us-east-1': 'cas.aliyuncs.com',
            'us-west-1': 'cas.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('cas', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def create_dvorder_audit_with_options(
        self,
        request: cas_20180713_models.CreateDVOrderAuditRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.CreateDVOrderAuditResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.CreateDVOrderAuditResponse().from_map(
            self.do_rpcrequest('CreateDVOrderAudit', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_dvorder_audit_with_options_async(
        self,
        request: cas_20180713_models.CreateDVOrderAuditRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.CreateDVOrderAuditResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.CreateDVOrderAuditResponse().from_map(
            await self.do_rpcrequest_async('CreateDVOrderAudit', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_dvorder_audit(
        self,
        request: cas_20180713_models.CreateDVOrderAuditRequest,
    ) -> cas_20180713_models.CreateDVOrderAuditResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_dvorder_audit_with_options(request, runtime)

    async def create_dvorder_audit_async(
        self,
        request: cas_20180713_models.CreateDVOrderAuditRequest,
    ) -> cas_20180713_models.CreateDVOrderAuditResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_dvorder_audit_with_options_async(request, runtime)

    def create_user_certificate_with_options(
        self,
        request: cas_20180713_models.CreateUserCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.CreateUserCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.CreateUserCertificateResponse().from_map(
            self.do_rpcrequest('CreateUserCertificate', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_user_certificate_with_options_async(
        self,
        request: cas_20180713_models.CreateUserCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.CreateUserCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.CreateUserCertificateResponse().from_map(
            await self.do_rpcrequest_async('CreateUserCertificate', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_user_certificate(
        self,
        request: cas_20180713_models.CreateUserCertificateRequest,
    ) -> cas_20180713_models.CreateUserCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_user_certificate_with_options(request, runtime)

    async def create_user_certificate_async(
        self,
        request: cas_20180713_models.CreateUserCertificateRequest,
    ) -> cas_20180713_models.CreateUserCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_user_certificate_with_options_async(request, runtime)

    def delete_user_certificate_with_options(
        self,
        request: cas_20180713_models.DeleteUserCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DeleteUserCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DeleteUserCertificateResponse().from_map(
            self.do_rpcrequest('DeleteUserCertificate', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_user_certificate_with_options_async(
        self,
        request: cas_20180713_models.DeleteUserCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DeleteUserCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DeleteUserCertificateResponse().from_map(
            await self.do_rpcrequest_async('DeleteUserCertificate', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_user_certificate(
        self,
        request: cas_20180713_models.DeleteUserCertificateRequest,
    ) -> cas_20180713_models.DeleteUserCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_user_certificate_with_options(request, runtime)

    async def delete_user_certificate_async(
        self,
        request: cas_20180713_models.DeleteUserCertificateRequest,
    ) -> cas_20180713_models.DeleteUserCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_user_certificate_with_options_async(request, runtime)

    def describe_dvorder_result_with_options(
        self,
        request: cas_20180713_models.DescribeDVOrderResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeDVOrderResultResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeDVOrderResultResponse().from_map(
            self.do_rpcrequest('DescribeDVOrderResult', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dvorder_result_with_options_async(
        self,
        request: cas_20180713_models.DescribeDVOrderResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeDVOrderResultResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeDVOrderResultResponse().from_map(
            await self.do_rpcrequest_async('DescribeDVOrderResult', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dvorder_result(
        self,
        request: cas_20180713_models.DescribeDVOrderResultRequest,
    ) -> cas_20180713_models.DescribeDVOrderResultResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dvorder_result_with_options(request, runtime)

    async def describe_dvorder_result_async(
        self,
        request: cas_20180713_models.DescribeDVOrderResultRequest,
    ) -> cas_20180713_models.DescribeDVOrderResultResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dvorder_result_with_options_async(request, runtime)

    def describe_order_instance_list_with_options(
        self,
        request: cas_20180713_models.DescribeOrderInstanceListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeOrderInstanceListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeOrderInstanceListResponse().from_map(
            self.do_rpcrequest('DescribeOrderInstanceList', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_order_instance_list_with_options_async(
        self,
        request: cas_20180713_models.DescribeOrderInstanceListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeOrderInstanceListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeOrderInstanceListResponse().from_map(
            await self.do_rpcrequest_async('DescribeOrderInstanceList', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_order_instance_list(
        self,
        request: cas_20180713_models.DescribeOrderInstanceListRequest,
    ) -> cas_20180713_models.DescribeOrderInstanceListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_order_instance_list_with_options(request, runtime)

    async def describe_order_instance_list_async(
        self,
        request: cas_20180713_models.DescribeOrderInstanceListRequest,
    ) -> cas_20180713_models.DescribeOrderInstanceListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_order_instance_list_with_options_async(request, runtime)

    def describe_user_certificate_detail_with_options(
        self,
        request: cas_20180713_models.DescribeUserCertificateDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeUserCertificateDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeUserCertificateDetailResponse().from_map(
            self.do_rpcrequest('DescribeUserCertificateDetail', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_user_certificate_detail_with_options_async(
        self,
        request: cas_20180713_models.DescribeUserCertificateDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeUserCertificateDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeUserCertificateDetailResponse().from_map(
            await self.do_rpcrequest_async('DescribeUserCertificateDetail', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_user_certificate_detail(
        self,
        request: cas_20180713_models.DescribeUserCertificateDetailRequest,
    ) -> cas_20180713_models.DescribeUserCertificateDetailResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_user_certificate_detail_with_options(request, runtime)

    async def describe_user_certificate_detail_async(
        self,
        request: cas_20180713_models.DescribeUserCertificateDetailRequest,
    ) -> cas_20180713_models.DescribeUserCertificateDetailResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_user_certificate_detail_with_options_async(request, runtime)

    def describe_user_certificate_list_with_options(
        self,
        request: cas_20180713_models.DescribeUserCertificateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeUserCertificateListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeUserCertificateListResponse().from_map(
            self.do_rpcrequest('DescribeUserCertificateList', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_user_certificate_list_with_options_async(
        self,
        request: cas_20180713_models.DescribeUserCertificateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cas_20180713_models.DescribeUserCertificateListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return cas_20180713_models.DescribeUserCertificateListResponse().from_map(
            await self.do_rpcrequest_async('DescribeUserCertificateList', '2018-07-13', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_user_certificate_list(
        self,
        request: cas_20180713_models.DescribeUserCertificateListRequest,
    ) -> cas_20180713_models.DescribeUserCertificateListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_user_certificate_list_with_options(request, runtime)

    async def describe_user_certificate_list_async(
        self,
        request: cas_20180713_models.DescribeUserCertificateListRequest,
    ) -> cas_20180713_models.DescribeUserCertificateListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_user_certificate_list_with_options_async(request, runtime)
