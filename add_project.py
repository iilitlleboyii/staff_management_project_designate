try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}
from deepfos.element.dimension import Dimension, DimMember


def main(p1, p2):
    # {'project_id': 'project_test', 'project_name': '项目测试'}
    dim = Dimension("Entity")
    project_id = p2['project_id']
    project_name = p2['project_name']
    parent_name = 'ProjectMembers'
    dim.add_member(DimMember(name=project_id, parent_name=parent_name, multilingual={'zh-cn': project_name, 'en': project_id}))
    dim.save()
    # print("Hello world!")


if __name__ == '__main__':
    main(para1, para2)
