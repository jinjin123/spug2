/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, Tag, Icon, Divider, message,Select,Radio } from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
import { Action } from "components";
const { Column } = Table;
@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loadings: [],
    };
  
  }

  componentDidMount() {
    store.fetchRecords();
  }
  enterLoading = (raw,index) => {
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

        const formData = { project_id: raw.project_id, deployid: raw.deployid, env_id : raw.env_id};
        http.post('/api/app/deploy/svc',formData)
        .then(res => {
          message.success('重新部署成功');

        })
        .finally(() => newLoadings["load"] = false)
        return {
          loadings: newLoadings,
        };
      });
    }, 4000);
  };

  onChange = (info, action) => {
    console.log(info,action);
    switch(action){
      case 1:
        break;
        ;;
      case 2:
        break;
      ;;
      case 3:
        ;;
      case 4:
        break;
        ;;
      case 5:
        
        store.addRancherVisible = true;
        store.record = info;
        break;
          ;;
    }

  };
  render() {
    const {loadings} = this.state
    const {Option } = Select
    let data = store.records;
    if (store.ns) {
      data = data.filter(item => item['namespace'].toLowerCase().includes(store.ns.toLowerCase()))
    }
    if (store.project) {
      data = data.filter(item => item['project'].toLowerCase().includes(store.project.toLowerCase()))
    }
    if (store.app) {
      data = data.filter(item => item['deployname'].toLowerCase().includes(store.app.toLowerCase()))
    }
    if (store.envname) {
      data = data.filter(item => item['envname'].toLowerCase().includes(store.envname.toLowerCase()))
    }
    if (store.volume) {
      data = data.filter(item => item['volumes'].toLowerCase().includes(store.volume.toLowerCase()))
    }
    return (      
      <Table
        rowKey="id"
        loading={store.isFetching}
        dataSource={data}
        scroll={{ x: '110%' }}
        pagination={{
          showSizeChanger: true,
          showLessItems: true,
          hideOnSinglePage: true,
          showTotal: total => `共 ${total} 条`,
          pageSizeOptions: ['10', '20', '50', '100']
        }}>
          <Column title="所属项目" dataIndex="project"/>
          <Column title="命名空间" dataIndex="namespace"/>
          <Column title="应用" dataIndex="deployname"/>
          <Column title="镜像" dataIndex="img" width={300}/>
          <Column title="环境" dataIndex="envname"/>
          <Column title="关联卷" dataIndex="volumes"/>
          <Column title="挂载卷详情" dataIndex="volumes_detail" width={200} ellipsis={{"showTitle":false}} />
          <Column
            title="状态"
            dataIndex="state"
            key="state"
            render={(state) => (
              <Tag color={state === "active" ? "green":"volcano"} key={state}>
              {state}
            </Tag>
            )}
          />
          <Column title="暴露服务信息" dataIndex="pubsvc" width={200} ellipsis={{"showTitle":false}} />
          <Column title="副本" dataIndex="replica"/>
          <Column title="创建人" dataIndex="create_by"/>
          {hasPermission('deploy.rancher.edit|deploy.rancher.del') && (
            <Column title="操作" fixed="right" render={info => (
              // <Action>
              //   <Action.Button auth="deploy.src.edit" loading={info.id == loadings["id"] ? loadings["load"] :false}  onClick={() =>this.enterLoading(info,2)}>重新部署</Action.Button>
              //   <Action.Button auth="deploy.src.del" >回滚</Action.Button>
              //   <Action.Button auth="deploy.src.edit" >伸缩</Action.Button>
              //   <Action.Button auth="deploy.src.edit" >终端</Action.Button>
              // </Action>
              
              <Select defaultValue="更多操作..." onChange={this.onChange.bind(this,info)}  style={{ width: 100 }} >
                <Option value={1}>重新部署</Option>
                <Option value={2}>回滚</Option>
                <Option value={3}>伸缩</Option>
                <Option value={4}>终端</Option>
                <Option value={5}>发布</Option>
              </Select>
              
            )}/>
          )}
      </Table>
    )
  }
}

export default ComTable
