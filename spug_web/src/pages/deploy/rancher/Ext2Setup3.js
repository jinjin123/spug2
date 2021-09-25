/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Form, Input, Button, message, Divider, Alert, Icon, Select } from 'antd';
import Editor from 'react-ace';
import 'ace-builds/src-noconflict/mode-sh';
import 'ace-builds/src-noconflict/theme-tomorrow';
import styles from './index.module.css';
import { http, cleanCommand } from 'libs';
import store from './store';
import lds from 'lodash';

@observer
class Ext2Setup3 extends React.Component {
  constructor(props) {
    super(props);
    this.helpMap = {
      '0': null,
      '1': '相对于输入的本地路径的文件路径，仅将匹配到文件传输至要发布的目标主机。',
      '2': '支持模糊匹配，如果路径以 / 开头则基于输入的本地路径匹配，匹配到文件将不会被传输。'
    }
    this.state = {
      loading: false,
    }
  }

  componentDidMount() {
     console.log(store.record)
  }
  handleSubmit = () => {
    this.setState({loading: true});
    // const info = store.deploy;
    // info['app_id'] = store.app_id;
    // info['extend'] = '2';
    // info['host_actions'] = info['host_actions'].filter(x => (x.title && x.data) || (x.title && (x.src || x.src_mode === '1') && x.dst));
    // info['server_actions'] = info['server_actions'].filter(x => x.title && x.data);
    http.post('/api/deploy/request/rancher/', store.record)
      .then(res => {
        message.success('建立发布审批单成功！');
        store.ext2Visible = false;
      }, () => this.setState({loading: false}))
  };

  render() {

    return (
      <Form labelCol={{span: 6}} wrapperCol={{span: 14}} className={styles.ext2Form}>
          <Alert
            closable
            showIcon
            type="info"
            message="小提示"
            style={{margin: '0 80px 20px'}}
            description={[
              <p key={1}>不需要修改配置则点击直接提交</p>,
              <p key={2}>已经在rancher配置管理修改了配置值，不需要继续添加Key value的话则直接点击提交 </p>,
              <p key={3}>如上面2点不满足则继续添加基于已关联的配置增量映射key value</p>,
            ]}/>
        {!store.isReadOnly && (
          <Form.Item wrapperCol={{span: 14, offset: 6}}>
            <Button disabled={store.isReadOnly} type="dashed" block >
              <Icon type="plus"/>在已有关联卷基础上添加配置映射值？
            </Button>
          </Form.Item>
        )}
        <Form.Item wrapperCol={{span: 14, offset: 6}}>
          <Button
            type="primary"
            // disabled={store.isReadOnly || [...host_actions, ...server_actions].filter(x => x.title && x.data).length === 0}
            loading={this.state.loading}
            onClick={this.handleSubmit}>提交</Button>
          <Button style={{marginLeft: 20}} onClick={() => store.page -= 1}>上一步</Button>
        </Form.Item>
      </Form>
    )
  }
}

export default Ext2Setup3
