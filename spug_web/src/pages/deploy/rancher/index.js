/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button,Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import ComTable from './Table';
import ComForm from './Form';
import Ext1Form from './Ext1Form';
import Ext2Form from './Ext2Form';
import AddSelect from './AddSelect';
import store from './store';
import nsStore from 'pages/config/namespace/store';
import confStore from 'pages/config/configmap/store';

@observer
class Rancher extends  React.Component {
  constructor(props){
      super(props);
      this.state  =  {
        expire:undefined,
        count:''
      }
  }
  
  componentDidMount(){
    // if (nsStore.records.length === 0) {
    //   nsStore.fetchRecords()
    // }
    // if (confStore.records.length === 0) {
    //   confStore.fetchRecords()
    // }
   
  }
 
  render(){
    return (
      <AuthCard auth="deploy.rancher.view">
          <SearchForm>
          <SearchForm.Item span={4} title="项目">
              <Input allowClear value={store.project} onChange={e => store.project = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="命名空间">
              <Input allowClear value={store.ns} onChange={e => store.ns = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="应用">
              <Input allowClear value={store.app} onChange={e => store.app = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="关联数据卷">
              <Input allowClear value={store.volume} onChange={e => store.volume = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={3} title="环境">
              <Input allowClear value={store.envname} onChange={e => store.envname = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
        </SearchForm>
        <ComTable/>
      </AuthCard>
    )
  }
}

export default Rancher