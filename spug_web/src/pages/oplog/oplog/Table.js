/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Table, Modal, Tag, message } from 'antd';
import { Action } from 'components';
import { http, hasPermission } from 'libs';
import store from './store';

@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);

  }

  componentDidMount() {
    store.fetchRecords();

  }



  render() {
    let data = store.records;

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
          <Table.Column title="操作内容" dataIndex="content"/>
          <Table.Column title="操作" dataIndex="action"/>
          <Table.Column title="创建时间" dataIndex="create_time"/>
          <Table.Column title="操作人" dataIndex="opuser"/>

        </Table>
      </React.Fragment>
    )
  }
}

export default ComTable
