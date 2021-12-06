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
import envStore from 'pages/config/environment/store';


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
        return http.delete('/api/host/resource/db/', {params: {id: text.id}})
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
        this.handleDelete(info)
        this.setState({
          moreAction : [{"id": info.id,"v":"删除"}]
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
      key:'opeations',
      render: (info,index) => {
        return  <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." } autoClearSearchValue	allowClear={true} onChange={this.onChange.bind(this,info)}  style={{ width: 100 }} >
          <Select.Option key={index} value={1}>编辑</Select.Option>
          <Select.Option value={2}>删除</Select.Option>
          <Select.Option key={index} value={3}>待回收</Select.Option>
        </Select>
      }
    },
    {
      title: '实体项目',
      dataIndex: 'top_project',
      key:'top_project',
      render: info => {
        let tinfo = [];
        let tindex = "";
        let data = store.pj
        // console.log(data)
        info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map((dd,index) => {
                tinfo.push(dd.name)
                tindex = index
            })
        })
        return <span key={tindex}>{tinfo.join(";")}</span>
      },
    },
    {
      title: '项目子类',
      dataIndex: 'child_project',
      key:'child_project',
      render: info => {
        let tinfo = [];
        let tindex= ""; 
        let data = store.pj
        // console.log(data)
        info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map((dd,index) => {
                tinfo.push(dd.name)
                tindex = index

            })
        })
        return <span key={tindex}>{tinfo.join(";")}</span>
      },
    },
    {
      title: '所属集群',
      dataIndex: 'cluster',
      key:'cluster',
      render: info =>{
        let tinfo =[];
        let tindex= ""; 
        let data = store.cs
        // console.log(cuStore.records)
            info.map(ditem => { 
              let newArr = data.filter(item => item.id === ditem)
              newArr.map((dd,index) => {
                  tinfo.push(dd.name)
                  tindex = index
              })
          })
          return <span key={tindex}>{tinfo.join(";")}</span>


      },
    },
    // {
    //   title: '主机名',
    //   dataIndex: 'hostname',
    // },
    {
      title: '外网IP',
      dataIndex: 'outter_ip',
      key:'outter_ip',
    },
    {
      title: '虚拟IP',
      dataIndex: 'v_ip',
      key:'v_ip',
    },
    {
      title: '业务IP',
      dataIndex: 'ipaddress',
      key:'ipaddress',

    },
    {
      title: '连接用户',
      dataIndex: 'username',
      key:'username',
      render: info =>{
        let tinfo = "";
        let tindex= "";
        let data = store.cuser
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map((dd,index) => {
                // tinfo.push(dd.name)
                tinfo = dd.name
                tindex = index
            })
        // })
        return <span key={tindex}>{tinfo}</span>
      },
    },
    {
      title: '端口',
      dataIndex: 'port',
      key:'port',

    },
    {
      title: '资源类别',
      dataIndex: 'zone',
      key:'zone',

      render: info => {
        let tinfo = [];
        let tindex= "";
        let data = store.zz
        // console.log(data)
          info.map(ditem => { 
            let newArr = data.filter(item => item.id === ditem)
            newArr.map((dd,index) => {
                tinfo.push(dd.name)
                tindex = index
            })
        })
        return <span key={tindex}>{tinfo.join(";")}</span>
      
      },
    },
    {
      title: '系统类型',
      dataIndex: 'ostp',
      key:'ostp',

    },
    {
      title: '资源类型',
      key:'resource_type',
      dataIndex: 'resource_type',
      render: info =>{
        let tinfo = "";
        let tindex = ""
        let data = store.rset
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map((dd,index) => {
                // tinfo.push(dd.name)
                tinfo = dd.name
                tindex = index
            })
        // })
        return <span key={tindex}>{tinfo}</span>
      },
    },
    {
      title: '系统',
      dataIndex: 'osType',
      key:'osType',

    },
    {
      title: '版本',
      dataIndex: 'osVerion',
      key:'osVerion',
    },
    // {
    //   title: '内核版本',
    //   dataIndex: 'coreVerion',
    // },
    // {
    //   title: 'cpu逻辑核心',
    //   dataIndex: 'cpus',
    // },
    // {
    //   title: '内存(G)',
    //   dataIndex: 'memory',
    // },
    {
      title: '状态',
      key:'status',
      dataIndex: 'status',
      render: (status,index) => {
          return      <Tag color={status === "在线" ? "green":"volcano"} key={index}>
          {status ==="在线" ? "在线" : "离线"}
        </Tag>
      },
    },
    {
      title: '关系',
      key:'dbrelation',
      dataIndex: 'dbrelation',
      render: (dbrelation,index) => {
          if(dbrelation === 1){
            return  <Tag color={"green"} key={index}>
              {"主"}
            </Tag>
          }else if (dbrelation ===2){
            return  <Tag color={"geekblue"} key={index}>
              {"从"}
            </Tag>
          }else if (dbrelation ===3){
            return  <Tag color={"purple"} key={index}>
              {"集群"}
            </Tag>
          }
          else if (dbrelation ===4){
            return  <Tag color={"grey"} key={index}>
              {"无"}
            </Tag>
          }
      },
    },
    // {
    //   title: '系统盘',
    //   dataIndex: 'sys_disk',
    // },
    {
      title: '设备位置',
      dataIndex: 'provider',
      key:'provider',
      render: info =>{
        let tinfo = "";
        let tindex = "";
        let data = store.dvpo
        // console.log(cuStore.records)
        // info.map(ditem => { 
            let newArr = data.filter(item => item.id === info)
            newArr.map((dd,index) => {
                // tinfo.push(dd.name)
                tinfo = dd.name
                tindex = index
            })
        // })
        return <span key={tindex}>{tinfo}</span>
      },
    },
    {
      title: '实际用途',
      dataIndex: 'use_for',
      key:'use_for',

    },
    // {
    //   title: '供应商',
    //   dataIndex: 'supplier',
    // },
    {
      title: '开发',
      dataIndex: 'developer',
      key:'developer',

    },
    {
      title: '运维',
      dataIndex: 'opsper',
      key:'opsper',

    },
    {
      title: '录入人',
      dataIndex: 'create_by',
      key:'create_by',

    },
    // {
    //   title: '安装服务',
    //   dataIndex: 'service_pack',
    //   render: info => {
    //     let tinfo = [];
    //     let data = store.svbag
    //     // console.log(data)
    //     info.map(ditem => { 
    //         let newArr = data.filter(item => item.id === ditem)
    //         newArr.map(dd => {
    //             tinfo.push(dd.name)
    //         })
    //     })
    //     return <span>{tinfo.join(";")}</span>
    //   },
    // },
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
      key:'env_id',
      render: info => {
        let tinfo = "";
        let data = store.envs
        let tindex = ""
        let newArr = data.filter(item => item.id === info)
        newArr.map((dd,index) => {
            // tinfo.push(dd.name)
            tinfo = dd.name
            tindex = index
        })
        return  <span key={tindex}>{tinfo}</span>
      },
    },
    {
      title: '待回收ip',
      dataIndex: 'iprelease',
      key:'iprelease',

    },
    {
      title: '备注信息',
      dataIndex: 'comment',
      key:'comment',

    },

  ]


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
      data = data.filter(item => item['ipaddress'].toLowerCase().includes(store.f_ip.toLowerCase()))
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
          dataSource={data}
          columns={this.columns}
          expandedRowRender={data => <p style={{ margin: 0 }}>{data.disk}</p>}
          scroll={{ x: '210%' }}
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
