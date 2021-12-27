/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Button, Form, Modal,Input,message } from 'antd';
import store from './store';
import lds from 'lodash';
import { http } from 'libs';
@observer
class RestartForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      loading: false,
      visible: true
    }
  }
  handleOk = () => {
    this.setState({ loading: true });
    const info = store.restartrecord
    http.post('/api/app/svc/rdp/', {"id": parseInt(info.id),"tag":"feiyanuos"})
    .then(() => {
        message.success('重启成功');
        store.restartVisible = false;
        store.fetchRecords()
      
    }, () => {this.setState({loading: false}); store.restartVisible = false})

  };
  handleCancel = () => {
    store.restartVisible = false 
  };
  render() {
    const info = store.restartrecord
    const {  loading } = this.state;
    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        wrapClassName={'modalbox'}
        title="重启确认"
        onOk={() => this.handleOk}
        onCancel={() => store.restartVisible = false}
        footer={[
          <Button key="back" onClick={this.handleCancel}>
            取消
          </Button>,
          <Button key="submit" type="primary" loading={loading} onClick={this.handleOk}>
          提交
          </Button>,

        ]}
        > 
          <Form>
            <Form.Item label="项目">
              <Input  disabled defaultValue={info.top_project}/>
            </Form.Item>
            <Form.Item label="rancher项目">
                <Input disabled  defaultValue={info.pjname}/>
            </Form.Item>
            <Form.Item label="命名空间">
              <Input disabled  defaultValue={info.nsname}/>
            </Form.Item>
            <Form.Item label="应用名">
              <Input disabled  defaultValue={info.dpname}/>
            </Form.Item>
            <Form.Item label="镜像名">
              <Input disabled defaultValue={info.img}/>
            </Form.Item>
          </Form>
      </Modal>
    )
  }
}

export default RestartForm