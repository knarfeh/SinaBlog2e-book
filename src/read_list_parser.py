# -*- coding: utf-8 -*-
from src.container.task import SingleTask, TaskPackage
from src.tools.debug import Debug
from src.tools.match import Match
from src.tools.type import Type


class ReadListParser():
    u"""
    通过分析指令, 获得TaskPackage对象, 其中,有work_list={}和book_list{}
    """

    @staticmethod
    def get_task(command):
        u"""
        对外的接口, 用来分析指令,
        :param command:   网页的首地址
        :return:
        """
        def split_command(command):
            u"""
            # 一行是一本书, 每一行用$符号来区分章节
            :param command: 一行命令
            :return:
            """
            return command.split('$')

        def remove_comment(command):
            u"""
            去掉#后面的注释
            :param command:
            :return:
            """
            return command.split('#')[0]

        command = remove_comment(command)
        command_list = split_command(command)
        Debug.logger.debug(u"command_list:" + str(command_list))
        raw_task_list = []
        for command in command_list:
            raw_task = ReadListParser.parse_command(command)
            if raw_task:
                raw_task_list.append(raw_task)

        task_package = ReadListParser.merge_task_list(raw_task_list)
        return task_package

    @staticmethod
    def parse_command(raw_command=''):
        u"""
        分析单条命令并返回待完成的task
        :param raw_command:   网址原始链接, 如:http://blog.sina.com.cn/u/1287694611
        :return: task
        task格式
        *   kind
            *   字符串，见TypeClass.type_list
        *   spider
            *   href
                *   网址原始链接，例http://blog.sina.com.cn/u/1287694611
                *   末尾没有『/』
        *   book
            *   kind
            *   info
            *   question
            *   answer
        """
        def detect(command):
            for command_type in Type.type_list:
                result = getattr(Match, command_type)(command)    # 目前只有SinaBlog类型
                if result:
                    return command_type
            return 'unknown'

        def parse_SinaBlog(command):
            u"""

            :param command: 某个新浪博客博主的首页地址
            :return: task:
            """
            result = Match.SinaBlog(command)
            SinaBlog_author_id = result.group('SinaBlog_people_id')
            Debug.logger.debug(u"SinaBlog_people_id:" + str(SinaBlog_author_id))
            task = SingleTask()

            task.author_id = SinaBlog_author_id
            task.kind = 'SinaBlog'
            task.spider.href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(SinaBlog_author_id)
            task.spider.href = 'http://blog.sina.com.cn/u/{}'.format(SinaBlog_author_id)
            task.spider.href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(SinaBlog_author_id)
            task.book.kind = 'SinaBlog'
            task.book.sql.info_extra = 'creator_id = "{}"'.format(SinaBlog_author_id)
            task.book.sql.article_extra = 'author_id = "{}"'.format(SinaBlog_author_id)
            task.book.author_id = SinaBlog_author_id
            Debug.logger.debug(u"在parse_SinaBlog中, task.book.author_id为" + str(task.book.author_id))
            return task

        def parse_error(command):
            if command:
                Debug.logger.info(u"""无法解析记录:{}所属网址类型,请检查后重试。""".format(command))
            return

        parser = {'SinaBlog': parse_SinaBlog,
                  'unknown': parse_error}
        kind = detect(raw_command)
        return parser[kind](raw_command)

    @staticmethod
    def merge_task_list(task_list):
        task_package = TaskPackage()
        for item in task_list:
            # Debug.logger.debug(u"merge_task_list中的item是什么???" + str(item))
            task_package.add_task(item)
        return task_package.get_task()
