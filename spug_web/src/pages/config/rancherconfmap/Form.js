/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message} from 'antd';
import http from 'libs/http';
import store from './store';
import 'codemirror/lib/codemirror.js';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/shell/shell.js';
import 'codemirror/theme/monokai.css';
import styles from './form.module.css';
import envStore from '../environment/store'
import './form.css';
import CodeMirrorWrapper from "./CodeMirrorWrapper";
@observer
class ComForm extends React.Component {
  constructor(props) {
    super(props);
    this.isModify = store.record.id !== undefined;
    this.state = {
      loading: false,
      envs: this.isModify ? [store.record.env_id] : []
    }
  }

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    formData['old_id'] = store.record.id;
    formData['envs'] = this.state.envs;
    // request = http.post('/api/config/', formData)

    http.put('/api/config/rsconfig/', formData)
      .then(res => {
        message.success('操作成功');
        store.formVisible = false;
        store.fetchRecords()
      }, () => this.setState({loading: false}))
  };

  handleEnvCheck = (id) => {
    if (!this.isModify) {
      const index = this.state.envs.indexOf(id);
      if (index !== -1) {
        this.state.envs.splice(index, 1);
      } else {
        this.state.envs.push(id);
      }
      this.setState({envs: this.state.envs})
    }
  };

  render() {
    const info = store.record;
    const {envs} = this.state;
    const {getFieldDecorator} = this.props.form;
    return (
      <Modal
      visible
      width={800}
      style={{ float: 'right',top: 0}}
      wrapClassName={'modalbox'}
      maskClosable={false}
      title={store.record.id ? '更新配置' : '新增配置'}
      onCancel={() => store.formVisible = false}
      confirmLoading={this.state.loading}
      onOk={this.handleSubmit}>
        {/* <div className={styles.ChildBox}> 
          <div className={styles.ChildContent}>
                <CodeMirror 
                            options={{
                              mode: 'shell',
                              theme: 'monokai',
                              lineNumbers: true
                            }}
                            onChange={(editor, data, value) => {
                              console.log(editor)
                            }}
                          />
          </div>
        </div> */}
            <Form labelCol={{span: 2}} wrapperCol={{span: 22}}>
              <Form.Item required label="Key">
                {getFieldDecorator('configMap_k', {initialValue: info['configMap_k']})(
                  <Input disabled={true} placeholder=""  />
                )}
              </Form.Item>
              <Form.Item required label="Value">
                {this.props.form.getFieldDecorator('configMap_v', {initialValue: info['configMap_v']})(
                            <CodeMirrorWrapper 
                            options={{
                              mode: 'shell',
                              theme: 'monokai',
                              lineNumbers: true
                            }}
                          />
                )}
              </Form.Item>
              <Form.Item hidden>
                  {getFieldDecorator('configname', {initialValue: info['configname']})(
                      <Input disabled={true} placeholder=""  />
                    )}
              </Form.Item>
              <Form.Item hidden>
                  {getFieldDecorator('namespace', {initialValue: info['namespace']})(
                      <Input disabled={true} placeholder=""  />
                    )}
              </Form.Item>
              <Form.Item hidden>
                  {getFieldDecorator('configid', {initialValue: info['configid']})(
                      <Input disabled={true} placeholder=""  />
                    )}
              </Form.Item>
              <Form.Item label="选择环境">
                {envStore.records.map((item, index) => (
                  <Row
                    key={item.id}
                    onClick={() => this.handleEnvCheck(item.id)}
                    style={{cursor: 'pointer', borderTop: index ? '1px solid #e8e8e8' : ''}}>
                    <Col span={2}><Checkbox disabled={this.isModify} checked={envs.includes(item.id)}/></Col>
                    <Col span={4} className={styles.ellipsis}>{item.key}</Col>
                    <Col span={9} className={styles.ellipsis}>{item.name}</Col>
                    <Col span={9} className={styles.ellipsis}>{item.desc}</Col>
                  </Row>
                ))}
              </Form.Item>
            </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
