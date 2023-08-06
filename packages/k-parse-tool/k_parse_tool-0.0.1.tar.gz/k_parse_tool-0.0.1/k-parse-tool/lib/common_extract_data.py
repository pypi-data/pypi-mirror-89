import re
import regex
from k_parse_tool.Enum.ItemPropertyEnum import ItemPropertyEnum

from k_parse_tool.Enum.fix_const_enum import FixConstEnum
from prettytable import basestring


from k_parse_tool.lib.column_common_reg import LawAccordingReg, AdminPenaltyDateReg, AdminPenaltyDeptReg, \
    AdminPenaltyNumberReg, AdminPenaltyPunishedPartiesReg, AdminPenaltyPunishedPeopleReg, \
    AdminPenaltyPunishedMeasuresReg


class CommonExtractData:


    @staticmethod
    def extract_data_by_common_reg(item, resource, reg_dict):

        reg_dict = CommonExtractData.add_data_to_item_by_common_reg_from_resource(reg_dict)

        CommonExtractData.extract_data_from_dict_and_resource(reg_dict, resource, item)


    @staticmethod
    def add_data_to_item_by_common_reg_from_resource(reg_dict):

        if len(reg_dict) == 0 or reg_dict is None:
            reg_dict = {}
        #发布部门
        if ItemPropertyEnum.DETAIL_PAGE_DEPT.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_DEPT.value] = AdminPenaltyDeptReg.getCommonDeptReg()
        # 处罚日期
        if ItemPropertyEnum.DETAIL_PAGE_DATE.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_DATE.value] = AdminPenaltyDateReg.getCommonAdminPenaltyDateReg()
        # 发文字号
        if ItemPropertyEnum.DETAIL_PAGE_TEXT_NUMBER.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_TEXT_NUMBER.value] = AdminPenaltyNumberReg.getCommonNumberReg()

        # 法律依据
        if ItemPropertyEnum.DETAIL_PAGE_LAWACCORDING.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_LAWACCORDING.value] = LawAccordingReg.getCommonLawAccordingReg()
        # 处罚对象(公司)
        if ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PARTIES.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PARTIES.value] = AdminPenaltyPunishedPartiesReg.getCommonPunishedPartiesReg()
        # 处罚负责人
        if ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PEOPLE.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_PUNISHED_PEOPLE.value] = AdminPenaltyPunishedPeopleReg.getCommonPunishedPeopleReg()
        # 处罚结果
        if ItemPropertyEnum.DETAIL_PAGE_PUNISHMENT_MEASURES.value not in reg_dict.keys():
            reg_dict[ItemPropertyEnum.DETAIL_PAGE_PUNISHMENT_MEASURES.value] = AdminPenaltyPunishedMeasuresReg.getCommonPunishedMeasuresReg()
        return reg_dict


    @staticmethod
    # reg_dict  的key 是item的属性名称,  value  是提取该属性的正则表达式
    def extract_data_from_dict_and_resource(reg_dict, resource, item):
        if (len(reg_dict) > 0):
            for key, value in reg_dict.items():
                if key not in item.keys():
                    end_value = ""
                    # 法律依据提取多条
                    if key == ItemPropertyEnum.DETAIL_PAGE_LAWACCORDING.value:
                        list_value = regex.findall(value, resource)
                        end_value = "\r\n".join(list_value) if len(list_value) > 0 else end_value
                        end_value = CommonExtractData.get_law_according(end_value)
                    else:
                        reg_result = regex.search(value, resource)
                        if (reg_result):
                            end_value = reg_result.group()

                    item[key] = end_value

    @staticmethod
    def join_post_params_and_url(url, post_params):
        is_str = isinstance(post_params, basestring)
        join_str = ''
        if is_str:
            join_str = url+'<POST>'+post_params+'</POST>'
        else:
            str_list =[]
            for key, value in post_params.items():
                str_list.append(str(key)+'='+str(value))
            join_str = "&".join(str_list)
            join_str = url+'<POST>'+join_str+'</POST>'
        return join_str

    @staticmethod
    def get_content_by_reg(resource, reg, search_full):
        dict = {}
        dict[FixConstEnum.REG_CONTENT.value] = ""

        if search_full:
            list_value = regex.findall(reg, resource)
            dict[FixConstEnum.REG_CONTENT.value] = list_value
        else:
            reg_result = regex.search(reg, resource, regex.I)
            if (reg_result):
                end_value = reg_result.group()
                dict[FixConstEnum.REG_CONTENT.value] = end_value
        return dict

    @staticmethod
    def get_law_according(resource):
        law_reg = LawAccordingReg.getCommonLawAccordingReg()
        list_value = regex.findall(law_reg, resource)
        end_value = "\r\n".join(list_value) if len(list_value) > 0 else ''
        return end_value