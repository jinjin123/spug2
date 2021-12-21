/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, Icon, Popover, Tag, message } from 'antd';
import { http, hasPermission,formatDate } from 'libs';
import { Action } from "components";
import store from './store';


@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      loadings: [],
    }
  }

  componentDidMount() {
    store.fetchRecords()
  }
  enterLoading = (raw,index) => {
    console.log(raw)
    this.setState(({ loadings }) => {
      const newLoadings = [...loadings];
      newLoadings["load"] = true;
      newLoadings["id"] = raw.id;
      return {
        loadings: newLoadings,
      };
    });
    setTimeout(() => {
      this.setState(({ loadings }) => {
        const newLoadings = [...loadings];
        newLoadings["id"] = raw.id;

        const formData = { app_id: raw.app_id, app_name: raw.app_name, env_id : raw.env_id, deploy_id: raw.deploy_id};
        http.post('/api/deploy/request/rancher/publish',formData)
        .then(res => {
          message.success('发布成功');
          store.fetchRecords()
        })
        .finally(() => newLoadings["load"] = false)
        return {
          loadings: newLoadings,
        };
      });
    }, 4000);
  };
  columns = [{
    title: '申请标题',
    dataIndex: 'name',
  }, {
    title: '应用',
    dataIndex: 'app_name',
  }, {
    title: '发布环境',
    dataIndex: 'env_name',
  }, 
  // {
  //   title: '版本',
  //   render: info => {
  //     if (info['app_extend'] === '1') {
  //       const [type, ext1, ext2] = info.extra;
  //       if (type === 'branch') {
  //         return <React.Fragment>
  //           <Icon type="branches"/> {ext1}#{ext2.substr(0, 6)}
  //         </React.Fragment>
  //       } else {
  //         return <React.Fragment>
  //           <Icon type="tag"/> {ext1}
  //         </React.Fragment>
  //       }
  //     } else {
  //       return <React.Fragment>
  //         <Icon type="build"/> {info.extra[0]}
  //       </React.Fragment>
  //     }
  //   }
  // }, 
  {
    title: '状态',
    render: info => {
      if (info.status === '-1' && info.reason) {
        return <Popover title="驳回原因:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['status_alias']}</span>
        </Popover>
      } else if (info.status === '1' && info.reason) {
        return <Popover title="审核意见:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['status_alias']}</span>
        </Popover>
      } else if (info.status === '2') {
        return <Tag color="blue">{info['status_alias']}</Tag>
      } else if (info.status === '3') {
        return <Tag color="green">{info['status_alias']}</Tag>
      } else if (info.status === '-3') {
        return <Tag color="red">{info['status_alias']}</Tag>
      } else if (info.status === '1' ) {
        return <Tag color="magenta" >{info['status_alias']}</Tag>
      } else {
        return <Tag >{info['status_alias']}</Tag>

      }
    }
  }, 
  {
    title: '发布类型',
    dataIndex: 'type',
  },
  {
    title: '运维审核状态',
    // dataIndex: 'opsstatus',
    render: info => {
      if (info.opsstatus === -1 && info.reason) {
        return <Popover title="驳回原因:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['opsstatus_alias']}</span>
        </Popover>
      } else if (info.opsstatus === 1 && info.reason) {
        return <Popover title="审核意见:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['opsstatus_alias']}</span>
        </Popover>
      } else if (info.opsstatus === 2) {
        return <Tag color="blue">{info['opsstatus_alias']}</Tag>
      } else if (info.opsstatus === 3) {
        return <Tag color="green">{info['opsstatus_alias']}</Tag>
      } else if (info.opsstatus === -3) {
        return <Tag color="red">{info['opsstatus_alias']}</Tag>
      } else if (info.opsstatus === 1 ){
        return <Tag color="magenta">{info['opsstatus_alias']}</Tag>
      } else {
        return <Tag >{info['opsstatus_alias']}</Tag>

      }
    }
  },
  {
    title: '运维审核人',
    dataIndex: 'opshandler',
  },
  {
    title: '测试审核状态',
    // dataIndex: 'opsstatus',
    render: info => {
      if (info.teststatus === -1 && info.reason) {
        return <Popover title="驳回原因:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['teststatus_alias']}</span>
        </Popover>
      } else if (info.teststatus === 1 && info.reason) {
        return <Popover title="审核意见:" content={info.reason}>
          <span style={{color: '#1890ff'}}>{info['teststatus_alias']}</span>
        </Popover>
      } else if (info.teststatus === 2) {
        return <Tag color="blue">{info['teststatus_alias']}</Tag>
      } else if (info.teststatus === 3) {
        return <Tag color="green">{info['teststatus_alias']}</Tag>
      } else if (info.teststatus === -3) {
        return <Tag color="red">{info['teststatus_alias']}</Tag>
      } else if (info.teststatus === 1 ){
        return <Tag color="magenta">{info['teststatus_alias']}</Tag>
      } else {
        return <Tag >{info['teststatus_alias']}</Tag>

      }
    }
  },
  {
    title: '测试审核人',
    dataIndex: 'testhandler',
  },  
  {
    title: '申请人',
    dataIndex: 'created_by_user',
  }, {
    title: '申请时间',
    dataIndex: 'created_at',
    sorter: (a, b) => a['created_at'].localeCompare(b['created_at'])
  }, {
    title: '操作',
    className: hasPermission('deploy.request.do|deploy.request.edit|deploy.request.approve|deploy.request.del') ? null : 'none',
    render: info => {
      const {loadings} = this.state

      switch (info.status) {

        case '-3':
          return <Action>
            {info["pub_tag"] === '2'?  
                <Action>
                <Action.Button auth="deploy.request.do" loading={info.id == loadings["id"] ? loadings["load"] :false}  onClick={() =>this.enterLoading(info,2)} > rancher发布</Action.Button>
                <Action.Button
                auth="deploy.request.do"
                disabled={info.type === '2'}
                onClick={() => this.handleRollback(info)}>回滚</Action.Button>
                  <Action.Link
                  auth="deploy.request.view"
                  to={`/deploy/do/rancher/${info.id}/1`}>查看</Action.Link> 
                <Action.Button auth="deploy.request.view" onClick={() => store.showChange(info)}>查看变更</Action.Button>

                </Action>
                
            :  <Action.Link auth="deploy.request.do" to={`/deploy/do/ext${info['app_extend']}/${info.id}`}>主机发布</Action.Link>
            }
            {/* <Action.Button auth="deploy.request.del" onClick={() => this.handleDelete(info)}>删除</Action.Button> */}
          </Action>;
        case '3':
          return <Action>
            {info["pub_tag"] === '2'?  
                <Action>
                  <Action.Link
                  auth="deploy.request.view"
                  to={`/deploy/do/rancher/${info.id}/1`}>查看</Action.Link> 
                  <Action.Button auth="deploy.request.approve" onClick={() => store.showApprove(info,"测试")}>测试审核</Action.Button>
                  <Action.Button auth="deploy.request.view" onClick={() => store.showChange(info)}>查看变更</Action.Button>

                </Action>
              : <Action.Link
                auth="deploy.request.view"
                to={`/deploy/do/ext${info['app_extend']}/${info.id}/1`}>查看</Action.Link>
            }
                <Action.Button
                auth="deploy.request.do"
                disabled={info.type === '2'}
                onClick={() => this.handleRollback(info)}>回滚</Action.Button>
          </Action>;
        case '-1':
          return <Action>
            <Action.Button auth="deploy.request.edit" onClick={() => store.showForm(info)}>编辑</Action.Button>
            {/* <Action.Button auth="deploy.request.del" onClick={() => this.handleDelete(info)}>删除</Action.Button> */}
          </Action>;
        case '0':
          return <Action>
            <Action.Button auth="deploy.request.approve" onClick={() => store.showApprove(info,"运维")}>审核</Action.Button>
            <Action.Button auth="deploy.request.view" onClick={() => store.showChange(info)}>查看变更</Action.Button>
            {/* <Action.Button auth="deploy.request.del" onClick={() => this.handleDelete(info)}>删除</Action.Button> */}
          </Action>;
        case '1':
          // const {loadings} = this.state
          return <Action>
            {info["pub_tag"] === '2'?  
                <Action>
                              <Action.Button auth="deploy.request.view" onClick={() => store.showChange(info)}>查看变更</Action.Button>
                  <Action.Button auth="deploy.request.do" loading={info.id == loadings["id"] ? loadings["load"] :false}  onClick={() =>this.enterLoading(info,2)} > rancher发布</Action.Button>
                  {/* <Action.Button
                    auth="deploy.request.do"
                    disabled={info.type === '2'}
                    onClick={() => this.handleRollback(info)}>回滚</Action.Button> */}
                </Action>
            :  <Action.Link auth="deploy.request.do" to={`/deploy/do/ext${info['app_extend']}/${info.id}`}>主机发布</Action.Link>
            }
            {/* <Action.Button auth="deploy.request.del" onClick={() => this.handleDelete(info)}>删除</Action.Button> */}
          </Action>;
        case '2':
          return <Action>
            <Action.Link
              auth="deploy.request.view"
              to={`/deploy/do/ext${info['app_extend']}/${info.id}/1`}>查看</Action.Link>
          </Action>;
        default:
          return null
      }
    }
  }];
  rowSelection = {
    onChange: (selectedRowKeys, selectedRows) => {
      console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    },
    getCheckboxProps: record => ({
      
    }),
  };

  handleRollback = (info) => {
    console.log(info)
    this.setState({loading: true});
    store.tmp_rollid = info.app_id
    let rivision = []
    let t
    return http.get('/api/app/svc/rollback/'+ info.app_id +'/')
    .then(({data})=>{
      data.map((item)=>(
        t = formatDate(item["createdTS"],"yyyy-MM-dd hh:mm"),
        rivision.push({"id":item["id"], "time":item["id"]+" "+ (t),"tag":item["createdTS"]})
      ))
      console.log(rivision)
    })
    .finally(() => (
      this.isLoading = false,
      store.rollbackv = rivision.sort((a,b)=> b.tag-a.tag),
      store.rollVisible = true
    ))
    // http.put('/api/deploy/request/', {id: info.id, action: 'check'})
    //   .then(res => {
    //     Modal.confirm({
    //       title: '回滚确认',
    //       content: `确定要回滚至 ${res['date']} 创建的名称为【${res['name']}】的发布申请版本?`,
    //       onOk: () => {
    //         return http.put('/api/deploy/request/', {id: info.id, action: 'do'})
    //           .then(() => {
    //             message.success('回滚申请创建成功');
    //             store.fetchRecords()
    //           })
    //       }
    //     })
    //   })
    //   .finally(() => this.setState({loading: false}))
  };

  handleDelete = (info) => {
    Modal.confirm({
      title: '删除确认',
      content: `确定要删除【${info['name']}】?`,
      onOk: () => {
        return http.delete('/api/deploy/request/', {params: {id: info.id}})
          .then(() => {
            message.success('删除成功');
            store.fetchRecords()
          })
      }
    })
  };

  render() {
    let data = store.records;
    if (store.f_app_id) {
      data = data.filter(item => item['app_id'] === store.f_app_id)
    }
    if (store.f_env_id) {
      data = data.filter(item => item['env_id'] === store.f_env_id)
    }
    if (store.f_s_date) {
      data = data.filter(item => {
        const date = item['created_at'].substr(0, 10);
        return date >= store.f_s_date && date <= store.f_e_date
      })
    }
    if (store.f_status !== 'all') {
      if (store.f_status === '99') {
        data = data.filter(item => ['-1', '2'].includes(item['status']))
      } else {
        data = data.filter(item => item['status'] === store.f_status)
      }
    }
    return (
      <Table
        rowKey="id"
        rowSelection={this.rowSelection}
        expandedRowRender={data => <p style={{ margin: 0 }}>{data.desccomment}</p>}
        loading={store.isFetching}
        dataSource={data}
        pagination={{
          showSizeChanger: true,
          showLessItems: true,
          hideOnSinglePage: true,
          showTotal: total => `共 ${total} 条`,
          pageSizeOptions: ['10', '20', '50', '100']
        }}
        columns={this.columns}/>
    )
  }
}

export default ComTable
