#!/usr/bin/env python
# -*- coding: UTF-8 -*-


vobbranch = [ ["develop@\\TN710",1], [r"feat_tn703@\OnsPlatform",1], [r"develop@\TN715",1], \
        [r"feat_v13@\TN715",1], ["main@\\OnsPlatform",1], \
        ["10G_CHT_06MAR30_BR@\\NetRing",1], ["feat_KT_220X@\\NetRing",1], ["10G_SbbV2217@\\NetRing",1], \
        ["feature@\NetRing",1], \
        ["NR40K_V1_20070709@\NetRing",1], ["TN7xx_Universe_Unification_Base@\OnsPlatform",1], \
        ["NR600V1_BaseV23117@\NetRing",1],  ["NR2G5_XC_BOARD@\NetRing",1], ["2500_Distributed_Final@\NetRing",1],\
        ["NR40K_V1_20090204@\NetRing",1],  ["NR10K_BaseV2319SP2@\NetRing",1],  \
        ["TN705_V1.3.2.14_branch@\OnsPlatform",1],["TN7X5_SBB_V1.2.0_Dev@\OnsPlatform",1]], \
        ["sbb_V1.3.2.18_base@\OnsPlatform",1], \
        ["TN705_V1.5.0.6_maintain@\OnsPlatform",1], \
		["TN765_R1.1_maintenance@\OnsPlatform",1],\
        ["TN7xx_V2.2.2.4@\OnsPlatform",1], \
        ["TN7xx_V2.2.3.x@\OnsPlatform",1], \
        ["TN735_DEV1@\OnsPlatform",1],\
        ["TN735_DEV_MAINTAIN@\OnsPlatform",1],\
        ["TN735_CHT_MAINTAIN@\OnsPlatform",1],\
        ["TN735_CHT_MAINTIAN@\OnsPlatform",1],\
        ["TN735_V2.1.1_maintain@\OnsPlatform",1],\
        ["TN735_V2.1.2.8_maintain@\OnsPlatform",1],\
        ["ONS00029627_ctc21@\admin-pon-vob",1], ["ONS00038638@\admin-pon-vob",1], \
        ["iAN_B1205_R2.1.0_MAIN@\ian8k_b1200_adm",1]

approve_servers = {}
approve_servers[r"develop@\TN710"] = "hz_ons_rdsvr1"
approve_servers[r"feat_tn703@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"develop@\TN715"] = "hz_ons_rdsvr1"
approve_servers[r"feat_v13@\TN715"] = "hz_ons_rdsvr1"
approve_servers[r"10G_CHT_06MAR30_BR@\\NetRing"] = "hz_ons_rdsvr2"
approve_servers[r"feat_KT_220X@\\NetRing"] = "hz_ons_rdsvr2"
approve_servers[r"10G_SbbV2217@\\NetRing"] = "hz_ons_rdsvr2"
approve_servers[r"feature@\NetRing"] = "hz_rd_fjl"
#approve_servers[r"feature@\NetRing"] = "172.21.146.4"   
approve_servers[r"NR600V1_BaseV23117@\NetRing"] = "hz_rd_fjl"
approve_servers[r"NR40K_V1_20090204@\NetRing"] = "hz_rd_fjl"
approve_servers[r"NR2G5_XC_BOARD@\NetRing"] = "hz_rd_fjl"
approve_servers[r"2500_Distributed_Final@\NetRing"] = "hz_rd_fjl"
approve_servers[r"NR10K_BaseV2319SP2@\NetRing"] = "hz_rd_fjl"
approve_servers[r"main@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"NR40K_V1_20070709@\NetRing"] = "hz_rd_build3"
approve_servers[r"TN7xx_Universe_Unification_Base@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN7xx_V2.2.2.4@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN7xx_V2.2.3.x@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN705_V1.3.2.14_branch@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN705_V1.5.0.6_maintain@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN765_R1.1_maintenance@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"sbb_V1.3.2.18_base@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN7X5_SBB_V1.2.0_Dev@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN735_DEV1@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN735_DEV_MAINTAIN@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN735_CHT_MAINTIAN@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN735_V2.1.1_maintain@\OnsPlatform"] = "hz_rd_build3"
approve_servers[r"TN735_V2.1.2.8_maintain@\OnsPlatform"] = "hz_rd_build3"
#add by Wu Shuming 2011/10/18
approve_servers[r"ONS00029627_ctc21@\admin-pon-vob"] = "172.21.76.130"
approve_servers[r"ONS00038638@\admin-pon-vob"] = "172.21.76.130"
approve_servers[r"iAN_B1205_R2.1.0_MAIN@\ian8k_b1200_adm"] = "172.21.76.129"


branch_choices = (
        (r'NR40K_V1_20070709@\NetRing', r'NR40K_V1_20070709@\NetRing'),\
                #((r'develop@\TN710', r'develop@\TN710'), \
                #(r'feat_tn703@\OnsPlatform', r'feat_tn703@\OnsPlatform'),\
                #        (r'develop@\TN715', r'develop@\TN715'),\
                #        (r'feat_v13@\TN715', r'feat_v13@\TN715'),\
                #        (r'10G_CHT_06MAR30_BR@\NetRing', r'10G_CHT_06MAR30_BR@\NetRing'),\
                #        (r'feat_KT_220X@\NetRing', r'feat_KT_220X@\NetRing'),\
                #        (r'10G_SbbV2217@\NetRing', r'10G_SbbV2217@\NetRing'),\
                (r'feature@\NetRing', r'feature@\NetRing'),\
                (r'NR600V1_BaseV23117@\NetRing', r'NR600V1_BaseV23117@\NetRing'),\
                (r'NR40K_V1_20090204@\NetRing', r'NR40K_V1_20090204@\NetRing'),\
                (r'NR2G5_XC_BOARD@\NetRing', r'NR2G5_XC_BOARD@\NetRing'),\
                (r'2500_Distributed_Final@\NetRing', r'2500_Distributed_Final@\NetRing'),\
                (r'NR10K_BaseV2319SP2@\NetRing', r'NR10K_BaseV2319SP2@\NetRing'),\
                #(r'main@\OnsPlatform', r'main@\OnsPlatform'),\
                (r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform', r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform'),\
                (r'TN705_V1.3.2.14_branch@\OnsPlatform', r'TN705_V1.3.2.14_branch@\OnsPlatform'),\
                (r'TN705_V1.5.0.6_maintain@\OnsPlatform', r'TN705_V1.5.0.6_maintain@\OnsPlatform'),\
				(r'TN765_R1.1_maintenance@\OnsPlatform', r'TN765_R1.1_maintenance@\OnsPlatform'),\
                (r'sbb_V1.3.2.18_base@\OnsPlatform', r'sbb_V1.3.2.18_base@\OnsPlatform'),\
                (r'TN7xx_Universe_Unification_Base@\OnsPlatform', r'TN7xx_Universe_Unification_Base@\OnsPlatform'),\
                (r'TN7xx_V2.2.2.4@\OnsPlatform', r'TN7xx_V2.2.2.4@\OnsPlatform'),\
                (r'TN7xx_V2.2.3.x@\OnsPlatform', r'TN7xx_V2.2.3.x@\OnsPlatform'),\
                (r'TN735_DEV1@\OnsPlatform', r'TN735_DEV1@\OnsPlatform'),\
                (r'TN735_V2.1.1_maintain@\OnsPlatform', r'TN735_V2.1.1_maintain@\OnsPlatform'),\
                (r'TN735_V2.1.2.8_maintain@\OnsPlatform', r'TN735_V2.1.2.8_maintain@\OnsPlatform'),\
                #(r'TN735_DEV_MAINTAIN@\OnsPlatform', r'TN735_DEV_MAINTAIN@\OnsPlatform'),\
                #(r'TN735_CHT_MAINTIAN@\OnsPlatform', r'TN735_CHT_MAINTIAN@\OnsPlatform'),\
                #(r'ONS00029627_ctc21@\admin-pon-vob', r'ONS00029627_ctc21@\admin-pon-vob'),\
                #(r'ONS00038638@\admin-pon-vob', r'ONS00038638@\admin-pon-vob'),\
                #(r'iAN_B1205_R2.1.0_MAIN@\ian8k_b1200_adm', r'iAN_B1205_R2.1.0_MAIN@\ian8k_b1200_adm'),\
                (r'725E_dev@\OnsPlatform', r' 725E_dev@\OnsPlatform'),\
                (r'test', r'test'),\
                )#分支信息的choice

newfile_branch_choices = (
                ('','---------'),
                (r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform', r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform'),\
                (r'TN705_V1.3.2.14_branch@\OnsPlatform', r'TN705_V1.3.2.14_branch@\OnsPlatform'),\
                (r'TN705_V1.5.0.6_maintain@\OnsPlatform', r'TN705_V1.5.0.6_maintain@\OnsPlatform'),\
                (r'TN7xx_Universe_Unification_Base@\OnsPlatform', r'TN7xx_Universe_Unification_Base@\OnsPlatform'),\
                (r'TN7xx_V2.2.2.4@\OnsPlatform', r'TN7xx_V2.2.2.4@\OnsPlatform'),\
                (r'TN7xx_V2.2.3.x@\OnsPlatform', r'TN7xx_V2.2.3.x@\OnsPlatform'),\
                (r'TN735_DEV1@\OnsPlatform', r'TN735_DEV1@\OnsPlatform'),\
                (r'725E_dev@\OnsPlatform', r'725E_dev@\OnsPlatform'),
                (r'TN735_V2.1.1_maintain@\OnsPlatform', r'TN735_V2.1.1_maintain@\OnsPlatform'),\
                (r'TN735_V2.1.2.8_maintain@\OnsPlatform', r'TN735_V2.1.2.8_maintain@\OnsPlatform'),\
				(r'TN705_SBB_Private_svcoam@\OnsPlatform', r'TN705_SBB_Private_svcoam@\OnsPlatform'),\
				(r'725E_dev@\OnsPlatform', r'725E_dev@\OnsPlatform'),\
                )

reviewer1_choices = (('','---------'),
        (r'高永红', r'高永红'),\
        (r'卢玲玲', r'卢玲玲'),\
        (r'饶双宜', r'饶双宜'),\
        (r'施莹', r'施莹'),\
        (r'翁秀娟', r'翁秀娟'),\
        (r'赵玮芳', r'赵玮芳'),\
        (r'何玉斌', r'何玉斌'),\
        (r'陈玲萍', r'陈玲萍'),\
        (r'饶红霞', r'饶红霞'),\
        (r'冯绍聪', r'冯绍聪'),\
		(r'郑伟', r'郑伟'),
		(r'李彩云', r'李彩云'),
        )#QM的choice

reviewer2_choices = (('','---------'),
        (r'陈玲萍', r'陈玲萍'),\
        (r'程焱芳', r'程焱芳'),\
        (r'陈波', r'陈波'),\
        (r'陈骋', r'陈骋'),\
        (r'陈莹', r'陈莹'),\
        (r'陈官伟', r'陈官伟'),\
        (r'丁庆华', r'丁庆华'),\
        (r'范传林', r'范传林'),\
        (r'方樟钱', r'方樟钱'),\
        (r'冯佳良', r'冯佳良'),\
        (r'冯绍聪', r'冯绍聪'),\
        (r'高华能', r'高华能'),\
        (r'高永红', r'高永红'),\
        (r'葛海峰', r'葛海峰'),\
        (r'龚俊强', r'龚俊强'),\
        (r'顾雪敏', r'顾雪敏'),\
        (r'何玉斌', r'何玉斌'),\
        (r'侯明永', r'侯明永'),\
        (r'黄磊', r'黄磊'),\
        (r'何婷', r'何婷'),\
        (r'韩大卫', r'韩大卫'),\
        (r'金志华', r'金志华'),\
        (r'金洪波', r'金洪波'),\
        (r'乐歌谣', r'乐歌谣'),\
        (r'李彩云', r'李彩云'),\
        (r'李治国', r'李治国'),\
        (r'刘崇美', r'刘崇美'),\
        (r'刘龙', r'刘龙'),\
        (r'李杰龙', r'李杰龙'),\
        (r'卢玲玲', r'卢玲玲'),\
        (r'毛明华', r'毛明华'),\
        (r'聂亚娜', r'聂亚娜'),\
        (r'潘琳', r'潘琳'),\
        (r'钱镇华', r'钱镇华'),\
        (r'邱炜', r'邱炜'),\
        (r'裘江平', r'裘江平'),\
        (r'饶红霞', r'饶红霞'),\
        (r'饶双宜', r'饶双宜'),\
        (r'沈枫', r'沈枫'),\
        (r'施莹', r'施莹'),\
        (r'唐昌顼', r'唐昌顼'),\
        (r'田路', r'田路'),\
        (r'汪飞', r'汪飞'),\
        (r'王磊', r'王磊'),\
        (r'王敏', r'王敏'),\
        (r'王任', r'王任'),\
        (r'王益维', r'王益维'),\
        (r'魏开祥', r'魏开祥'),\
        (r'翁秀娟', r'翁秀娟'),\
        (r'吴飞英', r'吴飞英'),\
        (r'吴昊', r'吴昊'),\
        (r'吴淑明', r'吴淑明'),\
        (r'武立福', r'武立福'),\
        (r'王文其', r'王文其'),\
        (r'王振', r'王振'),\
        (r'夏爱军', r'夏爱军'),\
        (r'向小娟', r'向小娟'),\
        (r'谢作豪', r'谢作豪'),\
        (r'徐凯', r'徐凯'),\
        (r'夏海强', r'夏海强'),\
        (r'杨振', r'杨振'),\
        (r'于泉', r'于泉'),\
        (r'姚振宇', r'姚振宇'),\
        (r'尹社红', r'尹社红'),\
        (r'尤建平', r'尤建平'),\
        (r'杨磊', r'杨磊'),\
        (r'叶庆龙', r'叶庆龙'),\
        (r'应烈勇', r'应烈勇'),\
        (r'袁杰', r'袁杰'),\
        (r'张浩', r'张浩'),\
        (r'张文科', r'张文科'),\
        (r'赵世鑫', r'赵世鑫'),\
        (r'赵玮芳', r'赵玮芳'),\
        (r'郑义民', r'郑义民'),\
        (r'周光普', r'周光普'),\
        (r'周杰', r'周杰'),\
        (r'张蕃', r'张蕃'),\
        (r'章剑彪', r'章剑彪'),\
        (r'张明泽', r'张明泽'),\
        (r'赵阳', r'赵阳'),\
        (r'朱蕾', r'朱蕾'),\
        (r'郑伟', r'郑伟'),\
        )#team的choice

energy_choices = (
        (r'0', r'0'),\
        (r'1', r'1'),\
        (r'2', r'2'),\
        (r'3', r'3'),\
        (r'4', r'4'),\
        (r'5', r'5'),\
        )#review2的投入度choice

totaltime_choices = (
        (r'0.25', r'0.25'),\
        (r'0.5', r'0.5'),\
        (r'1', r'1'),\
        (r'1.5', r'1.5'),\
        (r'2', r'2'),\
        (r'2.5', r'2.5'),\
        (r'3', r'3'),\
        (r'4', r'4'),\
        )#review1花的时间的choice

rootcase_choices = (('','-------------------'),
        (r'产品和分支差异', r'产品和分支差异'),\
        (r'代码设计缺陷', r'代码设计缺陷'),\
        (r'代码实现错误', r'代码实现错误'),\
        (r'代码优化', r'代码优化'),\
        (r'规避软件问题', r'规避软件问题'),\
        (r'规避硬件问题', r'规避硬件问题'),\
        (r'合并代码及编译错误', r'合并代码及编译错误'),\
        (r'其它', r'其它'),\
        (r'新需求', r'新需求'),\
        (r'新需求实现不完整', r'新需求实现不完整'),\
        (r'业务逻辑错误', r'业务逻辑错误'),\
        )#MR root cause的choice

leadinto_choices = (
        (r'True', r'True'),\
        (r'False', r'False'),\
        )#是否是引入的choice

module_choices = (('','-------------------'),
        (r'1588', r'1588'),\
        (r'ACL', r'ACL'),\
        (r'Alarm', r'Alarm'),\
        (r'AUX card', r'AUX card'),\
        (r'BCM', r'BCM'),\
        (r'BSP/BIOS', r'BSP/BIOS'),\
        (r'CFP', r'CFP'),\
        (r'CLI', r'CLI'),\
        (r'CLK', r'CLK'),\
        (r'DC', r'DC'),\
        (r'DualHome', r'DualHome'),\
        (r'ECN', r'ECN'),\
        (r'Ethernet Interface Card', r'Ethernet Interface Card'),\
        (r'Ethernet Service Card', r'Ethernet Service Card'),\
        (r'FAN card', r'FAN card'),\
        (r'FP', r'FP'),\
        (r'ICCP', r'ICCP'),\
        (r'IGMP', r'IGMP'),\
        (r'IIC', r'IIC'),\
        (r'LACP', r'LACP'),\
        (r'LED', r'LED'),\
        (r'Link OAM', r'Link OAM'),\
        (r'LPT', r'LPT'),\
        (r'LSP/PW APS', r'LSP/PW APS'),\
        (r'LUA', r'LUA'),\
        (r'MR Review', r'MR Review'),\
        (r'MSP', r'MSP'),\
        (r'NeSvc', r'NeSvc'),\
        (r'NSP', r'NSP'),\
        (r'OAM', r'OAM'),\
        (r'OAM card', r'OAM card'),\
        (r'OAM G.1711', r'OAM G.1711'),\
        (r'OAM G.1731', r'OAM G.1731'),\
        (r'OAM G.8113.1', r'OAM G.8113.1'),\
        (r'ObjMng', r'ObjMng'),\
        (r'OSPF', r'OSPF'),\
        (r'Other', r'Other'),\
        (r'Performance', r'Performance'),\
        (r'PHY', r'PHY'),\
        (r'Platform', r'Platform'),\
        (r'POS card', r'POS card'),\
        (r'PPC card', r'PPC card'),\
        (r'PWIN card', r'PWIN card'),\
        (r'QOS', r'QOS'),\
        (r'SDH/PDH/ATM card', r'SDH/PDH/ATM card'),\
        (r'SDH/PDH/ATM service', r'SDH/PDH/ATM service'),\
        (r'Simulator', r'Simulator'),\
        (r'Switch', r'Switch'),\
        (r'System', r'System'),\
        (r'Transceiver', r'Transceiver'),\
        (r'Upgrade', r'Upgrade'),\
        (r'Vpws/Vpls', r'Vpws/Vpls'),\
        (r'VxWorks', r'VxWorks'),\
        (r'WarmReboot', r'WarmReboot'),\
        (r'ZEBOS', r'ZEBOS'),\
        )#module的choice

team_choices = (('','---------'),
        (r'access', r'access'),\
        (r'BSP', r'BSP'),\
        (r'CES', r'CES'),\
        (r'CLK', r'CLK'),\
        (r'CPL', r'CPL'),\
        (r'DPL', r'DPL'),\
        (r'FPL', r'FPL'),\
        (r'NR', r'NR'),\
        (r'OAM', r'OAM'),\
        (r'PPC', r'PPC'),\
        (r'switch', r'switch'),\
        (r'TN735', r'TN735'),\
        (r'QM', r'QM'),\
        )#team的choice

#各分支对应的审核人
approvers = {}
approvers[r'develop@\TN710']=('hz05401','hz15020','hz08377','hz05600','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz21203','hz05916','hz08692','hz05867','hz20173','hz05941','hz05936',)
#approvers[r'develop@\TN710']=('hz08678','admin',)#FIXME just for test
approvers[r'feat_tn703@\OnsPlatform']=('hz15020','admin','hz08377','hz03881','hz05600','hz08483', 'hz08539','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20173','hz20173','hz05941','hz05936',)
approvers[r'develop@\TN715']=('hz15020','hz08377','hz05600','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20173','hz05941','hz05936',)
approvers[r'feat_v13@\TN715']=('hz15020','hz08377','hz05600','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20173','hz05941','hz05936',)
approvers[r'main@\OnsPlatform']=('hz08377','hz03881','hz15020','hz05600','hz08483', 'hz08539','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20173','hz05941','hz05936',)
approvers[r'10G_CHT_06MAR30_BR@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers[r'feat_KT_220X@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['10G_SbbV2217@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
#approvers['feature@\NetRing']=('hz05999',)
approvers['feature@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['NR40K_V1_20070709@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['NR600V1_BaseV23117@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['NR40K_V1_20090204@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['NR2G5_XC_BOARD@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['2500_Distributed_Final@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['NR10K_BaseV2319SP2@\NetRing']=('hz15018','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15020','hz21203','hz05916','hz08692','hz05867','hz05941','hz05936',)
approvers['TN7X5_SBB_V1.2.0_Dev@\OnsPlatform']=('hz08377','hz03881','hz15020','hz05600','hz08483', 'hz08539','hz05889','hz08541','hz05604','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN7xx_Universe_Unification_Base@\OnsPlatform']=('hz08377','hz03881','hz15020','hz05600','hz08483', 'hz08539','hz15018','hz05889','hz08541','hz05604','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN705_V1.3.2.14_branch@\OnsPlatform']=('hz08377','hz08539','hz15020','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05604','hz05941','hz05936',)
approvers['TN765_R1.1_maintenance@\OnsPlatform']=('hz08377','hz08539','hz15020','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN705_V1.5.0.6_maintain@\OnsPlatform']=('hz08377','hz08539','hz15020','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916', 'hz08541','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05604','hz05941','hz05936',)
approvers['sbb_V1.3.2.18_base@\OnsPlatform']=('hz08377','hz08539','hz15020','admin','hz05600','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN7xx_V2.2.2.4@\OnsPlatform']=('hz08377','hz03881','hz15020','hz05600','hz08483', 'hz08539','hz15018','hz05889','hz08541','hz05604','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN7xx_V2.2.3.x@\OnsPlatform']=('hz08377','hz03881','hz15020','hz05600','hz08483', 'hz08539','hz15018','hz05889','hz08541','hz05604','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz20173','hz05941','hz05936',)
approvers['TN735_DEV1@\OnsPlatform']=('hz08483','hz15020','hz05604','hz05881','hz05819','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz05941','hz20173','hz05936',)
approvers['TN735_DEV_MAINTAIN@\OnsPlatform']=('hz08483','hz15020','hz05604','hz05881','hz05819','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz08541','hz05941','hz20173','hz05936',)
approvers['TN735_CHT_MAINTIAN@\OnsPlatform']=('hz08483','hz15020','hz05604','hz05881','hz05819','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz08541','hz05941','hz20173','hz05936',)
approvers['TN735_V2.1.1_maintain@\OnsPlatform']=('hz08483','hz15020','hz05604','hz05881','hz05819','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz05941','hz20173','hz05936',)
approvers['TN735_V2.1.2.8_maintain@\OnsPlatform']=('hz08483','hz15020','hz05604','hz05881','hz05819','admin','hz03523','hz07706','hz08531','hz07704','hz08412','hz21150','hz05890','hz15018','hz21203','hz05916','hz08692','hz05867','hz20186','hz05973','hz20249','hz05941','hz20173','hz05936',)
# XPON 
approvers['ONS00029627_ctc21@\\admin-pon-vob']=('hz15020','hz07706','hz08309','admin','hz08692',)
approvers['ONS00038638@\\admin-pon-vob']=('hz15020','hz07706','hz08309','admin','hz08692',)
approvers['iAN_B1205_R2.1.0_MAIN@\\ian8k_b1200_adm']=('hz03523','hz15020','hz07706','hz08309','admin','hz08692',)
approvers['test']=('admin',)

#审核人的名称
approver_name = {}
approver_name['admin']='admin'
approver_name['hz05401']='Wang Jing (ONS)'
approver_name['hz15020']='Wang Fei'
approver_name['hz15018']='Zhao Shixin'
approver_name['hz08377']='Ge Haifeng'
approver_name['hz03881']='Chen Song'
approver_name['hz05600']='Yin Shehong'
approver_name['hz08483']='Li Zhiguo'
approver_name['hz08539']='Liu Long'
approver_name['hz05889']='Qiu Wei'
approver_name['hz08541']='Tian Lu'
approver_name['hz05604']='Wu Lifu'
approver_name['hz21203']='Feng Jialiang'
approver_name['hz05916']='Jin Zhihua(BBU)'
# add by Wu Shuming 2011/10/14 (this is QM)
approver_name['hz03188']='Cheng Zhenbo'
approver_name['hz03523']='Yang Lei'
approver_name['hz07706']='Shi Ying'
approver_name['hz08531']='Weng Xiujuan'
approver_name['hz07704']='Rao ShuangYi'
approver_name['hz08412']='Gao Yonghong'
approver_name['hz21150']='Lu Lingling'
approver_name['hz05890']='Zhao Weifang'
approver_name['hz20173']='Fan Chuanlin'
# XPON approver
approver_name['hz03188']='Cheng Zhenbo'
approver_name['hz03523']='Yang Lei'
approver_name['hz08309']='Hu ChangYin'
approver_name['hz03876']='Wang Wei'
approver_name['hz08732']='Li Min'
approver_name['hz08692']='Zheng Wei'

#QM of each team
approver_name['hz05867']='Feng Shaocong'
approver_name['hz20186']='Wu Feiying'
approver_name['hz05973']='Rao Hongxia'
approver_name['hz20249']='Yang Zhen'
approver_name['hz05941']='He Yubin'


#TN735_DEV1 
approver_name['hz05881']='Huang Lei'
approver_name['hz05819']='Zheng Yimin'

# tset client
approver_name['hz05999']='Wu Shuming'
vob_branch_status = {}
vob_branch_release_number= {}

jobnumber_name = {
        r"admin":[r"吴淑明","ADMIN"],
        r"hz07704": [r"饶双宜", 'QM'],
        r"hz07706": [r"施莹", 'QM'],
        r"hz05918": [r"姚振宇",'FPL'],
        r"hz05936": [r"陈玲萍",'NR'],
        r'hz08704': [r'程焱芳','OAM'],
        r'hz05924': [r'丁庆华','TN735'],
        r'hz20173': [r'范传林','CES'],
        r'hz21203': [r'冯佳良','NR'],
        r'hz05867': [r'冯绍聪','NR'],
        r'hz05950': [r'高华能','access'],
        r'hz08377': [r'葛海峰','CES'],
        r'hz05941': [r'何玉斌','PPC'],
        r'hz05881': [r'黄磊','TN735'],
        r'hz05916': [r'金志华','OAM'],
        r'hz08705': [r'李彩云','CLK'],
        r'hz08483': [r'李治国','TN735'],
        r'hz05988': [r'刘崇美','PPC'],
        r'hz08539': [r'刘龙','PPC'],
        r'hz21150': [r'卢玲玲','CPL'],
        r'hz08731': [r'毛明华','CPL'],
        r'hz08702': [r'潘琳','DPL'],
        r'hz05889': [r'邱炜','CPL'],
        r'hz05850': [r'沈枫','BSP'],
        r'hz08541': [r'田路','DPL'],
        r'hz15020': [r'汪飞',''],
        r'hz05990': [r'王磊','NR'],
        r'hz20259': [r'王敏','PPC'],
        r'hz05933': [r'王益维','CES'],
        r'hz08531': [r'翁秀娟','QM'],
        r'hz20186': [r'吴飞英','PPC'],
        r'hz08714': [r'吴昊','PPC'],
        r'hz05999': [r'吴淑明','FPL'],
        r'hz05604': [r'武立福','CLK'],
        r'hz20199': [r'夏海强','switch'],
        r'hz05917': [r'谢作豪','CES'],
        r'hz08706': [r'徐凯','CLK'],
        r'hz05600': [r'尹社红',''],
        r'hz08716': [r'张明泽','CPL'],
        r'hz05997': [r'张文科','OAM'],
        r'hz15018': [r'赵世鑫',''],
        r'hz05890': [r'赵玮芳','DPL'],
        r'hz05819': [r'郑义民','TN735'],
        r'hz20210': [r'周光普','OAM'],
        r'hz08713': [r'周杰','OAM'],
        r'hz03008': [r'朱蕾','BSP'],
        r'hz08762': [r'陈波','CPL'],
        r'hz08787': [r'陈骋','DPL'],
        r'hz08767': [r'陈莹','access'],
        r'hz08781': [r'方樟钱','NR'],
        r'hz08412': [r'高永红','QM'],
        r'hz08788': [r'龚俊强','OAM'],
        r'hz08751': [r'顾雪敏','DPL'],
        r'hz08793': [r'侯明永','CLK'],
        r'hz08808': [r'何婷','CPL'],
        r'hz08766': [r'韩大卫','access'],
        r'hz03190': [r'金洪波','access'],
        r'hz08746': [r'乐歌谣','NR'],
        r'hz08765': [r'李杰龙','FPL'],
        r'hz08778': [r'聂亚娜','access'],
        r'hz05986': [r'钱镇华','CES'],
        r'hz08749': [r'裘江平','FPL'],
        r'hz05973': [r'饶红霞','CES'],
        r'hz08719': [r'唐昌顼','PPC'],
        r'hz08759': [r'王任','CES'],
        r'hz05992': [r'魏开祥','PPC'],
        r'hz08783': [r'王文其','DPL'],
        r'hz08754': [r'王振','CPL'],
        r'hz08760': [r'夏爱军','TN735'],
        r'hz08743': [r'向小娟','OAM'],
        r'hz20249': [r'杨振','CLK'],
        r'hz08780': [r'于泉','TN735'],
        r'hz08693': [r'尤建平','BSP'],
        r'hz03523': [r'杨磊',''],
        r'hz08805': [r'叶庆龙','access'],
        r'hz05998': [r'应烈勇','access'],
        r'hz05978': [r'袁杰','access'],
        r'hz08768': [r'张浩','PPC'],
        r'hz08703': [r'张蕃','FPL'],
        r'hz05989': [r'章剑彪','BSP'],
        r'hz08745': [r'赵阳','BSP'],
        r'hz08692': [r'郑伟','access'],
        r'hz08811': [r'陈官伟','access'],
}

approver_choices = (('','---------'),\
        ('admin','admin'),\
        ('hz15020','Wang Fei'),\
        ('hz15018','Zhao Shixin'),\
        ('hz08377','Ge Haifeng'),\
        ('hz03881','Chen Song'),\
        ('hz05600','Yin Shehong'),\
        ('hz08483','Li Zhiguo'),\
        ('hz08539','Liu Long'),\
        ('hz05889','Qiu Wei'),\
        ('hz08541','Tian Lu'),\
        ('hz05604','Wu Lifu'),\
        ('hz03188','Cheng Zhenbo'),\
        ('hz03523','Yang Lei'),\
        ('hz07706','Shi Ying'),\
        ('hz08531','Weng Xiujuan'),\
        ('hz07704','Rao ShuangYi'),\
        ('hz08412','Gao Yonghong'),\
        ('hz21150','Lu Lingling'),\
        ('hz05890','Zhao Weifang'),\
        ('hz03188','Cheng Zhenbo'),\
        ('hz03523','Yang Lei'),\
        ('hz08309','Hu ChangYin'),\
        ('hz05881','Huang Lei'),\
        ('hz05819','Zheng Yimin'),\
        ('hz08692','Zheng Wei'),\
        ('hz20173','Fan Chuanlin'),\
        ('hz05999','test'))

specId_choices = (('','---------'),\
        ('LErrCode',' LErrCode'),\
        ('NDT','NDT'),\
        ('LDataType','LDataType'),\
        ('LPerPrimId','LPerPrimId'),\
        ('LPerIdUnit','LPerIdUnit'),\
        ('LPerId','LPerId'))


#可以开通/关闭CC权限的用户
admin_user = ('admin', 'hz15020','hz15018')

#如果这里面的用户不在CC的许可权限内，则自动加上。
#回收的时候不回收这几个用户
vob_masters = {}
vob_masters['10G_CHT_06MAR30_BR@\NetRing']=('hz15018', 'hz20018', 'hz05172','hz21203','hz07706','hz08692',)
vob_masters['feat_KT_220X@\NetRing']=('hz15018', 'hz20018', 'hz05172','hz21203','hz07706','hz08692',)
vob_masters['10G_SbbV2217@\NetRing']=('hz15018', 'hz20018', 'hz05172','hz08377','hz21203','hz07706','hz08692','hz20173',)
vob_masters['feature@\NetRing']=('hz15018', 'hz20018', 'hz05172','hz21203','hz07706','hz08692',)
vob_masters['NR40K_V1_20070709@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['NR600V1_BaseV23117@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['NR40K_V1_20090204@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['NR2G5_XC_BOARD@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['2500_Distributed_Final@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['NR10K_BaseV2319SP2@\NetRing']=('hz15018','hz21203','hz07706','hz08692',)
vob_masters['TN7X5_SBB_V1.2.0_Dev@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08692',)
vob_masters['TN705_V1.3.2.14_branch@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08745','hz05989','hz20228','hz08692',)
vob_masters['TN765_R1.1_maintenance@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08745','hz05989','hz20228','hz08692',)
vob_masters['TN705_V1.5.0.6_maintain@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08745','hz05989','hz20228','hz08692',)
vob_masters['sbb_V1.3.2.18_base@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08692',)
vob_masters['TN7xx_Universe_Unification_Base@\OnsPlatform']=('hz15018','hz15020','hz08438', 'hz01388', 'hz03190', 'hz03997', 'hz03716', 'hz08546', 'hz03523', 'hz08312', 'hz03933','hz21203','hz05799','hz07706','hz08692',)
vob_masters['TN7xx_V2.2.2.4@\OnsPlatform']=('hz15018','hz15020','hz08438', 'hz01388', 'hz03190', 'hz03997', 'hz03716', 'hz08546', 'hz03523', 'hz08312', 'hz03933','hz21203','hz05799','hz07706','hz08692',)
vob_masters['TN7xx_V2.2.3.x@\OnsPlatform']=('hz15018','hz15020','hz08438', 'hz01388', 'hz03190', 'hz03997', 'hz03716', 'hz08546', 'hz03523', 'hz08312', 'hz03933','hz21203','hz05799','hz07706','hz08692',)
vob_masters['feat_tn703@\OnsPlatform']=('hz15018','hz15020','hz21203','hz07706','hz08692',)
vob_masters['TN735_DEV1@\OnsPlatform']=('hz15018','hz15020','hz08483','hz21203','hz07706','hz08692',)
vob_masters['TN735_DEV_MAINTAIN@\OnsPlatform']=('hz15018','hz15020','hz08483','hz21203','hz07706','hz08692',)
vob_masters['TN735_CHT_MAINTIAN@\OnsPlatform']=('hz15018','hz15020','hz08483','hz21203','hz07706','hz08692',)
vob_masters['TN735_V2.1.1_maintain@\OnsPlatform']=('hz15018','hz15020','hz08483','hz21203','hz07706','hz08692',)
vob_masters['TN735_V2.1.2.8_maintain@\OnsPlatform']=('hz15018','hz15020','hz08483','hz21203','hz07706','hz08692',)
vob_masters['main@\OnsPlatform']= ('hz15018','hz15020','hz08483', 'hz01388', 'hz03190', 'hz03997', 'hz03716', 'hz08546', 'hz03523', 'hz08312', 'hz03933','hz21203','hz07706','hz08692',)
vob_masters['ONS00029627_ctc21@\admin-pon-vob']=('hz15018','hz08309','hz15020','hz05799','hz07706','hz08692',)
vob_masters['ONS00038638@\admin-pon-vob']=('hz15018','hz08309','hz15020','hz05799','hz07706','hz08692',)
vob_masters['iAN_B1205_R2.1.0_MAIN@\ian8k_b1200_adm']=('hz15018','hz03523','hz08309','hz15020','hz05799','hz03876','hz08732','hz07706','hz08692',)

try:
    from workflow.vob_config import *
except Exception, e:
    from vob_config import *
