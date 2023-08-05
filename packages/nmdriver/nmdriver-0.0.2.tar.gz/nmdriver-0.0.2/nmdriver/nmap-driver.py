#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import time
import grpc
import nmap
import configparser
import os
from concurrent import futures
from ipdb import set_trace
from ipam import ipam_pb2 as ipam_pb3,ipam_pb2_grpc as ipam_pb3_grpc
from mgrpc import ipam_pb2,ipam_pb2_grpc 
import logging.config
import re

root_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取上一级目录
logging.config.fileConfig(root_dir+"/config"+"/logging.conf")
logger = logging.getLogger('root')

class NmapService(ipam_pb2_grpc.DeviceServiceServicer):
    def ListDeviceMsg(self,request_iterator,ctx):
        ip = request_iterator.next().ip
        logger.info('execute nmap scan ip = %s' % ip)
        res=nmapScan(ip)
        return res
    def GetDeviceMsg(self,request,ctx):
        logger.info('execute nmap scan ip = %s' % request.ip)
        res=nmapSearch(request.ip)
        return res
    
    def GetDeviceSubnet(self,request,ctx):
        logger.info('execute get device subnet')
        res=getDeviceSubnet()
        return res
    
def nmapScan(ip):
    try:
        nm = nmap.PortScanner()
        # 配置nmap扫描参数
        scan_raw_result = nm.scan(hosts=ip, arguments='-sS -F -O')
        nu=scan_raw_result['nmap']['scanstats']
        listDeviceMsgResponse = ipam_pb2.ListDeviceMsgResponse(up=nu['uphosts'],down=nu['downhosts'],total=nu['totalhosts'])
        for host, detail in scan_raw_result['scan'].items():
            ipItem=listDeviceMsgResponse.ipam_items.add()
            ipItem.ip=host
            ipItem.status=detail['status']['state']
            if len(detail['osmatch']) > 0:
                ipItem.os=detail['osmatch'][0]['name']
            else:
                ipItem.os=''
            if 'mac' in detail['addresses']:
                ipItem.mac=detail['addresses']['mac']
            else:
                ipItem.mac='';    
        return listDeviceMsgResponse
    except Exception as e: 
        logger.error('scan %s error: %s' % (ip,e))
        raise e
             
def nmapSearch(ip):
    try:
        nm = nmap.PortScanner()
        # 配置nmap扫描参数
        scan_raw_result = nm.scan(hosts=ip, arguments='-sS -F -O')
        res=scan_raw_result['nmap']['scanstats']
        ipItem = ipam_pb3.IpamItem()
        ipItem.ip=ip
        if len(scan_raw_result['scan']) != 0:
            ipItem.status=scan_raw_result['scan'][ip]['status']['state']
            ipItem.os=scan_raw_result['scan'][ip]['osmatch'][0]['name']
        response = ipam_pb2.GetDeviceMsgResponse(ipam_item=ipItem)
        return response
    except Exception as e:
        logger.error('scan %s error: %s' % (ip,e))
        raise e
  	 
def getDeviceSubnet():
    try:
        val = str(os.popen("ip r|awk '{print $1}'|grep /").read())
        # 配置nmap扫描参数
        response = ipam_pb2.GetDeviceSubnetResponse()
        response.subnets.extend(re.split('\n',val.strip()))
        return response
    except Exception as e:
        logger.error('get subnet error: %s' % (e))
        raise e    
    
def main():
    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 实例化 计算len的类
    servicer = NmapService()
    # 注册本地服务,方法ComputeServicer只有这个是变的
    ipam_pb2_grpc.add_DeviceServiceServicer_to_server(servicer, server)
    # 监听端口
    port = getPort()
    server.add_insecure_port('[::]:'+port)
    # 开始接收请求进行服务
    server.start()
    logger.info('nmap-driver server start port = %s' % port)
    server.wait_for_termination()
    logger.info('nmap-driver server stop port = $s' % port)

def getPort():
    cf = configparser.ConfigParser()
    cf.read(root_dir+"/config"+"/config.ini") 
    port = cf.get("Nmap-Driver", "port")
    return port

if __name__ == '__main__':
    main()


