/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button,Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard,AuthButton } from 'components';
import ComTable from './Table';
import store from './store';
import DeployForm from './DeployForm';
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
            {/* <SearchForm.Item span={4} title="关联数据卷">
              <Input allowClear value={store.volume} onChange={e => store.volume = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item> */}
            {/* <SearchForm.Item span={3} title="环境">
              <Input allowClear value={store.envname} onChange={e => store.envname = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item> */}
            <SearchForm.Item span={4} style={{textAlign: 'right'}}>
              <AuthButton auth="deploy.rancher.edit_config" 
                          type="primary" icon="plus" onClick={() => store.showAddForm()}>部署服务</AuthButton>
            </SearchForm.Item>
        </SearchForm>
        <ComTable/>
        {store.deployForm && <DeployForm/>}
        {store.addRancherVisible && <AddRancherSelect />}
        {store.ext2Visible &&  <Ext2Form />}
      </AuthCard>
    )
  }
}

export default Rancher