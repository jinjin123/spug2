/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, message } from 'antd';
import http from 'libs/http';
import store from './store';

@observer
class ComForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
    }
  }

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    formData['id'] = store.record.id;
    http.post('/api/config/portlist/', formData)
      .then(res => {
        message.success('操作成功');
        store.formVisible = false;
        store.fetchRecords()
      }, () => this.setState({loading: false}))
  };

  render() {
    const info = store.record;
    const {getFieldDecorator} = this.props.form;
    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title={store.record.id ? '编辑端口记录' : '编辑端口记录'}
        onCancel={() => store.formVisible = false}
        confirmLoading={this.state.loading}
        onOk={this.handleSubmit}>
        <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
          <Form.Item required label="ip地址">
            {getFieldDecorator('ipaddress', {initialValue: info['ipaddress']})(
              <Input placeholder="请输入ip地址，例如：1.1.1.1"/>
            )}
          </Form.Item>
          <Form.Item required label="端口">
            {getFieldDecorator('port', {initialValue: info['port']})(
              <Input placeholder="请输入端口，例如：22，333，444"/>
            )}
          </Form.Item>
          <Form.Item label="备注信息">
            {getFieldDecorator('comment', {initialValue: info['comment']})(
              <Input.TextArea placeholder="请输入备注信息"/>
            )}
          </Form.Item>
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
