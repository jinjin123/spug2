/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Select, Input, message, Col } from 'antd';
import http from 'libs/http';
import store from './store';

import svcstore from '../rancherioc/store';
import userStore from 'pages/system/account/store';
import { Link } from "react-router-dom";
import { SearchForm, AuthCard } from 'components';
@observer
class ComForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false
    }
  }

  componentDidMount() {
    if (userStore.records.length === 0) {
      userStore.fetchRecords()
    } 
    if (svcstore.records.length === 0) {
      svcstore.fetchRecords()
    } 
  }

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = {
      "tj": store.topproject,
      "ns": store.ns,
      "rj":store.rj,
      "app": store.app,
      "us": store.user
    }
    let request;
    if (store.record.id) {
      formData['id'] = store.record.id;
      request = http.patch('/api/app/deploy/svc/notice', formData)
    } else {
      request = http.post('/api/app/deploy/svc/notice', formData)
    }
    request.then(() => {
      message.success('操作成功');
      store.formVisible = false;
      store.fetchRecords()
    }, () => this.setState({loading: false}))
  };

  render() {
    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title={store.record.id ? '编辑账户' : '新建应用发布审核通知关联账户'}
        onCancel={() => store.formVisible = false}
        confirmLoading={this.state.loading}
        onOk={this.handleSubmit}>
        <Form labelCol={{span: 6}} wrapperCol={{span: 18}}>
          <Form.Item required label="实体项目">
            <Col span={16}>
              <Select   placeholder="请选择" value={store.topproject} onChange={v => store.topproject = v}>
                {svcstore.toppj.map((item,index) => (
                  <Select.Option  value={item} key={index}>{item}</Select.Option>
                ))}
              </Select>
            </Col>
          </Form.Item>
          <Form.Item required label="rancher细分项目" >
            <Col span={16}>
              <Select   placeholder="请选择" value={store.rj} onChange={v => store.rj = v}>
                {svcstore.rancherpj.map((item,index) => (
                  <Select.Option  value={item} key={index}>{item}</Select.Option>
                ))}
              </Select>
            </Col>
          </Form.Item>
          <Form.Item required label="命名空间" >
            <Col span={16}>
              <Select   placeholder="请选择" value={store.ns} onChange={v => store.ns = v}>
                {svcstore.nsname.map((item,index) => (
                  <Select.Option  value={item} key={index}>{item}</Select.Option>
                ))}
              </Select>
            </Col>
          </Form.Item>
          <Form.Item required label="应用" >
            <Col span={16}>
              <Select   placeholder="请选择" value={store.app} onChange={v => store.app = v}>
                {svcstore.apps.map((item,index) => (
                  <Select.Option  value={item} key={index}>{item}</Select.Option>
                ))}
              </Select>
            </Col>
          </Form.Item>
          <Form.Item required label="用户" >
            <Col span={16}>
              <Select   placeholder="请选择" value={store.user} onChange={v => store.user = v}>
                {userStore.records.map((item,index) => (
                  <Select.Option  value={item.nickname} key={index}>{item.nickname}</Select.Option>
                ))}
              </Select>
            </Col>
          </Form.Item>
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
