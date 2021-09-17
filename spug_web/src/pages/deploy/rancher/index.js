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

// export default observer(function () {
//   return (
//     <AuthCard auth="deploy.app.view">
//       {/* <SearchForm>
//         <SearchForm.Item span={6} title="应用名称">
//           <Input allowClear value={store.f_name} onChange={e => store.f_name = e.target.value} placeholder="请输入"/>
//         </SearchForm.Item>
//         <SearchForm.Item span={6} title="描述信息">
//           <Input allowClear value={store.f_desc} onChange={e => store.f_desc = e.target.value} placeholder="请输入"/>
//         </SearchForm.Item>
//         <SearchForm.Item span={8}>
//           <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
//         </SearchForm.Item>
//       </SearchForm> */}
//       {/* <AuthDiv auth="deploy.app.add" style={{marginBottom: 16}}>
//         <Button type="primary" icon="plus" onClick={() => store.showForm()}>新建</Button>
//       </AuthDiv> */}
//       <ComTable/>
//       {/* {store.formVisible && <ComForm />}
//       {store.addVisible && <AddSelect />}
//       {store.ext1Visible &&  <Ext1Form />}
//       {store.ext2Visible &&  <Ext2Form />} */}
//     </AuthCard>
//   )
// })

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
    if (nsStore.records.length === 0) {
      nsStore.fetchRecords()
    }
    if (confStore.records.length === 0) {
      confStore.fetchRecords()
    }
   
  }
 
  render(){
    return (
      <AuthCard auth="deploy.rancher.view">
          <SearchForm>
          <SearchForm.Item span={6} title="发布命名空间">
            <Select allowClear value={store.f_env_id} onChange={v => store.f_env_id = v} placeholder="请选择">
              {nsStore.records.map(item => (
                <Select.Option key={item.id} value={item.id}>{item.namespace}</Select.Option>
              ))}
            </Select>
          </SearchForm.Item>
          <SearchForm.Item span={6} title="配置映射文件">
            <Select allowClear value={store.f_app_id} onChange={v => store.f_app_id = v} placeholder="请选择">
              {confStore.records.map(item => (
                <Select.Option key={item.id} value={item.id}>{item.configid}</Select.Option>
              ))}
            </Select>
          </SearchForm.Item>
        </SearchForm>
        <ComTable/>
      </AuthCard>
    )
  }
}

export default Rancher