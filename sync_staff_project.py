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

    Project_Info = DataTableMySQL("Project_Info")
    SAPI = SpaceAPI(header=p1, sync=True)
    dim = Dimension("Entity")
    mbrs = dim.query('AndFilter(Base(ProjectMembers,0),Attr(is_active,1))', fields=['name', 'parent_name', 'multilingual'])
    df_insert = pd.DataFrame(columns=['emp_id', 'project_name', 'project_role', 'whether_to_assess', 'participation_status'])

    for m in mbrs:
        emp_name = m.multilingual['zh-cn']
        spaceUserInfo = SAPI.user.all_enable_user(keyword=emp_name)
        if spaceUserInfo is None:
            continue
        emp_id = m.name
        project_name = m.parent_name
        project_role = '02'
        whether_to_assess = '1'
        participation_status = '1'
        df_temp = pd.DataFrame({'emp_id': [emp_id], 'project_name': [project_name], 'project_role': [project_role], 'whether_to_assess': [whether_to_assess], 'participation_status': [participation_status]})
        df_insert = df_insert.append(df_temp)
    Project_Info.insert_df(df_insert, chunksize=5000, auto_fit=True)


if __name__ == '__main__':
    main(para1, para2)
