# -*- coding: utf-8 -*-
import os
import boto3
import json
import csv
from datetime import datetime

count = 0;
regionIDs = ['us-east-1',
             'us-east-2',
             'us-west-1',
             'us-west-2',
             'ca-central-1',
             'eu-central-1',
             'eu-west-1',
             'eu-west-2',
             'eu-west-3',
             'ap-northeast-1',
             'ap-northeast-2',
             'ap-southeast-1',
             'ap-southeast-2',
             'ap-south-1',
             'sa-east-1']
regionNames = ['美国东部（弗吉尼亚北部）',
               '美国东部（俄亥俄州）',
               '美国西部（加利福尼亚北部）',
               '美国西部（俄勒冈）',
               '加拿大 (中部)',
               '欧洲（法兰克福）',
               '欧洲（爱尔兰）',
               '欧洲 (伦敦)',
               '欧洲 (巴黎)',
               '亚太区域（东京）',
               '亚太区域（首尔）',
               '亚太区域（新加坡）',
               '亚太区域（悉尼）',
               '亚太地区（孟买）',
               '南美洲（圣保罗）']
def describe_instances(client):
    response = client.describe_instances()
    return response

def analysisInfoDict(response,regionName):
    reservations = response['Reservations']
    print ("实例数量：%s   " % (len(reservations)))
    for  reservation in reservations:
        Instances = reservation['Instances']
        analysisInstance(Instances,regionName)

def analysisInstance(Instancess,regionName):
    for Instances in Instancess:
        State = Instances['State']
        #IpAddresses = Instances['NetworkInterfaces'][0]['PrivateIpAddresses'][0]
        SecurityGroup = Instances['SecurityGroups'][0]
        AZ = Instances['Placement']['AvailabilityZone']
        LaunchTime = Instances['LaunchTime']
        Monitoring = Instances['Monitoring']
        Placement = Instances['Placement']
        TagsName = ''
        TagsOwner = ''
        Tags = []
        try:
            Tags = Instances['Tags']
            for tag in Tags:
                if tag['Key'] == 'Name':
                    TagsName = tag.get('Value','-')
                    break;
            for tag in Tags:
                if tag['Key'] == 'Owner':
                    TagsOwner = tag.get('Value','-')
                    break;
        except KeyError as e:
            print('-----------------------')
            print('except:', e)
            print(Instances)
            print('-----------------------')
        line = [TagsName,TagsOwner,Instances.get('InstanceId','-'),Instances.get('InstanceType','-'),Instances.get('Platform','-'),
                Instances.get('SubnetId','-'),Instances.get('VpcId','-'),State.get('Name','-'),Instances.get('PublicIpAddress','-'),Instances.get('PrivateIpAddress','-'),AZ,Instances.get('KeyName','-'),
                Monitoring.get('State','-'),LaunchTime,SecurityGroup.get('GroupName','-'),Placement.get('Tenancy','-'),regionName]
        saveStringToCsv(line)

def saveStringToCsv(inputString):
    global count
    count = count + 1
    #f = open("C:/Users/MSI/Desktop/python_work/result/volumes.csv", "w")
    out = open('C:/Users/Hui57/Desktop/python_work/result/DH_instances.csv','a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    csv_write.writerow(inputString)
    #print(count)
    #print("%3s" % (inputString), file = f)
    #f.close()

def saveInfoToTxt(inputString):
    f = open("C:/Users/Hui57/Desktop/python_work/result/DH_instances.txt", "w")
    print("%3s" % (inputString), file = f)
    f.close()

def mainThread():
    title = ['Name','Owner','InstanceId','InstanceType','Platform','SubnetId','VpcId','State','publicIP','privateIP','可用区','秘钥名称','监控','启动时间','安全组','Tenancy','region'];
    saveStringToCsv(title)
    for i in range(len(regionIDs)):
        client = boto3.client('ec2',region_name =regionIDs[i])
        response = describe_instances(client);
        inputString = analysisInfoDict(response,regionNames[i]);
        print ("代码：%s   名称：%s" % (regionIDs[i], regionNames[i]))
    

mainThread();
