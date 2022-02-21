/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import {observer} from 'mobx-react';
import {Table, Divider, Modal, Badge, message, Form, Input} from 'antd';
import {LinkButton} from 'components';
import ComForm from './Form';
import http from 'libs/http';
import store from './store';

@observer
class ComTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      password: ''
    }
  }
  componentDidMount() {
    store.fetchRecords()
  }

  columns = [{
    title: '序号',
    key: 'series',
    render: (_, __, index) => index + 1,
    width: 80
  }, {
    title: '实体项目',
    dataIndex: 'top_project',
  }, {
    title: 'rancher细分项目',
    dataIndex: 'pjname',
  }, {
    title: '命名空间',
    dataIndex: 'nsname',
  }, 
  {
    title: '应用',
    dataIndex: 'dpname'
  }, {
    title: '用户名',
    dataIndex: 'nickname',
  }, {
    title: '邮箱',
    dataIndex: 'email',
  }, 
  {
    title: '操作',
    render: info => (
      <span>
        {/* <LinkButton onClick={() => this.handleActive(info)}>{info['is_active'] ? '禁用' : '启用'}</LinkButton> */}
        {/* <Divider type="vertical"/> */}
        {/* <LinkButton onClick={() => store.showForm(info)}>编辑</LinkButton> */}
        {/* <Divider type="vertical"/> */}
        {/* <LinkButton disabled={info['type'] === 'ldap'} onClick={() => this.handleReset(info)}>重置密码</LinkButton> */}
        {/* <Divider type="vertical"/> */}
        <LinkButton onClick={() => this.handleDelete(info)}>删除</LinkButton>
      </span>
    )
  }];

  // handleActive = (text) => {
  //   Modal.confirm({
  //     title: '操作确认',
  //     content: `确定要${text['is_active'] ? '禁用' : '启用'}【${text['nickname']}】?`,
  //     onOk: () => {
  //       return http.patch(`/api/account/user/`, {id: text.id, is_active: !text['is_active']})
  //         .then(() => {
  //           message.success('操作成功');
  //           store.fetchRecords()
  //         })
  //     }
  //   })
  // };

  // handleReset = (info) => {
  //   Modal.confirm({
  //     icon: 'exclamation-circle',
  //     title: '重置登录密码',
  //     content: <Form>
  //       <Form.Item required label="重置后的新密码">
  //         <Input.Password onChange={val => this.setState({password: val.target.value})}/>
  //       </Form.Item>
  //     </Form>,
  //     onOk: () => {
  //       return http.patch('/api/account/user/', {id: info.id, password: this.state.password})
  //         .then(() => message.success('重置成功', 0.5))
  //     },
  //   })
  // };

  handleDelete = (text) => {
    Modal.confirm({
      title: '删除确认',
      content: `确定要删除【${text['nickname']}】?`,
      onOk: () => {
        return http.delete('/api/app/deploy/svc/notice', {params: {id: text.id}})
          .then(() => {
            message.success('删除成功');
            store.fetchRecords()
          })
      }
    })
  };

  render() {
    let data = store.records;
    if (store.topproject) {
      data = data.filter(item => item['top_project'].toLowerCase().includes(store.topproject.toLowerCase()))
    }
    if (store.rj) {
      data = data.filter(item => item['pjname'].toLowerCase().includes(store.rj.toLowerCase()))
    }
    if (store.app) {
      data = data.filter(item => item['dpname'].toLowerCase().includes(store.app.toLowerCase()))
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
          }}
          columns={this.columns}/>
        {store.formVisible && <ComForm/>}
      </React.Fragment>
    )
  }
}

export default ComTable
