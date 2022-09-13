try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}
from deepfos.element.datatable import DataTableMySQL
from deepfos.element.dimension import Dimension, DimMember
from deepfos.api.space import SpaceAPI
import pandas as pd
import numpy as np
import time


def main(p1, p2):
    Emp_Info = DataTableMySQL("Emp_Info")
    SAPI = SpaceAPI(header=p1, sync=True)
    dim = Dimension("Entity")
    mbrs = dim.query('AndFilter(Base(OrganizationalStructure,0),Attr(is_active,1))', fields=['name', 'parent_name', 'multilingual'])
    df_insert = pd.DataFrame(columns=['emp_id', 'email', 'emp_name', 'emp_post', 'dept_name', 'emp_status'])

    for m in mbrs:
        emp_name = m.multilingual['zh-cn']
        spaceUserInfo = SAPI.user.all_enable_user(keyword=emp_name)
        if spaceUserInfo is None:
            continue
        emp_id = m.name
        email = spaceUserInfo[0].email
        dept_name = m.parent_name
        emp_post = '01' if dept_name == 'DepartmentHead' else '02'
        emp_status = 'True'
        df_temp = pd.DataFrame({'emp_id': [emp_id], 'email': [email], 'emp_name': [emp_name], 'emp_post': [emp_post], 'dept_name': [dept_name], 'emp_status': [emp_status]})
        df_insert = df_insert.append(df_temp)
    Emp_Info.insert_df(df_insert, chunksize=5000, auto_fit=True)


if __name__ == '__main__':
    main(para1, para2)
