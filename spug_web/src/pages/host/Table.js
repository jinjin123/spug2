/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, message,Select, Tag } from 'antd';
import { Action } from 'components';
import ComForm from './Form';
import FormWin from './FormWin';
import ComImport from './Import';
import { http, hasPermission } from 'libs';
import store from './store';

@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        moreAction: [{"id":0,"v":"更多操作...."}]
    };
  
  }
  componentDidMount() {
    store.fetchRecords()
  }

  handleConsole = (info) => {
    window.open(`/ssh/${info.id}`)
  };

  handleDelete = (text) => {
    Modal.confirm({
      title: '回收确认',
      content: `确定要回收【${text['ipaddress']}】?`,
      onOk: () => {
        return http.delete('/api/host/', {params: {id: text.id}})
          .then(() => {
            message.success('待回收成功');
            store.fetchRecords()
          })
      }
    })
  };
  onChange = (info, action) => {
    switch(action){
      case 1:
        store.record = info
        if(info["ostp"] == "Windows"){
          store.winformVisible = true;

        }else{
          store.formVisible = true;
        }
        this.setState({
          moreAction : [{"id": info.id,"v":"编辑"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "更多操作...."
          })
        },1500)
        break;
        ;;
      case 2:
        window.open(`/ssh/${info.id}`)
        this.setState({
          moreAction : [{"id": info.id,"v":"终端"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "更多操作...."
          })
        },1500)
        break;
      case 3:
        this.handleDelete(info)
        this.setState({
          moreAction : [{"id": info.id,"v":"待回收"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "更多操作...."
          })
        },1500)
        break;
    }

  };

  render() {
    let data = store.permRecords;
    const {Option } = Select
    if (store.f_name) {
      data = data.filter(item => item['name'].toLowerCase().includes(store.f_name.toLowerCase()))
    }
    if (store.f_zone) {
      data = data.filter(item => item['zone'].toLowerCase().includes(store.f_zone.toLowerCase()))
    }
    if (store.f_ip) {
      data = data.filter(item => item['ipaddress'].toLowerCase().includes(store.f_ip.toLowerCase()))
    }

    if (store.otp) {
      data = data.filter(item => item['ostp'].toLowerCase().includes(store.otp.toLowerCase()))
    }
    return (
      <React.Fragment>
        <Table
          rowKey="id"
          loading={store.isFetching}
          // size="middle"
          dataSource={data}
          expandedRowRender={data => <p style={{ margin: 0 }}>{data.disk}</p>}
          scroll={{ x: '210%' }}
          pagination={{
            showSizeChanger: true,
            showLessItems: true,
            hideOnSinglePage: true,
            showTotal: total => `共 ${total} 条`,
            pageSizeOptions: ['10', '20', '50', '100']
          }}>
          <Table.Column title="实体项目" dataIndex="top_project"/>
          <Table.Column title="主机名" dataIndex="hostname" />
          <Table.Column title="IP" dataIndex="ipaddress" width={130} />
          <Table.Column title="连接用户" dataIndex="username"/>
          {/* <Table.Column width={100} title="端口" dataIndex="port"/> */}
          <Table.Column title="分组" dataIndex="zone"/>
          <Table.Column title="系统类型" dataIndex="ostp"/>
          <Table.Column title="系统" dataIndex="osType"/>
          <Table.Column title="版本" dataIndex="osVerion"/>
          <Table.Column title="内核版本" dataIndex="coreVerion"/>
          <Table.Column title="cpu逻辑核心" dataIndex="cpus"/>
          {/* <Table.Column title="cpu单U(核)" dataIndex="cpucore"/> */}
          
          <Table.Column title="内存(G)" dataIndex="memory"/>
          {/* <Table.Column title="状态" dataIndex="status"/> */}

          <Table.Column
            title="状态"
            dataIndex="status"
            key="status"
            render={(status) => (
              <Tag color={status === "在线" ? "green":"volcano"} key={status}>
              {status ==="在线" ? "在线" : "离线"}
            </Tag>
            )}
          />
          <Table.Column title="挂载盘数" dataIndex="disks"/>

          <Table.Column title="运营商" dataIndex="provider" />
          <Table.Column title="资源类型" dataIndex="resource_type"/>
          <Table.Column title="工作区域" dataIndex="work_zone"/>
          <Table.Column title="外网IP" dataIndex="outter_ip"/>
          <Table.Column title="虚拟IP" dataIndex="v_ip"/>
          <Table.Column title="实际用途" dataIndex="use_for"/>


          {/* <Table.Column title="挂载盘" dataIndex="disk" ellipsis/> */}
          <Table.Column title="序列号" dataIndex="serial_num"/>
          <Table.Column title="供应商" dataIndex="supplier"/>
          <Table.Column title="开发" dataIndex="developer"/>
          <Table.Column title="运维" dataIndex="opsper"/>
          <Table.Column title="录入人" dataIndex="create_by"/>
          <Table.Column title="安装服务" dataIndex="service_pack"/>
          <Table.Column title="补丁服务与版本" dataIndex="host_bug"/>
          <Table.Column title="扩展配置" dataIndex="ext_config1"/>
          <Table.Column title="环境" dataIndex="env" />
          <Table.Column title="待回收ip" dataIndex="iprelease"/>
          <Table.Column ellipsis title="备注信息" dataIndex="comment"/>
          {hasPermission('host.host.edit|host.host.del|host.host.console') && (
            <Table.Column width={100} fixed="right" title="操作" render={info => (
              // <Action>
              //   <Action.Button auth="host.host.edit" onClick={() => store.showForm(info)}>编辑</Action.Button>
              //   <Action.Button auth="host.host.del" onClick={() => this.handleDelete(info)}>删除</Action.Button>
              //   <Action.Button auth="host.host.console" onClick={() => this.handleConsole(info)}>Console</Action.Button>
              // </Action>
              <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." } autoClearSearchValue	allowClear={true} onChange={this.onChange.bind(this,info)}  style={{ width: 100 }} >
              <Option value={1}>编辑</Option>
              <Option value={2}>终端</Option>
              <Option value={3}>待回收</Option>
            </Select>
            )}/>
          )}
        </Table>
        {store.formVisible && <ComForm/>}
        {store.winformVisible && <FormWin/>}
        {store.importVisible && <ComImport/>}
      </React.Fragment>
    )
  }
}

export default ComTable
