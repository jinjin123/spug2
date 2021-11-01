/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
export default [
  {icon: 'desktop', title: '工作台', auth: 'home.home.view', path: '/home'},
  {
    icon: 'cloud-server', title: '资产管理', auth: 'host.host.view', child: [
      // {title: '', auth: 'exec.task.do', path: '/exec/task'},
      {icon: 'cloud-server', title: '主机管理', auth: 'host.host.view', path: '/host'},
      {icon: 'cloud-server', title: '数据库管理', auth: 'host.host.view', path: '/dbserver'},
      {icon: 'cloud-server', title: '服务包管理', auth: 'host.host.view', path: '/config/servicebag'},
      {icon: 'cloud-server', title: '端口管理', auth: 'host.host.view', path: '/config/portlist'},
      {icon: 'cloud-server', title: '集群管理', auth: 'host.host.view', path: '/config/cluster'},
      {icon: 'cloud-server', title: '项目管理', auth: 'host.host.view', path: '/config/project'},
      {icon: 'cloud-server', title: '所属区域管理', auth: 'host.host.view', path: '/config/workzone'},
      {icon: 'cloud-server', title: '资源类别管理', auth: 'host.host.view', path: '/config/zone'},
      {icon: 'cloud-server', title: '设备位置管理', auth: 'host.host.view', path: '/config/device'},
      {icon: 'cloud-server', title: '连接用户管理', auth: 'host.host.view', path: '/config/cuser'},
      {icon: 'cloud-server', title: '域名管理', auth: 'host.host.view', path: '/config/domain'},

      {icon: 'cloud-server', title: '资源类型管理', auth: 'host.host.view', path: '/config/resouret'},

    ]
  },
  // {icon: 'cloud-server', title: '主机管理', auth: 'host.host.view', path: '/host'},
  {
    icon: 'code', title: '批量执行', auth: 'exec.task.do|exec.template.view', child: [
      {title: '执行任务', auth: 'exec.task.do', path: '/exec/task'},
      {title: '模板管理', auth: 'exec.template.view', path: '/exec/template'},
    ]
  },
  {
    icon: 'flag', title: '应用发布', auth: 'deploy.app.view|deploy.request.view|deploy.rancher.view', child: [
      {title: '应用管理', auth: 'deploy.app.view', path: '/deploy/app'},
      {title: '发布申请', auth: 'deploy.request.view', path: '/deploy/request'},
      {title: 'rancher应用管理', auth: 'deploy.rancher.view', path: '/deploy/rancher'},
      {title: '应用发布审核关联管理', auth: 'deploy.notice.view', path: '/deploy/rancher/notice'},
    ]
  },
  {icon: 'schedule', title: '任务计划', auth: 'schedule.schedule.view', path: '/schedule'},
  {
    icon: 'deployment-unit', title: '配置中心', auth: 'config.env.view|config.src.view|config.rancher.view', child: [
      {title: '环境管理', auth: 'config.env.view', path: '/config/environment'},
      {title: '服务配置', auth: 'config.src.view', path: '/config/service'},
      {title: '应用配置', auth: 'config.app.view', path: '/config/app'},
      {title: 'rancher数据卷配置', auth: 'config.rancher.view', path: '/config/rancherconf'},
      // {title: '备份配置', auth: 'config.backup.view', path: '/config/backup'},
    ]
  },
  {icon: 'monitor', title: '监控中心', auth: 'monitor.monitor.view', path: '/monitor'},
  {
    icon: 'alert', title: '报警中心', auth: 'alarm.alarm.view|alarm.contact.view|alarm.group.view', child: [
      {title: '报警历史', auth: 'alarm.alarm.view', path: '/alarm/alarm'},
      {title: '报警联系人', auth: 'alarm.contact.view', path: '/alarm/contact'},
      {title: '报警联系组', auth: 'alarm.group.view', path: '/alarm/group'},
    ]
  },
  {
    icon: 'setting', title: '系统管理', auth: "system.account.view|system.role.view|system.setting.view", child: [
      {title: '账户管理', auth: 'system.account.view', path: '/system/account'},
      {title: '角色管理', auth: 'system.role.view', path: '/system/role'},
      {title: '系统设置', auth: 'system.setting.view', path: '/system/setting'},
    ]
  },
]
