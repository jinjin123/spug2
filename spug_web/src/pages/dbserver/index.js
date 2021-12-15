/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button, Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import ComTable from './Table';
import store from './store';
export default observer(function () {
  return (
    <AuthCard auth="host.host.view">
      <SearchForm>
        <SearchForm.Item span={6} title="实体项目">
            <Select allowClear autoClearSearchValue placeholder="请选择" value={store.tpjj} onChange={v => store.tpjj = v} mode="multiple">
              {store.pj.map(item => (
                item.tag === "实体项目" ? 
                <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                :null
              ))}
            </Select>
          </SearchForm.Item>

          <SearchForm.Item span={6} title="项目子类">
            <Select allowClear placeholder="请选择" value={store.chjj} onChange={v => store.chjj = v} mode="multiple">
              {store.pj.map(item => (
                item.tag === "项目子类" ? 
                <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                :null
              ))}
            </Select>
          </SearchForm.Item>

        <SearchForm.Item span={5} title="资源类别">
          <Select allowClear placeholder="请选择" value={store.f_zone} onChange={v => store.f_zone = v} mode="multiple">
            {store.zz.map(item => (
               (item.name).includes("数据库")?
              <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
              :null
            ))}
          </Select>
        </SearchForm.Item>
        <SearchForm.Item span={4} title="系统类型">
          <Select allowClear placeholder="请选择" value={store.otp} onChange={v => store.otp = v}>
            {store.ostp.map(item => (
              <Select.Option value={item} key={item}>{item}</Select.Option>
            ))}
          </Select>
          </SearchForm.Item>

          {/* <SearchForm.Item span={4} title="资源类型">
          <Select allowClear placeholder="请选择" value={store.rtp} onChange={v => store.rtp = v} >
            {store.rset.map(item => (
              <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
            ))}
          </Select>
          </SearchForm.Item> */}
        <SearchForm.Item span={4} title="设备位置">
          <Select allowClear placeholder="请选择" value={store.pvd} onChange={v => store.pvd = v}>
            {store.dvpo.map(item => (
              <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item>
        <SearchForm.Item span={6} title="所属集群">
          <Select allowClear autoClearSearchValue placeholder="请选择" value={store.csst} onChange={v => store.csst = v} mode="multiple" >
            {store.cs.map(item => (
              <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item>
        <SearchForm.Item span={4} title="所属区域">
          <Select allowClear autoClearSearchValue placeholder="请选择" value={store.wzz} onChange={v => store.wzz = v}  >
            {store.wz.map(item => (
              <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item>
        {/* <SearchForm.Item span={6} title="运营商">
          <Select allowClear placeholder="请选择" value={store.pvd} onChange={v => store.pvd = v}>
            {store.provider.map(item => (
              <Select.Option value={item} key={item}>{item}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item>

        <SearchForm.Item span={6} title="系统类型">
          <Select allowClear placeholder="请选择" value={store.otp} onChange={v => store.otp = v}>
            {store.ostp.map(item => (
              <Select.Option value={item} key={item}>{item}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item>
        <SearchForm.Item span={6} title="资产类型">
          <Select allowClear placeholder="请选择" value={store.rtp} onChange={v => store.rtp = v}>
            {store.res_t.map(item => (
              <Select.Option value={item} key={item}>{item}</Select.Option>
            ))}
          </Select>
        </SearchForm.Item> */}

        {/* <SearchForm.Item span={6} title="主机别名">
          <Input allowClear value={store.f_name} onChange={e => store.f_name = e.target.value} placeholder="请输入"/>
        </SearchForm.Item> */}
        <SearchForm.Item span={4} title="IP">
          <Input allowClear value={store.f_ip} onChange={e => store.f_ip = e.target.value} placeholder="请输入"/>
        </SearchForm.Item>
        <SearchForm.Item span={6}>
          <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
        </SearchForm.Item>
      </SearchForm>
      <AuthDiv auth="host.host.add" style={{marginBottom: 16}}>
        <Button type="primary" icon="plus" onClick={() => store.showForm()}>新建</Button>
        <Button  style={{marginLeft: 20}} type="primary" onClick={()=> store.downExcel()}icon="download" >导出</Button>
        <Button style={{marginLeft: 20}} type="primary" icon="import"
                onClick={() => store.importVisible = true}>批量导入</Button>
{/* 
        <Button style={{marginLeft: 20}} type="primary" icon="lock"
                        >批量改密</Button> */}
      </AuthDiv>
      <ComTable/>
    </AuthCard>
  )
})
