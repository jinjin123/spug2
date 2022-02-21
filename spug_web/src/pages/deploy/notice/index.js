/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Select, Button } from 'antd';
import { SearchForm, AuthCard } from 'components';
import ComTable from './Table';
import store from './store';

export default observer(function () {
  return (
    <AuthCard auth="system.account.view">
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
            <SearchForm.Item span={8} title="应用">
              <Input allowClear value={store.app} onChange={e => store.app = (e.target.value).trim()} placeholder="请输入"/>
            </SearchForm.Item>
        <SearchForm.Item span={5} title="账户名称">
          <Input allowClear value={store.f_name} onChange={e => store.f_name = e.target.value} placeholder="请输入"/>
        </SearchForm.Item>
        <SearchForm.Item span={8}>
          <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
        </SearchForm.Item>
      </SearchForm>
      <div style={{marginBottom: 16}}>
        <Button type="primary" icon="plus" onClick={() => store.showForm()}>新建</Button>
      </div>
      <ComTable/>
    </AuthCard>
  )
})
