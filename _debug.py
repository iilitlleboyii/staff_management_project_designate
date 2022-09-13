from deepfos.options import OPTION

# -----------------------------------------------------------------------------
# 从系统中获取以下参数
#: 环境参数
para1 = {'app': 'eijuqd005', 'space': 'eijuqd', 'user': 'ab7e4870-6fa2-4507-aa4b-bda02099c676', 'language': 'zh-cn', 'token': '452C0648C157674C88582419B2820560D2ED4F93209D24561AD8CCAEE226E6C9',
         'cookie': 'cloud_deepfos_users=%7B%22color%22%3A%224%22%2C%22email%22%3A%22xianhao.yu%40deepfinance.com%22%2C%22invitationActivation%22%3Atrue%2C%22mobilePhone%22%3A%2217671003464%22%2C'
                   '%22nickName%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22nickname%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22token%22%3A'
                   '%2298DE97A98C001D8F4166F0DDA27C6E9844BBD7D804D9B122FA481782A31A6B8A%22%2C%22tokenKey%22%3A%22cloud_deepfos_token%22%2C%22type%22%3A1%2C%22userId%22%3A%228001ce0d-7b0c-404f-b29e'
                   '-b7eb5c6812f6%22%2C%22username%22%3A%22yuxianhao%22%7D; cloud_deepfos_token=98DE97A98C001D8F4166F0DDA27C6E9844BBD7D804D9B122FA481782A31A6B8A; '
                   'alpha_deepfos_users=%7B%22color%22%3A%224%22%2C%22email%22%3A%22xianhao.yu%40deepfinance.com%22%2C%22invitationActivation%22%3Atrue%2C%22mobilePhone%22%3A%2217671003464%22%2C'
                   '%22nickName%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22nickname%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22token%22%3A'
                   '%22452C0648C157674C88582419B2820560D2ED4F93209D24561AD8CCAEE226E6C9%22%2C%22tokenKey%22%3A%22alpha_deepfos_token%22%2C%22type%22%3A1%2C%22userId%22%3A%22ab7e4870-6fa2-4507-aa4b'
                   '-bda02099c676%22%2C%22username%22%3A%22Axian%22%7D; alpha_deepfos_token=452C0648C157674C88582419B2820560D2ED4F93209D24561AD8CCAEE226E6C9',
         'envUrl': 'http://web-gateway'}

#: 业务参数
para2 = {'emp_id': 'zhongqiukuaile2', 'emp_name': '中秋快乐2', 'email': '未知邮箱', 'dept_name': ['TechnologyBusinessDepartment', 'PanRealEstateBusinessDepartment'], 'emp_post': '02', 'emp_status': 'True'}

#: 环境域名，根据自己的使用环境更改
host = "https://alpha.deepfos.com"

# -----------------------------------------------------------------------------
# 下面的代码是固定的

OPTION.general.use_eureka = False
OPTION.server.base = f"{host}/seepln-server"
OPTION.server.app = f"{host}/seepln-server/app-server"
OPTION.server.system = f"{host}/seepln-server/system-server"
OPTION.server.space = f"{host}/seepln-server/space-server"
OPTION.server.platform_file = f"{host}/seepln-server/platform-file-server"
OPTION.api.header = para1
OPTION.api.dump_on_failure = True
