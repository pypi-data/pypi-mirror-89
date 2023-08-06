from k_parse_tool.Enum.ItemPropertyEnum import ItemPropertyEnum

table_title = {
    ItemPropertyEnum.DETAIL_PAGE_TITLE.value:
        [u'案件名称', u'案件名称：', u'案件名称:', u'处罚名称', u'项目名称：'],  # 标题
    ItemPropertyEnum.DETAIL_PAGE_DEPT.value:
        [u'作出处罚决定的机关名称', u'执法主体', u'许可机关:', u'处罚机关', u'处罚机关:', u'处罚机关：',
         u'登记机关', u'做出处罚的机关名称和日期', u'作出处罚的机关名称和日期', u'作出处罚机关名称和日期',
         u'作出处罚决定的部门', u'执法单位名称', u'作出处罚单位名称'],  # 发布部门
    ItemPropertyEnum.DETAIL_PAGE_DATE.value:
        [u'作出处罚的日期', u'日期', u'处罚决定日期:', u'处罚生效期：', u'处罚日期', u'处罚生效期起', u'作出决定时间',
         u'做出处罚的机关名称和日期', u'作出处罚的机关名称和日期', u'作出处罚机关名称和日期', u'处罚决定日期：',
         u'作出处理决定的机关名称和日期', u'签发日期', u'处罚决定作出日期'],  # 发布时间
    ItemPropertyEnum.DETAIL_PAGE_TEXT_NUMBER.value:
        [u'行政处罚决定书文号', u'处罚决定书文号', u'行政处罚决定文书号：', u'文书字轨', u'行政处罚决定书文号：',
         u'行政处罚决定书文号:', u'行政处理决定书文号', u'行政决定书文号', u'处罚许可决定书文号:', u'决定书号'],  # 发文字号
    ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PARTIES.value:
        [u'被处罚自然人姓名、被处罚企业或其他组织名称', u'行政相对人', u'行政相对人名称：', u'行政相对人名称:',
         u'纳税人名称', u'违法企业名称或违法自然人姓名', u'被处罚人', u'被处罚对象', u'被处罚人名称', u'被处罚单位（人）名称',
         u'当事人名称'],  # 被处罚对象
    ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PEOPLE.value:
        [u'负责人姓名', u'法定代表人', u'法定代表人姓名：', u'法人代表姓名:', u'法人代表姓名：',
         u'行政处罚相对人姓名', u'经营者', u'法定代表人:'],  # 被处罚人
    ItemPropertyEnum.DETAIL_PAGE_LAWACCORDING.value:
        [u'处罚依据', u'执法依据', u'处罚依据:', u'处罚依据：', u'行政处罚依据',
         u'行政处罚的种类和依据', u'行政处理的种类和依据'],  # 法律依据
    ItemPropertyEnum.DETAIL_PAGE_PENALTYACCORDING.value:
        [u'案由', u'事由', u'处罚事由', u'处罚依据'],  # 处罚依据
    ItemPropertyEnum.DETAIL_PAGE_PUNISHMENT_MEASURES.value:
        [u'处罚结果', u'处罚结果：', u'处罚结果:', u'罚款结果', u'行政处罚结果',
         u'处理结果', u'处罚内容:', u'处罚决定内容', u'处罚措施', u'处罚金额'],  # 处罚结果
}
