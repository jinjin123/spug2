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

import { Action } from "components";
const { Column } = Table;

@observer
class HistoryForm extends React.Component {
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
    let data = store.versiontmp;

    return (
        <Modal
        visible
        width={1000}
        style={{ float: 'right',top: 0}}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={'历史版本查看'}
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
              <Column title="实体项目" dataIndex="top_project"/>
              <Column title="rancher细分项目" dataIndex="pjname"/>
              <Column title="命名空间" dataIndex="nsname"/>
              <Column title="应用" dataIndex="dpname"/>
              <Column title="镜像" dataIndex="img" width={300}/>
              <Column title="配置映射卷" dataIndex="configName"/>
              {/* <Column
                title="状态"
                dataIndex="state"
                key="state"
                render={(state) => (
                  <Tag color={state === "active" ? "green":"volcano"} key={state}>
                  {state}
                </Tag>
                )}
              /> */}
              <Column title="副本" dataIndex="replica"/>
              <Column title="创建人" dataIndex="create_by"/>
              <Column title="创建时间" dataIndex="create_time"/>
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
export default Form.create()(HistoryForm)
