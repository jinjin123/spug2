/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Table,Radio,Select} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import  styles from "./index.module.css";
@observer
class DeployForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        value: 1,
        input_value: 1
    }
  }
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
  onChange = e => {
    console.log('radio checked', e.target.value);
    this.setState({
      value: e.target.value,
    });
  };

  onRadioInputChange = e => {
    this.setState({
      input_value: e.target.value,
    });
  };
  render() {
    // let data = store.vrecords;
    const {value} = this.state;
    const {input_value} = this.state;
    const { Option } = Select;
    // if (historystore.f_name) {
    //   data = data.filter(item => item['namespace'].toLowerCase().includes(historystore.f_name.toLowerCase()))
    // }
    return (
        <Modal
        visible
        width={1100}
        style={{ float: 'right',top: 0}}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.record.id ? '新应用服务部署' : '以现有应用服务部署'}
        onCancel={() => store.deployForm = false}
        onOk={() => store.deployForm = false}
        >
          <Form  layout="inline" wrapperCol={{ span: 24 }}>
            <Form.Item required label="名称"  rules={[{ required: true, message: 'Please input your username!' }]}>
                {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                  <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                {/* )} */}
            </Form.Item>
            <Form.Item required label="工作负载类型"  rules={[{ required: true, message: 'Please input your username!' }]}>
                {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                  <Radio.Group onChange={this.onChange} value={value}>
                    <div className={styles.RadioVisbale}>
                        <Radio value={1}>Deployment: 部署无状态应用:<Input style={{ width: 50, marginLeft: 10 }} placeholder="" onChange={this.onRadioInputChange} />个 Pods</Radio>
                        <Radio value={2}>DaemonSet: 每台主机部署 {input_value} 个Pods</Radio>
                        <Radio value={3}>StatefulSet: 部署有状态应用 {input_value}个Pods </Radio>
                        <Radio value={4}>CronJob: 定时运行{input_value} 个Pods</Radio>
                        <Radio value={5}>Job: 一次性运行{input_value} 个Pods</Radio>
                      </div>
                  </Radio.Group>
                {/* )} */}
            </Form.Item>
            </Form>
            <Form layout="inline" wrapperCol={{ span: 24 }}>
                <Form.Item required label="Docker镜像" rules={[{ required: true, message: 'Please input your username!' }]}>
                    {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                      <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                      {/* )} */}
                </Form.Item>
                <Form.Item required label="命名空间" rules={[{ required: true, message: 'Please input your username!' }]}>
                    {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                      <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                    {/* )} */}
                </Form.Item>
              </Form>
              <Form>
                  <Form.Item  label="端口映射" rules={[{ required: true, message: 'Please input your username!' }]}>
                      {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                        <Input placeholder="例如:tcp8080" style={{ width: 150, marginLeft: 10 }}/> &nbsp;
                        <Input placeholder="容器端口" style={{ width: 150, marginLeft: 10 }}/>&nbsp;&nbsp;&nbsp;
                        <Select defaultValue="TCP" style={{ width: 100 }} >
                          <Option value="TCP">TCP</Option>
                          <Option value="UDP">UDP</Option>
                        </Select>&nbsp;&nbsp;
                          <Select defaultValue="NodePort"  style={{ width: 280 }} >
                            <Option value="NodePort">NodePort (所有主机端口均可访问)</Option>
                            <Option value="HostPort">HostPort (仅 Pod 所在主机端口可访问)</Option>
                          </Select>&nbsp;&nbsp;
                        <Input placeholder="默认NodePort随机端口30000-32768" style={{ width: 250, marginLeft: 10 }}/>
                      {/* )} */}
                  </Form.Item>
                  <Form.Item  label="数据卷" rules={[{ required: true, message: 'Please input your username!' }]}>
                      {/* {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })( */}
                        <Select defaultValue="添加卷..." style={{ width: 250 }} >
                          <Option value="PVC">使用现有PVC</Option>
                          <Option value="host">映射主机目录</Option>
                          <Option value="config">配置映射卷</Option>
                        </Select>&nbsp;&nbsp;
                      {/* )} */}
                  </Form.Item>
              </Form>
 
        </Modal>
    )
  }
}
export default Form.create()(DeployForm)
