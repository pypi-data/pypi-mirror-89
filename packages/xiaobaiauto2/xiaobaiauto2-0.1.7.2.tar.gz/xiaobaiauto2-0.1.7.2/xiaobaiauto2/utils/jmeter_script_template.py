#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'jmeter_script_template.py'
__create_time__ = '2020/12/24 14:44'

from typing import Optional
from urllib.parse import urlparse

def JMETER_SCRIPT_HEAD(JMETER_VERSION: Optional[str] = '5.2.1'):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="{JMETER_VERSION}">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <CookieManager guiclass="CookiePanel" testclass="CookieManager" testname="HTTP Cookie管理器" enabled="true">
        <collectionProp name="CookieManager.cookies"/>
        <boolProp name="CookieManager.clearEachIteration">false</boolProp>
        <boolProp name="CookieManager.controlledByThreadGroup">false</boolProp>
      </CookieManager>
      <hashTree/>
      <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="察看结果树" enabled="true">
        <boolProp name="ResultCollector.error_logging">false</boolProp>
        <objProp>
          <name>saveConfig</name>
          <value class="SampleSaveConfiguration">
            <time>true</time>
            <latency>true</latency>
            <timestamp>true</timestamp>
            <success>true</success>
            <label>true</label>
            <code>true</code>
            <message>true</message>
            <threadName>true</threadName>
            <dataType>true</dataType>
            <encoding>false</encoding>
            <assertions>true</assertions>
            <subresults>true</subresults>
            <responseData>false</responseData>
            <samplerData>false</samplerData>
            <xml>false</xml>
            <fieldNames>true</fieldNames>
            <responseHeaders>false</responseHeaders>
            <requestHeaders>false</requestHeaders>
            <responseDataOnError>false</responseDataOnError>
            <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
            <assertionsResultsToSave>0</assertionsResultsToSave>
            <bytes>true</bytes>
            <sentBytes>true</sentBytes>
            <url>true</url>
            <threadCounts>true</threadCounts>
            <idleTime>true</idleTime>
            <connectTime>true</connectTime>
          </value>
        </objProp>
        <stringProp name="filename"></stringProp>
      </ResultCollector>
      <hashTree/>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">1</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
'''

def JMETER_SCRIPT_FOOT():
    return '''
    </hashTree>
  </hashTree>
</jmeterTestPlan>
'''

def JMETER_SCRIPT_HEADER(key, value):
    return f'''
              <elementProp name="" elementType="Header">
                <stringProp name="Header.name">{key}</stringProp>
                <stringProp name="Header.value">{value}</stringProp>
              </elementProp>
    '''

def JMETER_EQUEST(file_path: Optional[str] = '',
                  post_value: Optional[str] = '',
                  domain: Optional[str] = '',
                  port: Optional[str] = '',
                  protocol: Optional[str] = '',
                  contentEncoding: Optional[str] = '',
                  path: Optional[str] = '/',
                  method: Optional[str] = 'GET',
                  headers: Optional[dict] = None):
    header = ''
    for k, v in headers.items():
        header += JMETER_SCRIPT_HEADER(k, v)
    request_name = 'index' if urlparse(url=path).path in ['', '/'] else urlparse(url=path).path.split('/')[-1]
    return f'''
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{request_name}" enabled="true">
          <elementProp name="HTTPsampler.Files" elementType="HTTPFileArgs">
            <collectionProp name="HTTPFileArgs.files">
              <elementProp name="{file_path}" elementType="HTTPFileArg">
                <stringProp name="File.path">{file_path}</stringProp>
                <stringProp name="File.paramname"></stringProp>
                <stringProp name="File.mimetype"></stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{post_value}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">{domain}</stringProp>
          <stringProp name="HTTPSampler.port">{port}</stringProp>
          <stringProp name="HTTPSampler.protocol">{protocol}</stringProp>
          <stringProp name="HTTPSampler.contentEncoding">{contentEncoding}</stringProp>
          <stringProp name="HTTPSampler.path">{path}</stringProp>
          <stringProp name="HTTPSampler.method">{method}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
            <collectionProp name="HeaderManager.headers">
              {header}
            </collectionProp>
          </HeaderManager>
          <hashTree/>
        </hashTree>
      </hashTree>
'''

def create_jmeter(
        jmeter_version: Optional[str] = '5.2.1',
        request: Optional[list] = None,
    ):
    if request is None:
        return JMETER_SCRIPT_HEAD(jmeter_version) + \
            JMETER_EQUEST() + \
            JMETER_SCRIPT_FOOT()
    else:
        code = ''
        for i, v in enumerate(request):
            if isinstance(v, dict):
                code += JMETER_EQUEST(post_value=v.get('data'), path=v.get('url'), method=v.get('method'),
                                      headers=v.get('headers'))
        return JMETER_SCRIPT_HEAD(jmeter_version) + \
               code + \
               JMETER_SCRIPT_FOOT()