/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, message,Select, Tag } from 'antd';
import { AuthDiv } from 'components';
import ComForm from './Form';
import FormWin from './FormWin';
import ComImport from './Import';
import { http } from 'libs';
import store from './store';
// import envStore from 'pages/config/environment/store';



@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        moreAction: [{"id":0,"v":"更多操作...."}],
        modifypwd: []
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
        return http.delete('/api/host/resource/host/', {params: {id: text.id}})
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
  columns = [
    {
      title: '操作',
      render: info => {
        return        <AuthDiv auth="host.host.add" style={{marginBottom: 16}}>
        <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." } autoClearSearchValue	allowClear={true} onChange={this.onChange.bind(this,info)}  style={{ width: 100 }} >
          <Select.Option value={1}>编辑</Select.Option>
          <Select.Option value={2}>终端</Select.Option>
          <Select.Option value={3}>待回收</Select.Option>
        </Select>
        </AuthDiv>
      }
    },
    {
      title: '实体项目',
      dataIndex: 'top_project',
      render: info => {
        let tinfo = [];
        let data = store.pj
        // console.log(data)
        info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map(dd => {
                tinfo.push(dd.name)
            })
        })
        return <span>{tinfo.join(";")}</span>
      },
    },
    {
      title: '项目子类',
      dataIndex: 'child_project',
      render: info => {
        let tinfo = [];
        let data = store.pj
        // console.log(data)
        info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map(dd => {
                tinfo.push(dd.name)
            })
        })
        return <span>{tinfo.join(";")}</span>
      },
    },
    {
      title: '所属集群',
      dataIndex: 'cluster',
      render: info =>{
        let tinfo =[];
        let data = store.cs
        // console.log(cuStore.records)
            info.map(ditem => { 
              let newArr = data.filter(item => item.id === ditem)
              newArr.map(dd => {
                  tinfo.push(dd.name)
              })
          })
          return <span>{tinfo.join(";")}</span>


      },
    },
    {
      title: '主机名',
      dataIndex: 'hostname',
    },
    {
      title: '外网IP',
      dataIndex: 'outter_ip',
    },
    {
      title: '虚拟IP',
      dataIndex: 'v_ip',
    },
    {
      title: '业务IP',
      dataIndex: 'ipaddress',
    },
    {
      title: '连接用户',
      dataIndex: 'username',
      render: info =>{
        let tinfo = "";
        let data = store.cuser
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map(dd => {
                // tinfo.push(dd.name)
                tinfo = dd.name
            })
        // })
        return <span>{tinfo}</span>
      },
    },
    {
      title: '资源类别',
      dataIndex: 'zone',
      render: info => {
        let tinfo = [];
        let data = store.zz
        // console.log(data)
          info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map(dd => {
                tinfo.push(dd.name)
            })
        })
        return <span>{tinfo.join(";")}</span>
      
      },
    },
    {
      title: '系统类型',
      dataIndex: 'ostp',
    },
    {
      title: '资源类型',
      dataIndex: 'resource_type',
      render: info =>{
        let tinfo = "";
        let data = store.rset
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map(dd => {
                // tinfo.push(dd.name)
                tinfo = dd.name
            })
        // })
        return <span>{tinfo}</span>
      },
    },
    {
      title: '系统',
      dataIndex: 'osType',
    },
    {
      title: '版本',
      dataIndex: 'osVerion',
    },
    {
      title: '内核版本',
      dataIndex: 'coreVerion',
    },
    {
      title: 'cpu逻辑核心',
      dataIndex: 'cpus',
    },
    {
      title: '内存(G)',
      dataIndex: 'memory',
    },
    {
      title: '状态',
      dataIndex: 'status',
      render: status => {
          return      <Tag color={status === "在线" ? "green":"volcano"} key={status}>
          {status ==="在线" ? "在线" : "离线"}
        </Tag>
      },
    },
    {
      title: '系统盘',
      dataIndex: 'sys_disk',
    },
    {
      title: '硬盘空间',
      dataIndex: 'sys_data',
    },
    {
      title: '设备位置',
      dataIndex: 'provider',
      render: info =>{
        let tinfo = "";
        let data = store.dvpo
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map(dd => {
                // tinfo.push(dd.name)
                tinfo = dd.name
            })
        // })
        return <span>{tinfo}</span>
      },
    },
    {
      title: '实际用途',
      dataIndex: 'use_for',
    },
    {
      title: '供应商',
      dataIndex: 'supplier',
    },
    {
      title: '开发',
      dataIndex: 'developer',
    },
    {
      title: '运维',
      dataIndex: 'opsper',
    },
    {
      title: '录入人',
      dataIndex: 'create_by',
    },
    {
      title: '安装服务',
      dataIndex: 'service_pack',
      render: info => {
        let tinfo = [];
        let data = store.svbag
        // console.log(data)
        info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map(dd => {
                tinfo.push(dd.name)
            })
        })
        return <span>{tinfo.join(";")}</span>
      },
    },
    // {
    //   title: '补丁服务与版本',
    //   dataIndex: 'host_bug',
    // },
    // {
    //   title: '扩展配置',
    //   dataIndex: 'ext_config1',
    // },
    {
      title: '环境',
      dataIndex: 'env_id',
      render: info => {
        let tinfo = "";
        let data = store.envs
        let newArr = data.filter(item => item.id === info)
        newArr.map(dd => {
            // tinfo.push(dd.name)
            tinfo = dd.name
        })
        return  <span>{tinfo}</span>
      },
    },
    {
      title: '待回收ip',
      dataIndex: 'iprelease',
    },
    {
      title: '备注信息',
      dataIndex: 'comment',
    },
  ]
  rowSelection = {
    
    onChange: (selectedRowKeys, selectedRows) => {
      store.modifypwdkey = selectedRowKeys

    },
    getCheckboxProps: record => ({
      
    }),
  };
  render() {
      let data = store.permRecords;
      if(store.tpjj){
        store.tpjj.map(titem =>(
          data = data.filter(item => item["top_project"].includes(titem))
        ))
      }
      if(store.chjj){
        store.chjj.map(titem =>(
          data = data.filter(item => item["child_project"].includes(titem))
        ))
      }
      if(store.csst){
        store.csst.map(titem =>(
          data = data.filter(item => item["cluster"].includes(titem))
        ))
      }
    // if (store.f_name) {
    //   data = data.filter(item => item['name'].toLowerCase().includes(store.f_name.toLowerCase()))
    // }
    if (store.f_zone) {
      store.f_zone.map(titem=>(
        data = data.filter(item => item['zone'].includes(titem))
      ))
    }
    if (store.f_ip) {
      let tt = []
      let tmp,tmp1,tmp2
      tmp = data.filter(item => item['ipaddress'].toLowerCase().includes(store.f_ip.toLowerCase()))
      tmp1 = data.filter(item => item['outter_ip'] != null? item['outter_ip'].toLowerCase().includes(store.f_ip.toLowerCase()) : null)
      tmp2 = data.filter(item => item['v_ip'] != null ? item['v_ip'].toLowerCase().includes(store.f_ip.toLowerCase()): null)
      data = tt.concat(tmp,tmp1,tmp2)
      data = [...new Set(data)]
    }

    if (store.otp) {
      data = data.filter(item => item['ostp'].toLowerCase().includes(store.otp.toLowerCase()))
    }
    // if (store.tpjj) {
    //   data = data.filter(item => item['top_project'].toLowerCase().includes(store.tpjj.toLowerCase()))
    // }
    if (store.pvd) {
      data = data.filter(item => item['provider'] === store.pvd)
    }
    if (store.rtp) {
      data = data.filter(item => item['resource_type'] ===store.rtp)
    }
    if (store.wzz) {
      data = data.filter(item => item['work_zone'] ===store.wzz)
    }
    store.tmpExcel = data;
    return (
      <React.Fragment>
        <Table
          rowKey="id"
          loading={store.isFetching}
          // size="middle"
          rowSelection={this.rowSelection}

          dataSource={data}
          columns={this.columns}
          expandedRowRender={data => <p style={{ margin: 0 }}>{data.data_disk}</p>}
          scroll={{ x: '230%' }}
          pagination={{
            showSizeChanger: true,
            showLessItems: true,
            hideOnSinglePage: true,
            showTotal: total => `共 ${total} 条`,
            pageSizeOptions: ['10', '20', '50', '100']
          }}>
          {/* <Table.Column title="实体项目" dataIndex="top_project"/>
          <Table.Column title="主机名" dataIndex="hostname" />
          <Table.Column title="外网IP" dataIndex="outter_ip"/>
          <Table.Column title="虚拟IP" dataIndex="v_ip"/>
          <Table.Column title="业务IP" dataIndex="ipaddress" width={130} />
          <Table.Column title="连接用户" dataIndex="username"/>
          <Table.Column title="分组" dataIndex="zone"/>
          <Table.Column title="系统类型" dataIndex="ostp"/>
          <Table.Column title="系统" dataIndex="osType"/>
          <Table.Column title="版本" dataIndex="osVerion"/>
          <Table.Column title="内核版本" dataIndex="coreVerion"/>
          <Table.Column title="cpu逻辑核心" dataIndex="cpus"/>
          <Table.Column title="内存(G)" dataIndex="memory"/>
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
          <Table.Column title="系统盘" dataIndex="sys_disk"/>

          <Table.Column title="运营商" dataIndex="provider" />
          <Table.Column title="资源类型" dataIndex="resource_type"/>
          <Table.Column title="所属区域" dataIndex="work_zone"/>
          <Table.Column title="实际用途" dataIndex="use_for"/>


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
              <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." } autoClearSearchValue	allowClear={true} onChange={this.onChange.bind(this,info)}  style={{ width: 100 }} >
              <Option value={1}>编辑</Option>
              <Option value={2}>终端</Option>
              <Option value={3}>待回收</Option>
            </Select>
            )}/>
          )} */}
          
        </Table>
        {store.formVisible && <ComForm/>}
        {store.winformVisible && <FormWin/>}
        {store.importVisible && <ComImport/>}
      </React.Fragment>
    )
  }
}

export default ComTable
