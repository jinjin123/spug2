/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, message } from 'antd';
import ComForm from './Form';
import { http, hasPermission } from 'libs';
import store from './store';
import { Action } from "components";
import HistoryTable from './HisotryTable';
@observer
class ComTable extends React.Component {
  componentDidMount() {
    store.fetchRecords()
    // if (rsaggStore.records.length === 0) {
    //   rsaggStore.fetchRecords()
    // }
  }

  handleDelete = (text) => {
    Modal.confirm({
      title: '删除确认',
      content: `确定要删除【${text['name']}】?`,
      onOk: () => {
        return http.delete('/api/config/service/', {params: {id: text.id}})
          .then(() => {
            message.success('删除成功');
            store.fetchRecords()
          })
      }
    })
  };

  render() {
    let data = store.records;
    if (store.f_name) {
      data = data.filter(item => item['namespace'].toLowerCase().includes(store.f_name.toLowerCase()))
    }
    if (store.project) {
      data = data.filter(item => item['project'].toLowerCase().includes(store.project.toLowerCase()))
    }
    if (store.configname) {
      data = data.filter(item => item['configname'].toLowerCase().includes(store.configname.toLowerCase()))
    }
    if (store.envname) {
      data = data.filter(item => item['envname'].toLowerCase().includes(store.envname.toLowerCase()))
    }
    return (
      <React.Fragment>
        <Table
          rowKey="id"
          loading={store.isFetching}
          dataSource={data}
          pagination={{
            showSizeChanger: true,
            showLessItems: true,
            hideOnSinglePage: true,
            showTotal: total => `共 ${total} 条`,
            pageSizeOptions: ['10', '20', '50', '100']
          }}>
          <Table.Column title="序号" key="series" render={(_, __, index) => index + 1}/>
          <Table.Column title="所属项目" dataIndex="project"/>
          <Table.Column title="命名空间" dataIndex="namespace"/>
          <Table.Column title="数据卷名" dataIndex="configname"/>
          <Table.Column title="键" dataIndex="configMap_k"/>
          <Table.Column title="环境" dataIndex="envname"/>
          <Table.Column title="创建人" dataIndex="create_by"/>
          {hasPermission('config.src.edit|config.src.del|config.src.view_config') && (
            <Table.Column title="操作" render={info => (
              <Action>
                <Action.Button auth="config.src.edit" onClick={() => store.showForm(info,false)}>编辑</Action.Button>
                <Action.Button auth="config.src.del" onClick={() => this.handleDelete(info)}>删除</Action.Button>
                <Action.Button auth="config.src.edit" onClick={() => store.showHistory(info)}>版本</Action.Button>
                {/* <Action.Link auth="config.src.view_config" to={`/config/setting/src/${info.id}`}>配置</Action.Link> */}
              </Action>
            )}/>
          )}
        </Table>
        {store.formVisible && <ComForm/>}
        {store.historyVisible && <HistoryTable/>}
      </React.Fragment>
    )
  }
}

export default ComTable
