/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, message,Select } from 'antd';
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
    http.post('/api/config/project/', formData)
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
        title={store.record.id ? '编辑项目' : '新建项目'}
        onCancel={() => store.formVisible = false}
        confirmLoading={this.state.loading}
        onOk={this.handleSubmit}>
        <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
          <Form.Item required label="项目名称">
            {getFieldDecorator('name', {initialValue: info['name']})(
              <Input placeholder="请输入项目名称，例如：开发项目"/>
            )}
          </Form.Item>
          <Form.Item required label="项目分类">
            {getFieldDecorator('tag', {initialValue: info['tag']})(
                <Select  onChange={this.handleOsForm}  placeholder="项目分类">
                  <Select.Option value={"实体项目"} key={0}>{"实体项目"}</Select.Option>
                  <Select.Option value={"项目子类"} key={1}>{"项目子类"}</Select.Option>
              </Select>
              )}
          </Form.Item>
          <Form.Item label="备注信息">
            {getFieldDecorator('desc', {initialValue: info['desc']})(
              <Input.TextArea placeholder="请输入备注信息"/>
            )}
          </Form.Item>
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
