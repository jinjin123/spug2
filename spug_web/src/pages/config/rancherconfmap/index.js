/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button,Modal } from 'antd';
import { SearchForm, AuthButton, AuthCard } from 'components';
import ComTable from './Table';
import store from './store';
import envStore from '../environment/store';
@observer
class RancherConfigMap extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      view: '1'
    }

  }
  componentDidMount() {
    if (envStore.records.length === 0) {
      envStore.fetchRecords().then(() => {
        if (envStore.records.length === 0) {
          Modal.error({
            title: '无可用环境',
            content: <div>配置依赖应用的运行环境，请在 <a href="/config/environment">环境管理</a> 中创建环境。</div>
          })
        } else {
          this.updateEnv()
        }
      })
    } else {
      this.updateEnv()
    }
  }

  updateEnv = (env) => {
    store.env = env || envStore.records[0] || {};
  };

  render(){
      const {view} = this.state;
      return (
        <AuthCard auth="config.rancher.view">
          <SearchForm>
            <SearchForm.Item span={4} title="项目">
              <Input allowClear value={store.project} onChange={e => store.project = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="命名空间">
              <Input allowClear value={store.f_name} onChange={e => store.f_name = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={4} title="数据卷名">
              <Input allowClear value={store.configname} onChange={e => store.configname = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
            <SearchForm.Item span={2}>
              <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
            </SearchForm.Item>
            <SearchForm.Item span={4} style={{textAlign: 'right'}}>
              <AuthButton auth="config.app.edit_config|config.service.edit_config" disabled={view !== '1'}
                          type="primary" icon="plus" onClick={() => store.showAddForm()}>新增配置</AuthButton>
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
