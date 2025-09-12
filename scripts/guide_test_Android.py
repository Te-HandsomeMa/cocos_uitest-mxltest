import asyncio
import os
import sys
import argparse
from datetime import datetime

from common.base_page import BasePage
from common.ws_server import rpc_server
from configs.element_data import ElementsData
from configs.port_config import get_port_info
from common.log import LoggerWriter
from common.ding import send_dingding_error,send_dingding



async def chapter_one(bp: BasePage):
    """第一章"""
    perform_list = [
        ElementsData.UIStoryRecount.lab_continue,     # 1
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportPromote.UISupportPromote,     # 5
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.choice2,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
        ElementsData.UIBuildingConstruct.build,     # 10
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.building_add,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
        ElementsData.UIBuildingConstruct.build,     # 15
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.building_add,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIStoryDialogue.lab_continue,     # 20
        ElementsData.UIStoryGuide.hand,
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,
        ElementsData.UiSupportWorkAdopt.hand,     # 25
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIFunctionUnlock.lab_press_any,
        ElementsData.UILevelHUD.hand,
        ElementsData.UiMission.close,
    ]
    print("================第一章开始======================")
    print("====click_a_until_b_appear_list：chapter_one_perform_list====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list, interval=0.2)
    await bp.click_until_disappear(element_data=ElementsData.UiMission.close)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.task_effect)


    perform_list_1 = [
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuildingConstruct.build,
    ]
    print("====click_a_until_b_appear_list：chapter_one_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.2)
    await bp.click_until_disappear(element_data=ElementsData.UIBuildingConstruct.build)

    perform_list_2 = [
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.building_add,
        ElementsData.UILevelHUD.task_effect,     # 5
        ElementsData.UILevelHUD.task
        ]
    print("====click_a_until_b_appear_list：chapter_one_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.2)

    perform_list_3 = [
        ElementsData.UILevelHUD.task_effect,     # 1
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,     # 5
        ElementsData.UIBuildingUnlock.lab_continue,
        ElementsData.UILevelHUD.task_effect,
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue,     # 10
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportPromote.UISupportPromote
    ]
    print("====click_a_until_b_appear_list：chapter_one_perform_list_3====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.2)
    await bp.click_until_disappear(element_data=ElementsData.UISupportPromote.UISupportPromote)
    print("================第一章结束======================")


async def chapter_two(bp: BasePage):
    """第二章"""
    perform_list = [
        ElementsData.UIStoryDialogue.lab_continue,   # 1
        ElementsData.UIStoryDialogue.choice2,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.guide_rect,   # 5
        ElementsData.UISupportManagement.hand,
        ElementsData.UIBuildingConstruct.build,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.building_add,   # 10
        ElementsData.UICommonPopup4.confirm,
        ElementsData.UiSupportWorkAdopt.btn_adopt,
        ElementsData.UIBuilding.hand,
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.prob_btn,   # 15
        ElementsData.UiSupportWorkAdopt.btn_adopt,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.building_add,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.open_upgrade,   # 20
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,   # 25
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.prob_btn,
        ElementsData.UiSupportWorkAdopt.btn_adopt,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.hand,   # 30
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
    ]
    print("================第二章开始======================")
    print("====click_a_until_b_appear_list：chapter_two_perform_list====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list, interval=0.5)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.building_add)
    await bp.sleep(2)

    perform_list_1 = [ # 35
        ElementsData.UILevelHUD.xin_shou,#1
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.upgradeBtn,#5
        ElementsData.UIBuilding.task_effect,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou, #10
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.task_effect,
        ElementsData.UIFunctionUnlock.lab_press_any,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue, #15
        ElementsData.UIActivityXueyuan.hand,
        # ElementsData.UiArchiveInviteReward.close1,
        # ElementsData.UIActivityXueyuan.btn_aquire,
        # ElementsData.UIActivityXueyuan.btn_goto,
        ElementsData.UIActivityXueyuan.close,  ##小程序跑测取消注释该行，注释btn_aquire、btn_goto和close1
    ]
    print("====click_a_until_b_appear_list：chapter_two_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIActivityXueyuan.close)

    perform_list_2 = [
        ElementsData.UILevelHUD.xin_shou,    # 1
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,    # 5
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIChapterChangeTime.tap_close,
        ElementsData.UIBuildingUnlock.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.xin_shou,    # 10
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UiMission.btn_claim,    # 15
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryCartoon.UIStoryCartoon,
    ]

    print("====click_a_until_b_appear_list：chapter_two_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIStoryCartoon.UIStoryCartoon)
    print("================第二章结束======================")


async def chapter_three(bp: BasePage):
    """第三章"""
    perform_list = [
        ElementsData.UIStoryRecount.lab_continue,     # 1
        ElementsData.UILevelHUD.hand,  #民心
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UISupportManagement.hand,
        ElementsData.UIBuildingConstruct.hand, #医馆  #5
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,  #医馆任务完成
        ElementsData.UILevelHUD.xin_shou,  #煤矿升级
        ElementsData.UIBuilding.hand, #煤矿升级手点箭头
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,#升级  #10
        ElementsData.UILevelHUD.task_effect, #闪光效果判断
    ]
    print("================第三章开始======================")
    print("====click_a_until_b_appear_list：chapter_three_perform_list====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list, interval=0.2)

    perform_list_1 = [
        # ElementsData.UILevelHUD.task_effect, #闪光效果判断
        ElementsData.UILevelHUD.xin_shou,     # 1  原因：煤矿升级中点击了任务
        ElementsData.UIBuilding.upgradeBtn,  #猎人小屋升级
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab, #5
        ElementsData.UILevelHUD.xin_shou,   #民居甲
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.prob_btn,    #接纳流民
        ElementsData.UiSupportWorkAdopt.btn_adopt,
        ElementsData.UILevelHUD.xin_shou, #民居甲升级 #10
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou, #民居甲升级床铺  #15
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.task_effect,
        ElementsData.UILevelHUD.xin_shou, #伐木场
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,     # 20
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,  #厨房
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,     #25
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuilding.upgradeBtn,  #新  厨房
        ElementsData.UIBuilding.btn_splash,  # 30
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,#新

        ElementsData.UILevelHUD.xin_shou, #火炉
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,     # 35
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
    ]
    print("====click_a_until_b_appear_list：chapter_three_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.heart)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UISupportManagement.close)
    await bp.sleep(2)

    perform_list_2 = [
        ElementsData.UIBuildingUnlock.lab_continue, #1
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,
        ElementsData.UIReward.lab_continue, #5
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIRecruitNewHero.lab_tips,
        ElementsData.UILevelHUD.task_effect,

        ElementsData.UILevelHUD.xin_shou, #10
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportPromote.UISupportPromote,
        ElementsData.UILevelHUD.task_effect,
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue, #15
    ]
    print("====click_a_until_b_appear_list：chapter_three_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIReward.lab_continue)
    print("================第三章结束======================")


async def chapter_four(bp: BasePage):
    """第四章"""
    perform_list_1 = [
        ElementsData.UIStoryDialogue.lab_continue,  # 1
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIStoryDialogue.lab_continue,  # 5
        ElementsData.UIStoryDialogue.choice1,

        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.hand,
        ElementsData.BattleInGame.hand,
        ElementsData.UIBattleResultWin.lab_close,  # 10
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.hand,

        ElementsData.UIBuildingConstruct.build,  # 15
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
        ElementsData.UIRecruit.hand,
        ElementsData.UIRecruitNewHero.lab_tips,
        ElementsData.UIRecruit.return_btn, # 20

        ElementsData.UILevelHUD.hand,
        ElementsData.UIHeroList.hand,
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("================第四章开始======================")
    print("====click_a_until_b_appear_list：chapter_four_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroInfo.btn_back)

    perform_list_2 = [
        ElementsData.UIHeroList.closeBtn,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation,
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
    await bp.click_element_safe(element_data=ElementsData.UIBattleEmbattle.quick_formation)

    perform_list_3=[
        ElementsData.UIBattleEmbattle.start_battle,#1
        ElementsData.BattleInGame.hand,
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,   # 5
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIRecruit.basics_once,
        ElementsData.UIRecruitResult.lab_continue,
        ElementsData.UIRecruit.return_btn, # 10
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close,  # 15
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UiFirstPay.close,  #赵子龙
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_3====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.5)

    await bp.click_until_disappear(element_data=ElementsData.UiFirstPay.close)


    perform_list_4 = [
        ElementsData.UILevelHUD.xin_shou,   # 1
        ElementsData.UILevelHUD.hand,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,   # 5
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.BattleInGame.hand,
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UILevelHUD.xin_shou,   # 10
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIReward.lab_continue,

        ElementsData.UILevelHUD.hero,
        ElementsData.UIHeroList.cai, #15
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_4====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_4, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)
    await bp.click_element_safe(element_data=ElementsData.UIHeroList.closeBtn)

    perform_list_5 = [
        ElementsData.UIHeroList.guan,
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_5====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_5, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroList.closeBtn)


    perform_list_6 = [
        ElementsData.UILevelHUD.xin_shou, #1
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation,
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close,  # 5
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,
        ElementsData.UILevelHUD.xin_shou,#伐木场
        ElementsData.UIBuilding.upgradeBtn,  # 10
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
        ElementsData.UIBuilding.task_effect,
        ElementsData.UILevelHUD.xin_shou, #流民  #15
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_6====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_6, interval=0.5)
    print("click_element_safe")
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.xin_shou)
    await bp.sleep(3)
    await bp.click_element_safe(element_data=ElementsData.UiSupportWorkAdopt.btn_adopt)
    await bp.sleep(5)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.xin_shou)
    await bp.sleep(3)
    await bp.click_element_safe(element_data=ElementsData.UiSupportWorkAdopt.btn_adopt)
    await bp.sleep(3)
    await bp.click_element_safe(element_data=ElementsData.UIBuildingConstruct.build)
    await bp.sleep(5)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.xin_shou)
    await bp.sleep(3)
    await bp.click_element_safe(element_data=ElementsData.UiSupportWorkAdopt.btn_adopt)
    await bp.sleep(5)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.xin_shou)
    await bp.sleep(3)



    perform_list_7 = [
        ElementsData.UiSupportWorkAdopt.btn_adopt, # 1
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.prob_btn,
        ElementsData.UiSupportWorkAdopt.btn_adopt,

        ElementsData.UILevelHUD.xin_shou,#猎人 #5
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
        ElementsData.UIBuilding.task_effect,  # 10

        ElementsData.UILevelHUD.xin_shou, #医馆
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_7====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_7, interval=0.5)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    while True:
        await bp.click_element_safe(element_data=ElementsData.UIBuilding.upgradeBtn)
        if await bp.exist(element_data=ElementsData.ui_res_use_item.bu):
            print("判断")
            await bp.sleep(2)
            if not await bp.exist(element_data=ElementsData.ui_res_use_item.bu):
                print("不存在了")
                await bp.click_until_disappear(element_data=ElementsData.ui_res_use_item.close)
                continue
            await bp.click_a_until_b_appear(ElementsData.ui_res_use_item.bu,ElementsData.UiResQuickUse.confirm)
            await bp.click_until_disappear(element_data=ElementsData.UiResQuickUse.confirm)
            await bp.sleep(2)
            break
        elif await bp.exist(element_data=ElementsData.UIBuilding.btn_splash):
            print("判断2")
            await bp.sleep(2)
            break

    perform_list_8 = [
            ElementsData.UIBuilding.upgradeBtn,
            ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_8====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_8, interval=0.5)
    await bp.sleep(2)

    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    ###❌有问题
    await bp.click_until_disappear(ElementsData.UIBuilding.task_effect)
    await bp.sleep(2)

    perform_list_9 = [
        ElementsData.UILevelHUD.xin_shou, #火炉

        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
        ElementsData.UICommonPopup2.tog_check,
        ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_9====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_9, interval=0.5)

    await bp.click_element_safe(ElementsData.UICommonPopup2.tog_check)
    await bp.sleep(2)


    perform_list_10 = [
        ElementsData.UICommonPopup2.confirm, #1
        ElementsData.UIBuilding.task_effect,
        ElementsData.UIBuildingUnlock.lab_continue,
        ElementsData.UiActivitySevendays.close, #貂蝉

        ElementsData.UIFunctionUnlock.lab_press_any, #5

        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue
    ]
    print("====click_a_until_b_appear_list：chapter_four_perform_list_10====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_10, interval=0.5)
    print("================第四章结束======================")



async def chapter_five(bp: BasePage):
    """第五章"""
    perform_list = [
        ElementsData.UIStoryDialogue.lab_continue,  # 1
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UILevelHUD.xin_shou,  # todo 收复失地  5/10
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation, #5
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIReward.lab_continue, #10
        ElementsData.UILevelHUD.xin_shou,  # todo 收复失地  6/10
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation,
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close, #15
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,  # todo 收复失地  7/10  #20
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation,
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UILevelHUD.xin_shou, #25
        ElementsData.UILevelHUD.hand,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,  # todo 收复失地  8/10
        ElementsData.UILevelHUD.hand,
        ElementsData.UIBattleEmbattle.quick_formation,
        ElementsData.UIBattleEmbattle.start_battle, #30
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,  # todo 武将升级 ✅
        ElementsData.UIHeroList.hand,
        ElementsData.UIHeroInfo.level_up, #35
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("================第五章开始======================")
    print("====click_a_until_b_appear_list：chapter_five_perform_list====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)

    perform_list_0 = [
        ElementsData.UIHeroInfo.rank_up,
        ElementsData.UIHeroRankUp.level_up,# todo 升星
        ElementsData.UIResGetMoreItem.close,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_0====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_0, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroRankUp.close)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroInfo.btn_back)

    perform_list_1=[
        ElementsData.UIHeroList.guan,
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)

    perform_list_2 = [
        ElementsData.UIHeroInfo.rank_up,
        ElementsData.UIHeroRankUp.level_up,# todo 升星
        ElementsData.UIResGetMoreItem.close,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroRankUp.close)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroInfo.btn_back)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroList.closeBtn)

    perform_list_3 = [

        ElementsData.UILevelHUD.xin_shou, #1
        ElementsData.UILevelHUD.hand,
        ElementsData.UIReward.lab_continue,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand, #5
        ElementsData.UIBattleEmbattle.quick_formation,
        ElementsData.UIBattleEmbattle.start_battle,
        ElementsData.UIBattleResultWin.lab_close,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIReward.lab_continue,#10
        ElementsData.UIStoryDrawing.drawing_root,

        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDrawing.lab_continue_2,
        ElementsData.UIStoryDialogue.choice2,
        ElementsData.UIStoryDialogue.lab_continue, #15
        ElementsData.UIStoryGuide.hand,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIFunctionUnlock.lab_press_any,
        ElementsData.UILevelHUD.hand,  # todo 讨伐
        ElementsData.UIStoryDialogue.lab_continue, #20
        ElementsData.UIChapterLevel.challenge,
        ElementsData.UIBattleEmbattle.start_battle, #1-1
        ElementsData.UIBattleResultWin.lab_next,    # todo 下一关*4
        ElementsData.UIBattleEmbattle.start_battle, #1-2
        ElementsData.UIBattleResultWin.lab_next,  #25
        ElementsData.UIBattleEmbattle.start_battle,  #1-3
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  #1-4
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  #1-5  #30
        ElementsData.UIRecruitNewHero.lab_tips,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_3====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIRecruitNewHero.lab_tips)
    await bp.click_until_disappear(element_data=ElementsData.UIBattleResultWin.lab_next)
    await bp.click_element_safe(element_data=ElementsData.UIBattleEmbattle.quick_formation)
    await bp.click_until_disappear(element_data=ElementsData.UIBattleEmbattle.start_battle) #1-6
    await bp.click_until_disappear(element_data=ElementsData.UIBattleResultWin.lab_next)




    perform_list_4 = [
        ElementsData.UIBattleEmbattle.hero,
        ElementsData.UIHeroList.guan,
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIStoryDialogue.lab_continue,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_4====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_4, interval=0.5)


    await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)
    await bp.sleep(2)

    await bp.click_element_safe(element_data=ElementsData.UIResGetMoreItem.tao_fa)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UIChapterLevel.close)
    await bp.sleep(2)

    perform_list_5 = [
        ElementsData.UILevelHUD.hero,
        ElementsData.UIHeroList.ma,
        ElementsData.UIHeroInfo.level_up,
        ElementsData.UIResGetMoreItem.close_2,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_5====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_5, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroInfo.btn_back)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroList.closeBtn)

    perform_list_6=[
        ElementsData.UILevelHUD.tao_fa,
        ElementsData.UIChapterLevel.challenge,
        ElementsData.UIBattleEmbattle.start_battle,  #1-7
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle, #1-8
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle, #1-9
        ElementsData.UIBattleResultWin.win_close,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_6====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_6, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIBattleResultWin.win_close)

    await bag_operation(bp)


    perform_list_10 = [
        ElementsData.UILevelHUD.xin_shou, #1
        ElementsData.UIBuildingConstruct.build,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.xin_shou,      # 铁矿升级2
        ElementsData.UIBuilding.upgradeBtn, #5
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,  # 铁矿升级3
        ElementsData.UIBuilding.upgradeBtn, #10
        ElementsData.UIBuilding.btn_splash,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_10====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_10, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    perform_list_11 = [
        ElementsData.UIBuilding.upgradeBtn,# 铁矿升级4
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_11====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_11, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    perform_list_12 = [
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_12====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_12, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UIBuilding.task_effect)

    perform_list_13 = [
        ElementsData.UILevelHUD.xin_shou, #民居丁
        ElementsData.UIBuildingConstruct.build,
        ElementsData.UILevelHUD.xin_shou, #厨房4
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash, #5
        ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_13====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_13, interval=0.2)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    perform_list_14 = [
        ElementsData.UIBuilding.upgradeBtn, #厨房5
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_14====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_14, interval=0.2)
    await bp.click_element_safe(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UICommonPopup2.tog_check)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UICommonPopup2.confirm)


    perform_list_15 = [
        ElementsData.UICommonPopup2.confirm,
        ElementsData.UIBuilding.task_effect,
        ElementsData.UILevelHUD.xin_shou, #煤矿4
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_15====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_15, interval=0.2)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    perform_list_16 = [
        ElementsData.UIBuilding.upgradeBtn, #煤矿5
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_16====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_16, interval=0.2)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UIBuilding.task_effect)

    perform_list_17 = [
        ElementsData.UILevelHUD.xin_shou, #火炉 #1
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
        ElementsData.UIBuilding.task_effect,

        ElementsData.UIChapterChangeTime.tap_close,#5
        ElementsData.UIBuildingUnlock.lab_continue,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue, #10
    ]
    print("====click_a_until_b_appear_list：chapter_five_perform_list_17====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_17, interval=0.5)
    print("================第五章结束======================")



async def chapter_six(bp: BasePage):
    """第六章"""
    perform_list_0 = [
        ElementsData.UIStoryDialogue.lab_continue,  # 1
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue, #5
        ElementsData.UISupportManagement.hand,
        ElementsData.UIBuildingConstruct.build,
        ElementsData.UIStoryDialogue.lab_continue,
        ]
    print("================第六章开始======================")
    print("====click_a_until_b_appear_list：chapter_six_perform_list_0====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_0, interval=0.2)
    await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)


    perform_list_1 = [
        ElementsData.UIStoryGuide.hand,
        ElementsData.UISlgBuildingOperationPanel.train,
        ElementsData.UiBarracks.train,
        ElementsData.UiBarracks.acc,

    ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.2)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)
    await bp.sleep(2)


    perform_list_2 = [
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UILevelHUD.hand, #领取士兵

        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UIBuildingConstruct.build,  #城墙

        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,
        ElementsData.UISlgBuildingOperationPanel.upgrade, #升级城墙
        ElementsData.UISlgBuildingUpgrade.upgrade_lab,
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.hand,
        ElementsData.UIReward.lab_continue,
        ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.2)
    await  bp.sleep(1)
    await bp.click_until_disappear(element_data=ElementsData.UIReward.lab_continue)
    await bp.sleep(1)
    await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)
    await bp.sleep(1)

    perform_list_3 = [
        ElementsData.UIStoryGuide.hand_2, #1
        ElementsData.UiInsurgentsEnemyTips.attack,
        ElementsData.UIGoBattle.hand,
        ElementsData.UIGoBattleSelectHero.select_hero,
        ElementsData.UIGoBattle.hand, #5
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.choice2,


        ElementsData.UILevelHUD.task_desc,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.ling_qu, #10
        ElementsData.UIBuilding.upgradeBtn,  #铁矿
        ElementsData.UIBuilding.btn_splash,
   ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_3====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)
    await bp.sleep(1)

    perform_list_4 = [
        ElementsData.UILevelHUD.xin_shou,
        ElementsData.UILevelHUD.hand,
        ElementsData.UISupportManagement.ling_qu,
        ElementsData.UIBuilding.upgradeBtn,#猎人小屋
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_4====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_4, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)

    perform_list_5 = [
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
    ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_5====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_5, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(2)
    await bp.click_until_disappear(ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)
    if await bp.exist(element_data=ElementsData.UIBuilding.task_effect):
        await bp.click_until_disappear(element_data=ElementsData.UIBuilding.task_effect)
        await bp.sleep(1)
    else:
        await bp.click_until_disappear(element_data=ElementsData.UILevelHUD.mx_up)
        await bp.sleep(1)
        await bp.click_until_disappear(element_data=ElementsData.UISupportPromote.UISupportPromote)
        await bp.sleep(1)


    perform_list_6 = [
        ElementsData.UILevelHUD.xin_shou,          #商行
        ElementsData.UIBuildingConstruct.build,
        ElementsData.UILevelHUD.xin_shou,
    ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_6====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_6, interval=0.2)

    await bp.click_until_disappear(element_data=ElementsData.UILevelHUD.xin_shou)

    await hero_upgrade(bp, 3)
    await bp.sleep(2)
    await hero_upgrade(bp, 3)


    perform_list_7 = [
        ElementsData.UILevelHUD.xin_shou, #1
        ElementsData.UIChapterLevel.challenge,
        ElementsData.UIBattleEmbattle.start_battle, #1-10
        ElementsData.UIBattleResultWin.win_close,
        ElementsData.UILevelHUD.xin_shou, #5
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue,
        ]
    print("====click_a_until_b_appear_list：chapter_six_perform_list_7====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_7, interval=0.2)
    print("================第六章结束======================")



async def chapter_seven(bp: BasePage):

    perform_list_1 = [
        ElementsData.UIStoryDialogue.lab_continue,  # 1
        ElementsData.UIStoryDialogue.choice1,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UiMission.close,
        ElementsData.UILevelHUD.xin_shou,  #火炉 #5
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
    ]
    print("================第七章开始======================")
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
    await bp.sleep(2)
    await bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(2)
    if await bp.exist(ElementsData.UIBuilding.task_effect):
        await bp.click_until_disappear(element_data=ElementsData.UIBuilding.task_effect)
    else:
        await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)
        await bp.click_until_disappear(element_data=ElementsData.UILevelHUD.task_effect)
    await bp.sleep(2)

    perform_list_2 = [
        ElementsData.UIBuildingUnlock.lab_continue, #1
        ElementsData.UIFunctionUnlock.lab_press_any,

        ElementsData.UIStoryDialogue.lab_continue_2,
        ElementsData.UILevelHUD.hand,
        ElementsData.UIStoryDialogue.lab_continue_2, #5
        ElementsData.UIWatchTower.hand,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_2====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIWatchTower.hand)  #第一次烽火台
    await bp.sleep(2)
    if await bp.exist(ElementsData.UIMapInteractionTipsEnemy.attack):
        await bp.click_element_safe(element_data=ElementsData.UIMapInteractionTipsEnemy.attack)
        await bp.sleep(2)
        await bp.click_element_safe(element_data=ElementsData.UIGoBattle.go)
    elif await bp.exist(ElementsData.UIMapInteractionTipsRescue.rescue):
        await bp.click_until_disappear(element_data=ElementsData.UIMapInteractionTipsRescue.rescue)
    await bp.sleep(2)

    perform_list_3 = [
        ElementsData.UILevelHUD.hand,
        ElementsData.UIWatchTower.hand,
        ElementsData.UIReward.lab_continue,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_3====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIReward.lab_continue)
    await bp.sleep(2)
    if await bp.exist(ElementsData.UIWatchTower.hand):
        await bp.click_until_disappear(element_data=ElementsData.UIWatchTower.hand)#第二次
    else:
        await bp.click_object_of_plural_objects(ElementsData.UIWatchTower.task)
        await bp.sleep(1)
        await bp.click_object_of_plural_objects(ElementsData.UIWatchTower.go)
    await bp.sleep(2)

    if await bp.exist(ElementsData.UIMapInteractionTipsEnemy.attack):
        await bp.click_element_safe(element_data=ElementsData.UIMapInteractionTipsEnemy.attack)
        print(1)
        await bp.sleep(2)
        await bp.click_element_safe(element_data=ElementsData.UIGoBattle.go)
        await bp.sleep(2)
        print(2)
        if await bp.exist(ElementsData.UIGoBattleSelectHero.save):
            await bp.click_element_safe(element_data=ElementsData.UIGoBattleSelectHero.save)
            await bp.click_element_safe(element_data=ElementsData.UIGoBattle.go)
        else:
            pass
    elif await bp.exist(ElementsData.UIMapInteractionTipsRescue.rescue):
        await bp.click_until_disappear(element_data=ElementsData.UIMapInteractionTipsRescue.rescue)
    await bp.sleep(2)


    perform_list_4 = [
        ElementsData.UILevelHUD.feng_huo,
        ElementsData.UIWatchTower.dui,
        ElementsData.UIReward.lab_continue,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_4====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_4, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIReward.lab_continue)
    await bp.click_until_disappear(element_data=ElementsData.UiWatchtowerUpdate.close)
    await bp.sleep(5)


    await bp.click_object_of_plural_objects(ElementsData.UIWatchTower.task)
    await bp.sleep(2)
    await bp.click_object_of_plural_objects(ElementsData.UIWatchTower.go)

    await bp.sleep(2)
    if await bp.exist(ElementsData.UIMapInteractionTipsEnemy.attack):
        await bp.click_element_safe(element_data=ElementsData.UIMapInteractionTipsEnemy.attack)
        print(1)
        await bp.sleep(2)
        await bp.click_element_safe(element_data=ElementsData.UIGoBattle.go)
        await bp.sleep(2)
        print(2)
        if await bp.exist(ElementsData.UIGoBattleSelectHero.save):
            await bp.click_element_safe(element_data=ElementsData.UIGoBattleSelectHero.save)
            await bp.click_element_safe(element_data=ElementsData.UIGoBattle.go)
        else:
            pass
    elif await bp.exist(ElementsData.UIMapInteractionTipsRescue.rescue):
        await bp.click_until_disappear(element_data=ElementsData.UIMapInteractionTipsRescue.rescue)
    await bp.sleep(2)

    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.feng_huo)
    await bp.sleep(10)
    await bp.click_object_of_plural_objects(ElementsData.UIWatchTower.dui_2)



    await bp.click_until_disappear(element_data=ElementsData.UIReward.lab_continue)

    await bp.click_element_safe(element_data=ElementsData.UIWatchTower.back)

    perform_list_5 = [
        ElementsData.UILevelHUD.hui_cheng,
        ElementsData.UILevelHUD.task_effect,
        ]

    print("====click_a_until_b_appear_list：chapter_seven_perform_list_5====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_5, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UILevelHUD.task_effect)

    perform_list=[
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UIBuildingConstruct.build,  # 弓兵营
        ElementsData.UILevelHUD.task_effect,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list, interval=0.5)


    perform_list_6 = [
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UISlgBuildingOperationPanel.train,  #训练弓兵
        ElementsData.UiBarracks.use_diamond,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_6====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_6, interval=0.5)
    await bp.click_element_safe(element_data=ElementsData.UiBarracks.use_diamond)
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)

    perform_list_7 = [
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UILevelHUD.search,
        ElementsData.UiMapSearch.map_search,
        ElementsData.UIMapInteractionTipsEnemy.attack,#流寇
        ElementsData.UIGoBattle.go,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_7====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_7, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIGoBattle.go)

    await bp.sleep(5)
        ##击败流寇
    await bp.click_element_safe(element_data=ElementsData.UILevelHUD.hui_cheng)
    await bp.wait_for_appear(element_data=ElementsData.UILevelHUD.task_effect)

    perform_list_8=[
        ElementsData.UILevelHUD.task_desc,#伐木场5
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_8====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_8, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(1)
    await  bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)

    perform_list_9 = [
        ElementsData.UIBuilding.upgradeBtn, #伐木场6
        ElementsData.UIBuilding.btn_splash,
    ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_9====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_9, interval=0.2)
    await bp.sleep(1)
    await bp.click_element_safe(element_data=ElementsData.UIBuilding.open_upgrade)
    await bp.sleep(1)
    await  bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
    await bp.sleep(1)
    if await bp.exist(ElementsData.UIBuilding.task_effect):
        await bp.click_element_safe(element_data=ElementsData.UIBuilding.task_effect)
    else:
        await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)
        await bp.sleep(1)

    await bp.click_a_until_b_appear(ElementsData.UILevelHUD.task_desc,ElementsData.UIBuildingConstruct.build)
    await bp.click_until_disappear(element_data=ElementsData.UIBuildingConstruct.build)#民居戊
    await bp.sleep(2)

    perform_list_10 = [
        ElementsData.UILevelHUD.task_desc,   #煤矿
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_10====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_10, interval=0.2)
    await bp.click_element_safe(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)

    perform_list_11 = [
        ElementsData.UIBuilding.upgradeBtn,
        ElementsData.UIBuilding.btn_splash,
        ElementsData.UIBuilding.open_upgrade,
        ElementsData.UISlgBuildingUpgrade.use_diamond,
        ElementsData.UIBuilding.task_effect,
    ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_11====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_11, interval=0.2)
    if await bp.exist(ElementsData.UIBuilding.task_effect):
        await bp.click_element_safe(element_data=ElementsData.UIBuilding.task_effect)
    else:
        await bp.click_element_safe(element_data=ElementsData.UILevelHUD.utc_time)
        await bp.sleep(1)



    await hero_upgrade(bp, 3)
    perform_list_11_1 = [
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UIChapterLevel.reward,  #领华雄
        ElementsData.UIRecruitNewHero.lab_tips,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_11_1====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_11_1, interval=0.2)
    await bp.click_until_disappear(element_data=ElementsData.UIRecruitNewHero.lab_tips)


    perform_list_12 = [
        ElementsData.UIReward.lab_continue,
        ElementsData.UIChapterLevel.next_chapter,
        ElementsData.UIChapterLevel.challenge,
        ElementsData.UIBattleEmbattle.quick_formation,
        ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_12====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_12, interval=0.2)
    await bp.sleep(2)
    await bp.click_element_safe(element_data=ElementsData.UIBattleEmbattle.quick_formation)


    perform_list_13=[
        ElementsData.UIBattleEmbattle.start_battle,  # 2-1   #1
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-2
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-3  #5
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-4
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-5
        ElementsData.UIBattleResultWin.lab_next,    #10
        ElementsData.UIBattleEmbattle.start_battle,  # 2-6
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-7
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-8  #15
        ElementsData.UIBattleResultWin.win_close,

    ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_13====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_13, interval=0.5)
    await bp.click_until_disappear(element_data=ElementsData.UIBattleResultWin.win_close)


    await zhaomu_operation(bp)
    await bp.sleep(1)
    if await bp.exist(element_data=ElementsData.UiGiftPop.close):
        await bp.click_until_disappear(element_data=ElementsData.UiGiftPop.close)
    await bp.sleep(1)
    await hero_upgrade(bp, 4)



    perform_list_14 = [
        ElementsData.UILevelHUD.task_desc,
        ElementsData.UIChapterLevel.challenge,
        ElementsData.UIBattleEmbattle.quick_formation,
    ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_14====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_14, interval=0.5)
    await bp.click_element_safe(element_data=ElementsData.UIBattleEmbattle.quick_formation)
    await bp.sleep(2)

    perform_list_15=[
        ElementsData.UIBattleEmbattle.start_battle,  # 2-9
        ElementsData.UIBattleResultWin.lab_next,
        ElementsData.UIBattleEmbattle.start_battle,  # 2-10
        ElementsData.UIBattleResultWin.win_close,
        ElementsData.UILevelHUD.task_effect,
        ElementsData.UiMission.btn_claim,
        ElementsData.UIReward.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue,
    ]
    print("====click_a_until_b_appear_list：chapter_seven_perform_list_15====")
    await bp.click_a_until_b_appear_list(perform_list=perform_list_15, interval=0.5)
    print("================第七章结束======================")


# async def chapter_eight(bp: BasePage):
#     perform_list_1 = [
#         ElementsData.UIStoryDialogue.lab_continue,
#         ElementsData.UIStoryDialogue.choice1,
#         ElementsData.UIStoryDialogue.lab_continue,
#     ]
#     print("================第八章开始======================")
#     print("====click_a_until_b_appear_list：perform_list_1====")
#     await bp.click_a_until_b_appear_list(perform_list=perform_list_1, interval=0.5)
#     await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)
#     await bp.click_element_safe(element_data=ElementsData.UILevelHUD.hui_cheng)
#     await bp.sleep(2)
#     await bag_operation(bp)
#     await bp.sleep(2)
#     perform_list_2 = [
#         ElementsData.UILevelHUD.task_desc,
#         ElementsData.UIBuilding.open_upgrade,
#         ElementsData.UISlgBuildingUpgrade.goto,
#         ElementsData.UISlgBuildingOperationPanel.upgrade,
#         #ElementsData.UISlgBuildingUpgrade.use_diamond,
#     ]
#     print("====click_a_until_b_appear_list：perform_list_2====")
#     await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
#     await bp.sleep(2)
#     await bp.click_until_disappear(element_data=ElementsData.UISlgBuildingOperationPanel.upgrade)
#
#     await bp.sleep(2)
#
#     for _ in range (6):
#         if await bp.exist(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond):
#             await bp.click_element_safe(element_data=ElementsData.UISlgBuildingUpgrade.use_diamond)
#         elif await bp.exist(element_data=ElementsData.UISlgBuildingUpgrade.free):
#             await bp.click_element_safe(element_data=ElementsData.UISlgBuildingUpgrade.free)
#         await bp.sleep(1)
#     await bp.click_until_disappear(element_data=ElementsData.UISlgBuildingUpgrade.close)
#
#     perform_list_3 = [
#         ElementsData.UILevelHUD.task_desc,
#         ElementsData.UIBuilding.open_upgrade,
#         ElementsData.UISlgBuildingUpgrade.use_diamond,
#         ElementsData.UIBuilding.task_effect,
#         ElementsData.UIBuildingUnlock.lab_continue,
#     ]
#     print("====click_a_until_b_appear_list：perform_list_3====")
#     await bp.click_a_until_b_appear_list(perform_list=perform_list_3, interval=0.5)
#     await bp.click_until_disappear(element_data=ElementsData.UIBuildingUnlock.lab_continue)




async def bag_operation(bp: BasePage):

    # 打开背包
    print("====bag_operation====")
    await bp.click_a_until_b_appear(ElementsData.UILevelHUD.bag, ElementsData.UIBag.back)
    await bp.sleep(5)

    q=await bp.get_position_list(element_data=ElementsData.UIBag.item)
    l=len(q)
    print("背包可使用物品数量：",l)

    # 点击物品
    while l>0:
        await bp.click_element_safe(element_data=ElementsData.UIBag.wood)
        await bp.sleep(3)
        try:
            text = await bp.get_text(element_data=ElementsData.UIBagPopup.num)
            print("当前点击物品数量:",text)
            count = int(text)
        except Exception as e:
            print(f"读取物品数量失败: {e}")
            continue
        # 然后点击 count 次
        if await bp.exist(element_data=ElementsData.UIBagPopup.add):
            print("click_element_safe",count,"次:{'locator': 'ui_layer/view/UIBagPopup/UIBagPopup/Layout/_group_handle/_but_add:but/Sprite', 'focus': (0.5, 0.5)}")
            for _ in range(count):
                await bp.click_element_safe(element_data=ElementsData.UIBagPopup.add,log=False)
            await bp.click_until_disappear(element_data=ElementsData.UIBagPopup.use)
            l -= 1
        else:
            continue


        if await bp.exist(element_data=ElementsData.UICommonPopup2.tog_check):
            await bp.click_element_safe(element_data=ElementsData.UICommonPopup2.tog_check)
            await bp.sleep(2)
            await bp.click_until_disappear(element_data=ElementsData.UICommonPopup2.confirm)

    await bp.click_element_safe(element_data=ElementsData.UIBag.back)


async def hero_upgrade(bp: BasePage, num):
    dict_hero = {
        "cai_wen_ji": ElementsData.UIHeroList.cai,
        "guan_yin_ping": ElementsData.UIHeroList.guan,
        "ma_su": ElementsData.UIHeroList.ma,
        "hua_xiong": ElementsData.UIHeroList.hua,
    }
    print("====hero_upgrade====")
    await bp.click_a_until_b_appear(ElementsData.UILevelHUD.hero, ElementsData.UIHeroList.closeBtn)


    for hero_name, hero_element in list(dict_hero.items())[:num]:
        await bp.click_a_until_b_appear(hero_element, ElementsData.UIHeroInfo.rank_up)
        await bp.sleep(2)
        print("==",hero_name,"升级==")
        # === 点击升级，直到出现 close_2 或 upgrade_condition 为止 ===
        while True:
            if await bp.exist(element_data=ElementsData.UIResGetMoreItem.close_2):
                print("检测到 close_2")
                break
            if await bp.exist(element_data=ElementsData.UIHeroInfo.upgrade_condition):
                print("检测到 upgrade_condition元素")
                break
            await bp.click_element_safe(element_data=ElementsData.UIHeroInfo.level_up)
            await bp.sleep(0.5)

        await bp.sleep(2)

        # === 如果出现 close_2，检查是否有剧情 ===
        if await bp.exist(element_data=ElementsData.UIResGetMoreItem.close_2):
            if await bp.exist(element_data=ElementsData.UIStoryDialogue.lab_continue):
                await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)
                await bp.sleep(2)
                await bp.click_element_safe(element_data=ElementsData.UIResGetMoreItem.tao_fa)
                await bp.sleep(2)
                await bp.click_until_disappear(element_data=ElementsData.UIChapterLevel.close)
                return
            else:
                await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close_2)

        # === 升星 ===
        print("==",hero_name,"升星==")
        perform_list_2 = [
            ElementsData.UIHeroInfo.rank_up,
            ElementsData.UIHeroRankUp.level_up,
            ElementsData.UIResGetMoreItem.close,
        ]
        await bp.click_a_until_b_appear_list(perform_list=perform_list_2, interval=0.5)
        await bp.sleep(2)

        if await bp.exist(element_data=ElementsData.UIResGetMoreItem.close):
            if await bp.exist(element_data=ElementsData.UIStoryDialogue.lab_continue):
                await bp.click_until_disappear(element_data=ElementsData.UIStoryDialogue.lab_continue)

                await bp.sleep(2)
                await bp.click_element_safe(element_data=ElementsData.UIResGetMoreItem.tao_fa2)

                await bp.sleep(2)
                await bp.click_until_disappear(element_data=ElementsData.UIChapterLevel.close)
                return
            else:
                await bp.click_until_disappear(element_data=ElementsData.UIResGetMoreItem.close)

        # 返回上层界面
        await bp.click_until_disappear(element_data=ElementsData.UIHeroRankUp.close)
        await bp.click_until_disappear(element_data=ElementsData.UIHeroInfo.btn_back)

    await bp.click_until_disappear(element_data=ElementsData.UIHeroList.closeBtn)


async def zhaomu_operation(bp: BasePage):
    print("====zhaomu_operation====")
    await bp.click_a_until_b_appear(ElementsData.UILevelHUD.hero, ElementsData.UIHeroList.closeBtn)
    await bp.sleep(2)
    await bp.click_a_until_b_appear(ElementsData.UIHeroList.chou_ka, ElementsData.UIRecruit.basic_num)
    await bp.sleep(2)
    basic=await bp.get_text(element_data=ElementsData.UIRecruit.basic_num)
    print("普通招募数量：",basic)
    advance=await bp.get_text(element_data=ElementsData.UIRecruit.advance_num)
    print("高级招募数量：",advance)

    try:
        basic = int(basic)
        advance = int(advance)
    except ValueError:
        print("招募次数格式错误，无法转换为整数")
        return

    # 普通招募
    if basic >= 10:
        ten_count = basic // 10
        one_count = basic % 10

        for _ in range(ten_count):
            print(f"正在执行第 {_ + 1} 次 basics_ten 点击")
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.basics_ten)
            await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)
            await bp.sleep(1)

        if one_count>=1:
            print(f"正在执行第 1 次 basics_once 点击")
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.basics_once)
            await bp.sleep(8)

            for i in range(one_count-1):
                print(f"正在执行第 {i + 1} 次 again 点击")
                await bp.click_element_safe(element_data=ElementsData.UIRecruit.again)
                if await bp.exist(element_data=ElementsData.UIRecruitNewHero.lab_tips):
                    await bp.click_element_safe(element_data=ElementsData.UIRecruitNewHero.lab_tips)
                await bp.sleep(1)

            await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)

    elif basic > 0:
        print(f"正在执行第 1 次 basics_once 点击")
        await bp.click_element_safe(element_data=ElementsData.UIRecruit.basics_once)
        await bp.sleep(8)
        for _ in range(basic-1):
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.again)
            if await bp.exist(element_data=ElementsData.UIRecruitNewHero.lab_tips):
                await bp.click_element_safe(element_data=ElementsData.UIRecruitNewHero.lab_tips)
            await bp.sleep(1)

        await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)

    # 高级招募
    if advance >= 10:
        ten_count = advance // 10
        one_count = advance % 10

        for _ in range(ten_count):
            print(f"正在执行第 {_ + 1} 次 advanced_ten 点击")
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.advanced_ten)
            await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)
            await bp.sleep(2)

        if one_count>=1:
            print(f"正在执行第 1 次 advanced_once 点击")
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.advanced_once)
            await bp.sleep(8)

            for i in range(one_count-1):
                print(f"正在执行第 {i + 1} 次 again 点击")
                await bp.click_element_safe(element_data=ElementsData.UIRecruit.again)
                if await bp.exist(element_data=ElementsData.UIRecruitNewHero.lab_tips):
                    await bp.click_element_safe(element_data=ElementsData.UIRecruitNewHero.lab_tips)
                await bp.sleep(2)

            await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)

    elif advance > 0:
        print(f"正在执行第 1 次 advanced_once 点击")
        await bp.click_element_safe(element_data=ElementsData.UIRecruit.advanced_once)
        await bp.sleep(8)
        for i in range(advance-1):
            print(f"正在执行第 {i + 1} 次 again 点击")
            await bp.click_element_safe(element_data=ElementsData.UIRecruit.again)
            if await bp.exist(element_data=ElementsData.UIRecruitNewHero.lab_tips):
                await bp.click_element_safe(element_data=ElementsData.UIRecruitNewHero.lab_tips)
            await bp.sleep(2)
        await bp.click_until_disappear(element_data=ElementsData.UIRecruitResult.lab_continue)

    await bp.click_until_disappear(element_data=ElementsData.UIRecruit.return_btn)
    await bp.click_until_disappear(element_data=ElementsData.UIHeroList.closeBtn)



# async def run_on_device(server,device_type,device_id):
#
#     os.makedirs("logs", exist_ok=True)
#     log_file = f"logs/run_{device_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
#     sys.stdout = LoggerWriter(log_file)
#
#     #bp = BasePage(server=server, is_mobile_device=True, is_ios=False, device_id=device_id)
#     bp = BasePage(
#         server=server,
#         is_mobile_device=(device_type == "android"),
#         is_ios=(device_type == "ios"),
#         device_id=device_id
#     )
#     try:
#         await bp.custom_command("setCamera ui_layer/UICamera")
#         await chapter_one(bp)
#         await chapter_two(bp)
#         await chapter_three(bp)
#         await chapter_four(bp)
#         await chapter_five(bp)
#         await chapter_six(bp)
#         await chapter_seven(bp)
#
#         print(f"[{device_id}] =================所有章节结束，脚本运行成功================")
#         send_dingding(log_file)
#         return True
#
#     except asyncio.TimeoutError:
#         print(f"[{device_id}] 超时异常，任务失败。")
#         send_dingding_error(log_file)
#         return False
#     except Exception as e:
#         print(f"[{device_id}] 未知异常: {e}")
#         send_dingding_error(log_file)
#         return False
#     finally:
#         bp.connect_close()



# @rpc_server(port=5101)
# async def main(server):
#     # 输入设备类型
#     # device_category="android"  #android,ios,pc
#     #
#     # android_ids = BasePage.list_android_devices()
#     # ios_ids = BasePage.list_ios_devices()
#     #
#     #
#     # tasks = []
#     # if device_category == "android":
#     #     for did in android_ids:
#     #         print(f"开始执行 Android 设备 {did}")
#     #         tasks.append(run_on_device(server, "android", did))
#     # elif device_category == "ios":
#     #     for did in ios_ids:
#     #         tasks.append(run_on_device(server, "ios", did))
#     # elif device_category == "pc":
#     #     tasks.append(run_on_device(server, "pc", None))
#     # else:
#     #     print("设备类型错误，请检查输入的设备类型")
#     #
#     #
#     # if not tasks:
#     #     print("没有检测到任何设备")
#     #     return
#     #
#     # results = await asyncio.gather(*tasks)
#     # print("所有设备执行完成:", results)
#     #
#     os.makedirs("logs", exist_ok=True)
#     log_file = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
#     sys.stdout = LoggerWriter(log_file)

#     bp = BasePage(server=server, is_mobile_device=True, is_ios=False,device_id="172.16.37.189:5555")
#     try:
#         await bp.custom_command("setCamera ui_layer/UICamera")

#         await chapter_one(bp)
#         await chapter_two(bp)
#         await chapter_three(bp)
#         await chapter_four(bp)
#         await chapter_five(bp)
#         await chapter_six(bp)
#         await chapter_seven(bp)

#         print("=================所有章节结束，脚本运行成功================")
#         send_dingding(log_file)
#     except asyncio.TimeoutError:
#         send_dingding_error(log_file)
#         print("超时异常，任务失败。")
#     except Exception as e:
#         print(f"未知异常: {e}")
#         send_dingding_error(log_file)

#     finally:
#         bp.connect_close()

# if __name__ == "__main__":
#     main()

# ...existing code...
from datetime import datetime
# ...existing code...

def get_chapter_limit():
    """获取章节限制，优先使用命令行参数，否则要求用户输入"""
    parser = argparse.ArgumentParser(description='Cocos UI自动化测试脚本')
    parser.add_argument('--max-chapter', type=int, choices=range(1, 8), 
                       help='测试到第几章 (1-7)')
    parser.add_argument('--device-id', type=str, 
                       help='设备ID')
    parser.add_argument('--mobile', action='store_true',
                       help='是否为移动设备测试')
    parser.add_argument('--device-type', type=str, choices=['android', 'ios'],
                       help='设备类型 (android/ios)')
    
    # 解析命令行参数
    args, unknown = parser.parse_known_args()
    
    # 如果提供了命令行参数，直接使用
    if args.max_chapter is not None:
        print(f"📋 使用命令行参数: 测试到第{args.max_chapter}章")
        if args.device_id:
            print(f"📱 使用设备ID: {args.device_id}")
        if args.mobile:
            print(f"📱 移动设备测试模式")
        if args.device_type:
            print(f"📱 设备类型: {args.device_type}")
        return args.max_chapter, args.device_id, args.mobile, args.device_type
    
    # 否则要求用户输入
    while True:
        user_input = input("请输入测试到第几章 (1-7，直接回车测试所有章节): ").strip()
        
        if not user_input:
            return 7, None, False, None
        
        try:
            chapter_num = int(user_input)
            if 1 <= chapter_num <= 7:
                return chapter_num, None, False, None
            else:
                print("❌ 请输入1-7之间的数字")
        except ValueError:
            print("❌ 请输入有效数字")

async def run_chapters_up_to(bp: BasePage, max_chapter):
    """执行到指定章节"""
    chapter_functions = {
        1: chapter_one,
        2: chapter_two, 
        3: chapter_three,
        4: chapter_four,
        5: chapter_five,
        6: chapter_six,
        7: chapter_seven
    }
    
    for chapter_num in range(1, max_chapter + 1):
        if chapter_num in chapter_functions:
            print(f"================第{chapter_num}章开始======================")
            start_time = datetime.now()  # 记录开始时间
            await chapter_functions[chapter_num](bp)
            print(f"================第{chapter_num}章结束======================")
            end_time = datetime.now()  # 记录结束时间
            duration = end_time - start_time
            print(f"第{chapter_num}章开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"第{chapter_num}章结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"第{chapter_num}章总耗时: {str(duration)}")

@rpc_server()
async def main(server):
    # 显示端口配置信息
    print(get_port_info())
    
    # 获取用户输入
    max_chapter, device_id, is_mobile_device, device_type = get_chapter_limit()
    
    # 根据设备类型确定is_ios参数
    is_ios = device_type == "ios" if device_type else False
    
    # 显示测试信息
    if max_chapter == 7:
        print("🎮 开始测试所有章节 (第1-7章)")
    else:
        print(f"🎮 开始测试第1-{max_chapter}章")
    
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    sys.stdout = LoggerWriter(log_file)

    start_time = datetime.now()  # 记录开始时间

    bp = BasePage(server=server, is_mobile_device=is_mobile_device, is_ios=is_ios, device_id=device_id)
    try:
        await bp.custom_command("setCamera ui_layer/UICamera")

        # 执行到指定章节
        await run_chapters_up_to(bp, max_chapter)

        print("=================测试完成================")  # 添加这行来触发报告生成
        send_dingding(log_file)
    except asyncio.TimeoutError:
        send_dingding_error(log_file)
        print("超时异常，任务失败。")
    except Exception as e:
        print(f"未知异常: {e}")
        send_dingding_error(log_file)

    finally:
        bp.connect_close()
        end_time = datetime.now()  # 记录结束时间
        duration = end_time - start_time
        print(f"脚本开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"脚本结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总耗时: {str(duration)}")
        print("测试结束")  # 添加这行来触发报告生成

if __name__ == "__main__":
    main()