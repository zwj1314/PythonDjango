# -*- coding: gbk -*-

from bs4 import BeautifulSoup
import requests
import xlrd
import xlwt
from xlutils.copy import copy
import time
import winsound

#������վ������
class EnterpriseInfoSpider:
    def __init__(self):

        #�ļ����
        self.excelPath = 'enterprise_data.xls'
        self.sheetName = 'details'
        self.workbook = None
        self.table = None
        self.beginRow = None

        # Ŀ¼ҳ
        self.catalogUrl = "http://www.qichacha.com/search_index"

        # ����ҳ��ǰ׺+firmXXXX+��׺��
        self.detailsUrl = "http://www.qichacha.com/company_getinfos"

        self.cookie = input("������cookie:").decode("gbk").encode("utf-8")
        self.host = "www.qichacha.com"
        self.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"

        self.headers = {
            "cookie" : self.cookie,
            "host" : self.host,
            "user-agent" : self.userAgent
        }

        #�����ֶ���17��
        self.fields = ['��˾����','�绰����','����','ͳһ������ô���','ע���','��֯��������','��Ӫ״̬','��˾����','��������','����������','ע���ʱ�',
                       'Ӫҵ����','�Ǽǻ���','��������','��˾��ģ','������ҵ','Ӣ����','������','��ҵ��ַ','��Ӫ��Χ']

    #���濪ʼǰ��һЩԤ����
    def init(self):
        try:
            #��̽�Ƿ��и�excel�ļ���#��ȡ������workbook.sheets()[0].nrows
            readWorkbook = xlrd.open_workbook(self.excelPath)
            self.beginRow = readWorkbook.sheets()[0].nrows #��ȡ����
            self.workbook = copy(readWorkbook)
            self.table = self.workbook.get_sheet(0)

        except Exception,e:
            print(e)
            self.workbook = xlwt.Workbook(encoding='utf-8')
            self.table = self.workbook.add_sheet(self.sheetName)

            #������ͷ�ֶ�
            col = 0
            for field in self.fields:
                self.table.write(0,col,field.decode('gbk').encode('utf-8'))
                col += 1

            self.workbook.save(self.excelPath)
            self.beginRow = 1
            print("���ڵ�ǰĿ¼�´���enterprise_data.xls���ݱ�")


    #��keyword/1ҳ �õ���html�л����ҳ����
    def getTotalPage(self,catalogPageCode):
        soup = BeautifulSoup(catalogPageCode,"html.parser")
        pagebar = soup.select("li #ajaxpage")
        if pagebar == None or pagebar == []:
            return -1
        return int(soup.select("li #ajaxpage")[-1].string.strip(' .'))

    #��keyword/pageҳ �õ�html�е����й�˾��Ŀ
    def getFirmIdDoms(self,catalogPageCode):
        soup = BeautifulSoup(catalogPageCode,"html.parser")
        return soup.select("#searchlist .table-search-list .tp2 a")

    #���濪ʼ
    def start(self):
        keyword = input("������ؼ��֣�").decode("gbk").encode("utf-8")
        while keyword != "end":
            #�Ȼ�ȡkeyword��һҳ���ݵ�ҳ��
            totalPage = self.getTotalPage(self.getCatalogPageCode(keyword, 1))
            if totalPage == -1:
                # ������һ�ֲ�ѯ�Ĺؼ���
                keyword = input("��ȡ����,������ؼ��֣�").decode("gbk").encode("utf-8")
                continue

            #ģ�ⷭҳ����
            for page in range(1,totalPage+1):

                print("������ȡ��")  + page + ("ҳ������,���Ե�...")

                #��ȡ��pageҳ����
                catalogPageCode = self.getCatalogPageCode(keyword,page)
                firmIdDoms = self.getFirmIdDoms(catalogPageCode)
                for firmIdDom in firmIdDoms:
                    firmId = firmIdDom['href'][6:-6]
                    companyname = "" #��˾��
                    for string in firmIdDom.strings:
                        companyname += string

                    tdDom = firmIdDom.find_parent().find_parent()
                    phoneDom = tdDom.select('.i-phone3')
                    emailDom = tdDom.select('.fa-envelope-o')
                    phone = ""
                    email = ""
                    if phoneDom != None and phoneDom != []:
                        phone = phoneDom[0].next_sibling.strip() #�ֻ�
                    if emailDom != None and emailDom != []:
                        email = emailDom[0].next_sibling.strip() #����

                    detailsPageCode = self.getDetailsPageCode(firmId,companyname)
                    self.writeDetailsToExcel(detailsPageCode,companyname,phone,email)
                    time.sleep(0.3) #0.5s��������ֹ���������

            #������һ�ֲ�ѯ�Ĺؼ���
            keyword = input("��ȡ����,������ؼ��֣�").decode("gbk").encode("utf-8")

        print("��������ȫ������")

    #����keyword��page�����ѯ��
    #����keyword�еĿո񻻳�+
    #���ز�ѯ�ַ������ɵ��ֵ�
    def getCatalogQueryString(self,keyword,page):
        keyword.replace(' ','+')
        return {"key": keyword, "index": "0", "p": page}

    def getDetailQueryString(self,firmId,companyname):
        return {"unique": firmId, "companyname":companyname,"tab": "base"}

    # ����keyword�ؼ��ֻ�ȡĿ¼ҳ����
    def getCatalogPageCode(self, keyword, page):
        queryString = self.getCatalogQueryString(keyword, page)
        response = requests.request("GET", self.catalogUrl, headers=self.headers, params=queryString)
        return response.text

    # ����firmId��ȡ��˾������ҳ����
    def getDetailsPageCode(self,firmId,companyname):
        queryString = self.getDetailQueryString(firmId,companyname)
        response = requests.request("GET", self.detailsUrl, headers=self.headers, params=queryString)
        return response.text

    #ץȡdetailsPageCodeҳ�ϸ���ҵ������Ϣ��������excel
    def writeDetailsToExcel(self,detailsPageCode,companyname,phone,email):
        detailDoms = self.getDetailDoms(detailsPageCode)

        self.table.write(self.beginRow, 0, companyname)
        self.table.write(self.beginRow, 1, phone)
        self.table.write(self.beginRow, 2, email)

        col = 3
        for detailDom in detailDoms:
            detailName = detailDom.label.string.strip()[:-1]
            detailValue = detailDom.label.next_sibling.string.strip()
            while col < len(self.fields):
                # �ҵ�ƥ��������ֶ�
                if detailName == self.fields[col].decode('gbk'):
                    self.table.write(self.beginRow, col, detailValue) #д��excel
                    col += 1
                    break
                else:
                    col += 1
        self.workbook.save(self.excelPath)  # �������ļ�
        self.beginRow += 1

    #����detailsPageCode�����������detailDomsԪ��
    def getDetailDoms(self,detailsPageCode):
        soup = BeautifulSoup(detailsPageCode,"html.parser")
        return soup.select(".company-base li")



########
#�������
########
spider = EnterpriseInfoSpider()
spider.init()
spider.start()