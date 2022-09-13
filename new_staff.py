try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}
import time
import uuid
import json
import hashlib
import requests
import datetime
import numpy as np
import pandas as pd
from deepfos.api.space import SpaceAPI
from deepfos.element.datatable import DataTableMySQL
from deepfos.element.dimension import Dimension, DimMember


class NewStaff:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.app = p1['app']
        self.space = p1['space']
        self.operateUserId = p1['user']
        self.cookie = p1['cookie']

        self.sapi = SpaceAPI(header=p1, sync=True)

        self.timeStamp = str(int(round(time.time() * 1000)))
        self.platformCode = 'OSalpha'
        self.platformSecret = 'E276g88TerSllV55YzBRi89r1TnY65q05isLQNe6B9Eg12BL28'
        self.enterpriseId = '2834fb13-2e34-4399-9e59-63b7c53e8746'
        self.sign_str = f"""{self.timeStamp}&@&{self.operateUserId}&@&{self.platformCode}&@&{self.platformSecret}"""

        self.emp_name = p2['emp_name']
        self.emp_id = p2['emp_id']
        self.email = p2['email']
        self.dept_name = p2['dept_name']
        self.emp_post = p2['emp_post']
        self.emp_status = p2['emp_status']

        self.project_name = 'NoProjectMembers'
        self.project_role = '02'
        self.whether_to_assess = '1'
        self.participation_status = '1'

    def insert_data2mysql_table(self):
        """向项目信息表插入一条新成员项目数据"""
        Project_Info = DataTableMySQL("Project_Info")
        df_insert = pd.DataFrame(
            {'emp_id': [self.emp_id], 'project_name': ['' if self.emp_post == '01' else self.project_name], 'project_role': [self.project_role],
             'whether_to_assess': [self.whether_to_assess],
             'participation_status': [self.participation_status]})
        Project_Info.insert_df(df_insert)

    def add_dimmember(self):
        """向Entity维度增加该成员"""
        dim = Dimension("Entity")
        is_active = True if self.emp_status == 'True' else False
        if self.emp_post == '02':
            sharedmember = True
            dim.add_member(
                DimMember(name=self.emp_id, parent_name=self.project_name, multilingual={'zh-cn': self.emp_name, 'en': ''}, is_active=is_active, sharedmember=sharedmember))
            dim.save()
            for i in range(len(self.dept_name) - 1, -1, -1):
                if i == 0:
                    sharedmember = False
                dim.add_member(
                    DimMember(name=self.emp_id, parent_name=self.dept_name[i], multilingual={'zh-cn': self.emp_name, 'en': ''}, is_active=is_active, sharedmember=sharedmember))
                dim.save()
        else:
            dim.add_member(
                DimMember(name=self.emp_id, parent_name='DepartmentHead', multilingual={'zh-cn': self.emp_name, 'en': ''}, is_active=is_active))
            dim.save()

    def judge_dimmember_exist_or_not(self):
        """判断Entity维度是否已存在该成员， 存在则先删除"""
        flag = False
        dim = Dimension("Entity")
        dim_data = dim.query(expression=f'Base(OrganizationalStructure,0)', fields=['name', 'parent_name', 'is_active', 'sharedmember'])
        for d in dim_data:
            if d.name == self.emp_id:
                flag = True
        return flag

    def delete_dimmenber(self):
        """删除Entity维度该成员"""
        Entity_td = DataTableMySQL("Entity_td")
        t_name = Entity_td.table_name
        sql = '''
                        delete from %s where name = '%s'
                        ''' % (t_name, self.emp_id)
        Entity_td.run_sql(sql)

    def add_space_user(self):
        """新增空间用户"""
        new_user_info = {
            'username': self.emp_id,
            'nickname': self.emp_name,
            'status': self.emp_status,
            'email': self.email,
            'mobilePhone': '',
            'password': '@deepfinance' + self.emp_id,
            'userId': str(uuid.uuid4()),
            'userTag': '1'
        }
        # 第一步：生成验签
        hl = hashlib.md5()
        hl.update(self.sign_str.encode(encoding='utf-8'))
        sign_result = hl.hexdigest()

        # 第二步：将新职员导入企业
        import_user_url = "https://alpha-account.deepfos.com/system-account-api/s/user/import/user"
        import_user_headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "platform-code": self.platformCode,
            "platform-secret": self.platformSecret,
            "sign": sign_result,
            "user": self.operateUserId,
            "timestamp": self.timeStamp,
            "space": self.space,
            "enterprise-id": self.enterpriseId
        }
        import_user_params = {
            "data": [
                new_user_info
            ],
            "enterpriseId": "",
            "platformCode": self.platformCode,
            "sendEmail": False,
            "spaceId": self.space,
            "spaceName": "",
            "tag": "INCREMENT"
        }
        requests.post(url=import_user_url, headers=import_user_headers, data=json.dumps(import_user_params))

        # 第三步：邀请用户至'绩效管理产品'空间
        invitation_url = 'https://alpha-account.deepfos.com/system-account-api/api/user/invitation/space/invitation'
        invitation_headers = {
            "content-type": "application/json;charset=UTF-8",
            "Cookie": self.cookie
        }
        invitation_body = {
            "platformCode": self.platformCode,
            "spaceId": self.space,
            "users": [{"userId": new_user_info['userId'], "userName": new_user_info['username']}]
        }
        requests.post(url=invitation_url, headers=invitation_headers, data=json.dumps(invitation_body))

        # 第四步：分配'考核及周报'应用成员角色
        role_url = 'https://alpha-account.deepfos.com/system-account-api/api/user/space/modify-user-detail'
        role_headers = {
            "content-type": "application/json;charset=UTF-8",
            "Cookie": self.cookie
        }
        role_body = {
            "userId": new_user_info['userId'],
            "enterpriseId": self.enterpriseId,
            "status": 1,
            "userRoleInfoSaveDTOList": [{"platformCode": self.platformCode,
                                         "children": [{"code": "uhovff001", "tag": "app", "roleList": ["-4"]}]}],
            "space": self.space
        }
        requests.post(url=role_url, headers=role_headers, data=json.dumps(role_body))


def main(p1, p2):
    new_staff = NewStaff(p1, p2)
    flag = new_staff.judge_dimmember_exist_or_not()
    if flag:
        new_staff.delete_dimmenber()
        new_staff.add_dimmember()
    else:
        new_staff.insert_data2mysql_table()
        new_staff.add_dimmember()

    print("Hello world!")


if __name__ == '__main__':
    main(para1, para2)
