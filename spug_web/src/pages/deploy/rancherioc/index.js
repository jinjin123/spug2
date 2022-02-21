/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input,Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard,AuthButton } from 'components';
import ComTable from './Table';
import store from './store';
import DeployForm from './DeployForm';
import PvcFrom from './PvcForm';
import CmpFrom from './CmpForm';
import HistoryForm from './HisotryForm';
import HistoryDetailForm from './HistoryDetailForm';
import RestartForm from './RestartForm';
import AddRancherSelect from './AddRancherSelect';
import Ext2Form from './Ext2Form';
@observer
class Rancher extends  React.Component {
  constructor(props){
      super(props);
      this.state  =  {
        expire:undefined,
        count:''
      }
  }
  
 
  render(){
    return (
      <AuthCard auth="deploy.rancher.view">
          <SearchForm>
            <SearchForm.Item span={8} title="实体项目" >
              <Select allowClear placeholder="请选择" style={{left:10}} value={store.topproject} onChange={v => store.topproject = v}>
                {store.toppj.map(item => (
                  <Select.Option value={item} key={item}>{item}</Select.Option>
                ))}
              </Select>
          </SearchForm.Item>
            <SearchForm.Item span={6} title="rancher细分项目">
              {/* <Input allowClear value={store.ns} onChange={e => store.ns = (e.target.value).trim()} placeholder="请输入"/> */}
              <Select allowClear placeholder="请选择" style={{left:10}} value={store.rj} onChange={v => store.rj = v}>
                {store.rancherpj.map(item => (
                  <Select.Option value={item} key={item}>{item}</Select.Option>
                ))}
              </Select>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="应用">
              <Input allowClear value={store.app} onChange={e => store.app = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} style={{textAlign: 'right'}}>
              <AuthButton auth="deploy.rancher.deploynew" 
                          type="primary" icon="plus" onClick={() => store.showAddForm()}>部署服务</AuthButton>
            </SearchForm.Item>
            <SearchForm.Item span={4} style={{textAlign: 'right'}}>
              <AuthButton type="primary" icon="sync" onClick={store.fetchRecords}>刷新</AuthButton>
            </SearchForm.Item>
        </SearchForm>
        <ComTable/>
        {store.historyDetailVisible && <HistoryDetailForm/>}
        {store.restartVisible && <RestartForm/>}

        {store.historyVisible && <HistoryForm/>}
        {store.deployForm && <DeployForm/>}
        {store.pvcForm && <PvcFrom/>}
        {store.cmpForm && <CmpFrom/>}
        {store.addRancherVisible && <AddRancherSelect />}
        {store.ext2Visible &&  <Ext2Form />}
      </AuthCard>
    )
  }
}

export default Rancher