/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Table} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
import ComForm from './Form';
import './form.css';
import { Action } from "components";
@observer
class HistoryConfig extends React.Component {
  // componentDidMount() {
  //   historystore.fetchRecords();
  // }

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
    let data = store.vrecords;
    // if (historystore.f_name) {
    //   data = data.filter(item => item['namespace'].toLowerCase().includes(historystore.f_name.toLowerCase()))
    // }
    return (
        <Modal
        visible
        width={800}
        style={{ float: 'right',top: 0}}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.record.id ? '历史版本查看' : '新增配置'}
        onCancel={() => store.historyVisible = false}
        onOk={() => store.historyVisible = false}
        >
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
            <Table.Column title="命名空间" dataIndex="namespace"/>
            <Table.Column title="配置文件" dataIndex="configname"/>
            <Table.Column title="创建时间" dataIndex="create_time"/>
            {/* <Table.Column title="配置文件id" dataIndex="configid"/> */}
            {hasPermission('config.src.edit|config.src.del|config.src.view_config') && (
              <Table.Column title="操作" render={info => (
                <Action>
                  <Action.Button auth="config.src.edit" onClick={() => store.showForm(info,true)}>编辑</Action.Button>
                  <Action.Button auth="config.src.del" onClick={() => this.handleDelete(info)}>删除</Action.Button>
                  {/* <Action.Button auth="config.src.edit" onClick={() => store.showHistory(info)}>版本</Action.Button> */}
                  {/* <Action.Link auth="config.src.view_config" to={`/config/setting/src/${info.id}`}>配置</Action.Link> */}
                </Action>
              )}/>
            )}
          </Table>
        </Modal>
    )
  }
}
export default Form.create()(HistoryConfig)
