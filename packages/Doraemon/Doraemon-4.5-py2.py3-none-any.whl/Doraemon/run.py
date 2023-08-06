from Doraemon import investigation

# set arguments
key_word_list = ["山东华骜植化", "华泰证券", "广发证券", "海通证券"]  # organizations
api_key = "7dab451889b5f88db606750d615d9824"  # api key for captcha recognition, https://www.3023data.com/
save_dir = "./temp"  # path to save
# switch for websites
switch = {
    "baidu": True,  # 百度
    "neris": True,  # 中国证监会证券期货市场失信检索结果
    "mee_gov": True,  # 中华人民共和国生态环境部检索结果
    "mnr_gov": True,  # 中华人民共和国自然资源部检索结果
    "china_tax": True,  # 国家税务局重大税收违法案件信息公布栏检索结果
    "zxgk": True,  # 全国法院被执行人信息检索结果
}

# no need to change
investigator = investigation.OrgInvestigator(api_key)
investigator.investigate(key_word_list, save_dir, switch)
investigator.quite()