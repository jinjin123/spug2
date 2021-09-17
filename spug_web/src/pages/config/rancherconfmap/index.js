/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button,Modal } from 'antd';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import ComTable from './Table';
import store from './store';
import envStore from '../environment/store';
@observer
class RancherConfigMap extends React.Component{
  constructor(props) {
    super(props);

  }
  componentDidMount() {
    if (envStore.records.length === 0) {
      envStore.fetchRecords().then(() => {
        if (envStore.records.length === 0) {
          Modal.error({
            title: '无可用环境',
            content: <div>配置依赖应用的运行环境，请在 <a href="/config/environment">环境管理</a> 中创建环境。</div>
          })
        } 
      })
    } 
  }

  render(){
      return (
        <AuthCard auth="config.rancher.view">
          <SearchForm>
            <SearchForm.Item span={8} title="命名空间名称">
              <Input allowClear value={store.f_name} onChange={e => store.f_name = e.target.value} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={8}>
              <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
            </SearchForm.Item>
          </SearchForm>
          {/* <AuthDiv auth="config.src.add" style={{marginBottom: 16}}>
            <Button type="primary" icon="plus" onClick={() => store.showForm()}>新建</Button>
          </AuthDiv> */}
          <ComTable/>
        </AuthCard>
      )
    }
    
}

export default RancherConfigMap
