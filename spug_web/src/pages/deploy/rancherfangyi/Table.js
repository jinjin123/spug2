/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table,  Tag,  message,Select,Tabs,Input,Modal } from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
import noticStore from '../notice/store';
import { SearchForm, AuthDiv, AuthCard,AuthButton } from 'components';
// import { Action } from "components";
const { Column } = Table;
const { TabPane } = Tabs;

@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loadings: [],
      moreAction: [{"id":0,"v":"更多操作...."}]
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

  onChange = (info, action,tag) => {
    console.log(info,action,tag);
    switch(tag){
      case 1:
        switch(action){
          case "cmap":
            store.cmaprecord = info;
            store.cmpForm = true;
            console.log(action)
            break;;
          case "svc":
            break;;
          case "pvc":
            break;;
        }
        break;
      
      case 2:
        switch(action){
          case "cmap":
            // store.cmaprecord = info;
            // store.cmpForm = true;
            this.setState({loading: true});
            Modal.confirm({
              title: '删除确认',
              content: `确定要删除【${info['configName']}】?`,
              onOk: () => {
                return http.delete('/api/app/deploy/cmapop/', {params: {id: info.id, env: 2}})
                  .then(() => {
                    message.success('删除成功');
                    store.fetchRecords()
                  })
              }
            })
            console.log(action)
            break;;
          case "svc":
            break;;
          case "pvc":
            this.setState({loading: true});
            Modal.confirm({
              title: '删除确认',
              content: `确定要删除【${info['pvcname']}】?`,
              onOk: () => {
                return http.delete('/api/app/deploy/pvcop/', {params: {id: info.id, env: 2}})
                  .then(() => {
                    message.success('删除成功');
                    store.fetchRecords()
                  })
              }
            })
            console.log(info.id)
            break;;
        }
        break;
      ;
      case 3:
        ;;
      case 4:
        break;
        ;;
      case 5:
        this.setState({
          moreAction : [{"id": info.id,"v":"申请发布"}]
        })
        store.addRancherVisible = true;
        store.record = info;
        setTimeout(() => {
          this.setState({
            moreAction : "更多操作...."
          })
        },1500)
        if ((noticStore.records).length === 0){
          noticStore.fetchRecords()
        }
        break;
          ;;
      case 6:
        break;;
      case 7:
        this.setState({
          moreAction : [{"id": info.id,"v":"历史版本"}]

        })
        store.historyVisible = true;
        setTimeout(() => {
          this.setState({
            moreAction : "更多操作...."
          })
        },1500)
        http.get('/api/app/deploy/svc/hsversion/' + info.id+ "/")
        .then((data) => store.versiontmp = data.data)
        .finally(() => store.isFetching = false)
        break;;

    }

  };
  render() {
    const {loadings} = this.state
    const {Option } = Select
    let data = store.records;
    let cmapdata =store.cmaprecords;
    let pvcdata = store.pvcrecords;
    if (store.topproject) {
      data = data.filter(item => item['top_project'].toLowerCase().includes(store.topproject.toLowerCase()))
    }
    if (store.rj) {
      data = data.filter(item => item['pjname'].toLowerCase().includes(store.rj.toLowerCase()))
    }
    // if (store.ns) {
    //   data = data.filter(item => item['namespace'].toLowerCase().includes(store.ns.toLowerCase()))
    // }
    if (store.project) {
      data = data.filter(item => item['project'].toLowerCase().includes(store.project.toLowerCase()))
    }
    if (store.app) {
      data = data.filter(item => item['dpname'].toLowerCase().includes(store.app.toLowerCase()))
    }
    if(store.cmapsearch) {
      cmapdata = cmapdata.filter(item => item['configName'].toLowerCase().includes(store.cmapsearch.toLowerCase()))
    }
    if(store.pvcsearch) {
      pvcdata = pvcdata.filter(item => item['pvcname'].toLowerCase().includes(store.pvcsearch.toLowerCase()))
    }
    // if (store.envname) {
    //   data = data.filter(item => item['envname'].toLowerCase().includes(store.envname.toLowerCase()))
    // }
    // if (store.volume) {
    //   data = data.filter(item => item['volumes'].toLowerCase().includes(store.volume.toLowerCase()))
    // }
    return (  
      <Tabs >
        <TabPane tab="服务列表" key="1">
            <Table
            rowKey="id"
            loading={store.isFetching}
            dataSource={data}
            scroll={{ x: '110%' }}
            expandedRowRender={data => <a href={data.verifyurl} target="_blank" style={{ margin: 0 }}>{data.verifyurl}</a>}
            pagination={{
              showSizeChanger: true,
              showLessItems: true,
              hideOnSinglePage: true,
              showTotal: total => `共 ${total} 条`,
              pageSizeOptions: ['10', '20', '50', '100']
            }}>
              <Column title="实体项目" dataIndex="top_project"/>
              <Column title="rancher细分项目" dataIndex="pjname"/>
              <Column title="命名空间" dataIndex="nsname"/>
              <Column title="应用" dataIndex="dpname"/>
              <Column title="镜像" dataIndex="img" width={300}/>
              {/* <Column title="环境" dataIndex="envname"/> */}
              <Column title="配置映射卷" dataIndex="configName"/>
              {/* <Column title="挂载卷详情" dataIndex="volumes_detail" width={200} ellipsis={{"showTitle":false}} /> */}
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
              {/* <Column title="暴露服务信息" dataIndex="pubsvc" width={200} ellipsis={{"showTitle":false}} /> */}
              <Column title="副本" dataIndex="replica"/>
              <Column title="创建人" dataIndex="create_by"/>
              <Column title="创建时间" dataIndex="create_time"/>

              {hasPermission('deploy.rancher.edit|deploy.rancher.del') && (
                <Column title="操作" fixed="right" render={info => (
                  <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." }  onChange={this.onChange.bind(this,info,"svc")}  style={{ width: 100 }} >
                    {/* <Option value={1}>编辑</Option> */}
                    {/* <Option value={2}>删除</Option> */}
                    {/* <Option value={3}>伸缩</Option> */}
                    {/* <Option value={4}>终端</Option> */}
                    <Option value={5}>申请发布</Option>
                    {/* <Option value={6}>重新部署</Option> */}
                    <Option value={7}>历史版本</Option>

                  </Select>
                  
                )}/>
              )}
          </Table>
        </TabPane>
        <TabPane tab="配置映射" key="2">
          <AuthCard auth="deploy.rancher.view">
                <SearchForm>
                  <SearchForm.Item span={4} style={{textAlign: 'left'}}>
                    <AuthButton auth="deploy.rancher.edit_config" 
                                type="primary" icon="plus" onClick={() => store.showAddCmpForm()}>添加配置映射</AuthButton>
                  </SearchForm.Item>
                  <SearchForm.Item span={4} title="配置映射文件名">
                    <Input  style={{width: 200, position: "absolute"}} allowClear value={store.cmapsearch} onChange={e => store.cmapsearch = (e.target.value).trim()} placeholder="请输入"/>
                  </SearchForm.Item>
              </SearchForm>
            </AuthCard>
          <Table
              rowKey="id"
              loading={store.isFetching}
              dataSource={cmapdata}
              scroll={{ x: '100%' }}
              expandedRowRender={cmapdata => <a href={cmapdata.verifyurl} target="_blank" style={{ margin: 0 }}>{cmapdata.verifyurl}</a>}
              pagination={{
                showSizeChanger: true,
                showLessItems: true,
                hideOnSinglePage: true,
                showTotal: total => `共 ${total} 条`,
                pageSizeOptions: ['10', '20', '50', '100']
              }}>
                <Column title="配置卷名称" dataIndex="configName"/>
                <Column title="命名空间" dataIndex="nsname"/>
                <Column title="创建人" dataIndex="create_by"/>
                <Column title="创建时间" dataIndex="create_time"/>

                {hasPermission('deploy.rancher.edit|deploy.rancher.del') && (
                  <Column title="操作" fixed="right" render={info => (          
                    <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." }  onChange={this.onChange.bind(this,info,"cmap")}  style={{ width: 100 }} >
                      <Option value={1}>编辑</Option>
                      <Option value={2}>删除</Option>
                    </Select>
                  )}/>
                )}
            </Table>
        </TabPane>
        <TabPane tab="PVC" key="3">
            <AuthCard auth="deploy.rancher.view">
                <SearchForm>
                  <SearchForm.Item span={4} style={{textAlign: 'left'}}>
                    <AuthButton auth="deploy.rancher.edit_config" 
                                type="primary" icon="plus" onClick={() => store.showAddPvcForm()}>添加 PVC</AuthButton>
                  </SearchForm.Item>
                  <SearchForm.Item span={4} title="pvc卷名">
                    <Input  style={{width: 200, position: "absolute"}} allowClear value={store.pvcsearch} onChange={e => store.pvcsearch = (e.target.value).trim()} placeholder="请输入"/>
                  </SearchForm.Item>
              </SearchForm>
            </AuthCard>
            <Table
              rowKey="id"
              loading={store.isFetching}
              dataSource={pvcdata}
              scroll={{ x: '100%' }}
              expandedRowRender={pvcdata => <a href={pvcdata.verifyurl} target="_blank" style={{ margin: 0 }}>{pvcdata.verifyurl}</a>}
              pagination={{
                showSizeChanger: true,
                showLessItems: true,
                hideOnSinglePage: true,
                showTotal: total => `共 ${total} 条`,
                pageSizeOptions: ['10', '20', '50', '100']
              }}>
                <Column title="pvc名称" dataIndex="pvcname"/>
                <Column title="命名空间" dataIndex="nsname"/>
                <Column title="大小" dataIndex="capacity"/>
                <Column title="权限" dataIndex="accessMode"/>
                <Column title="pvid" dataIndex="volumeid"/>
                <Column title="存储类" dataIndex="storageid"/>
                <Column title="创建人" dataIndex="create_by"/>
                <Column title="创建时间" dataIndex="create_time"/>
                {hasPermission('deploy.rancher.edit|deploy.rancher.del') && (
                  <Column title="操作" fixed="right" render={info => (          
                    <Select value={info.id == this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "更多操作...." }  onChange={this.onChange.bind(this,info,"pvc")}  style={{ width: 100 }} >
                      {/* <Option value={1}>编辑</Option> */}
                      <Option value={2}>删除</Option>
                    </Select>
                  )}/>
                )}
            </Table>
        </TabPane>
      </Tabs>
    )
  }
}

export default ComTable
