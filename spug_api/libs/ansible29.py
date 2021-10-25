import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict  # 用于添加选项。比如: 指定远程用户remote_user=None
from ansible.parsing.dataloader import DataLoader  # 读取 json/yml/ini 格式的文件的数据解析器
from ansible.vars.manager import VariableManager  # 管理主机和主机组的变量管理器
from ansible.inventory.manager import InventoryManager  # 管理资源库的，可以指定一个 inventory 文件等
from ansible.playbook.play import Play  # 用于执行 Ad-hoc 的类 ,需要传入相应的参数
from ansible.executor.task_queue_manager import TaskQueueManager  # ansible 底层用到的任务队列管理器
from ansible.plugins.callback import CallbackBase  # 处理任务执行后返回的状态
from ansible import context  # 上下文管理器，他就是用来接收 ImmutableDict 的示例对象
import ansible.constants as C  # 用于获取 ansible 产生的临时文档


class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.task_ok = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, **kwargs):
        self.host_failed[result._host.get_name()] = result


class MyAnsiable2(object):

    def __init__(self,
                 connection='local',  # 连接方式 local 本地方式，smart ssh方式
                 remote_user='root',  # ssh 用户
                 remote_password=None,  # ssh 用户的密码，应该是一个字典, key 必须是 conn_pass
                 private_key_file=None,  # 指定自定义的私钥地址
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,  # 模块路径，可以指定一个自定义模块的路径
                 become=None,  # 是否提权
                 become_method=None,  # 提权方式 默认 sudo 可以是 su
                 become_user=None,  # 提权后，要成为的用户，并非登录用户
                 check=False, diff=False,
                 listhosts=None, listtasks=None, listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None):

        # 函数文档注释
        """
        初始化函数，定义的默认的选项值，
        在初始化的时候可以传参，以便覆盖默认选项的值
        """
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            private_key_file=private_key_file,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
        )
        # 三元表达式，假如没有传递 inventory, 就使用 "localhost,"
        # 指定 inventory 文件
        # inventory 的值可以是一个 资产清单文件
        # 也可以是一个包含主机的元组，这个仅仅适用于测试
        #  比如 ： 1.1.1.1,    # 如果只有一个 IP 最后必须有英文的逗号
        #  或者： 1.1.1.1, 2.2.2.2
        self.inventory = inventory if inventory else "localhost,"
        # 实例化数据解析器
        self.loader = DataLoader()
        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)
        # 设置密码
        self.passwords = remote_password
        # 实例化回调插件对象
        self.results_callback = ResultCallback()
        # 变量管理器
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

    def run(self, hosts='localhost', gather_facts="no", module="ping", args='', task_time=0):

        """
        参数说明：
        task_time -- 执行异步任务时等待的秒数，这个需要大于 0 ，等于 0 的时候不支持异步（默认值）。这个值应该等于执行任务实际耗时时间为好
        """
        play_source = dict(
            name="Ad-hoc",
            hosts=hosts,
            gather_facts=gather_facts,
            tasks=[
                # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
                # 也可以作为参数传递过来，这里就简单化了。
                {"action": {"module": module, "args": args}, "async": task_time, "poll": 0}])
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)
            result = tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
                shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks):

        """
        Keyword arguments:
        playbooks --  需要是一个列表类型
        """
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbooks,
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)
        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback
        result = playbook.run()

    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        # print(self.results_callback.host_ok)
        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result
        # 最终打印结果，并且使用 JSON 继续格式化
        #print(json.dumps(result_raw, indent=4))
        return json.dumps(result_raw)

if __name__ == '__main__' :
    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart',remote_user='root')  # 创建资源库对象
    ansible3.run(hosts=["192.168.50.146","127.0.0.1"], module="ping", args='')
    stdout_dict = json.loads(ansible3.get_result())
    # print(stdout_dict['success']['127.0.0.1']["ansible_facts"]["ansible_mounts"])
    print(stdout_dict)
