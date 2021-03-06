/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Card, Icon } from 'antd';
import store from './store';
import styles from './index.module.css';

@observer
class AddRancherSelect extends React.Component {
  switchExt1 = () => {
    store.addVisible = false;
    store.ext1Visible = true;
    store.deploy = {
      git_type: 'branch',
      is_audit: false,
      rst_notify: {mode: '0'},
      versions: 10,
      host_ids: [undefined],
      filter_rule: {type: 'contain', data: ''}
    }
  };

  switchExt2 = () => {
    store.addRancherVisible = false;
    store.ext2Visible = true;
    store.deploy = {
      is_audit: false,
      rst_notify: {mode: '0'},
      host_ids: [undefined],
      host_actions: [],
      server_actions: []
    }
  };

  render() {
    const modalStyle = {
      display: 'flex',
      justifyContent: 'space-around',
      backgroundColor: 'rgba(240, 242, 245, 1)',
      padding: '80px 0'
    };

    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title="选择发布方式"
        bodyStyle={modalStyle}
        onCancel={() => store.addRancherVisible = false}
        footer={null}>
        <Card
          style={{width: 600, cursor: 'pointer'}}
          bodyStyle={{display: 'flex'}}
          onClick={this.switchExt2}>
          <div style={{marginRight: 16}}>
            <Icon type="ordered-list" style={{fontSize: 36, color: '#1890ff'}}/>
          </div>
          <div>
            <div className={styles.cardTitle}>常规发布</div>
            <div className={styles.cardDesc}>
            由 运维 来控制发布的主流程，你可以近通过添加的参数即可完成发布操作。
            </div>
          </div>
        </Card>
        {/* <Card
          style={{width: 300, cursor: 'pointer'}}
          bodyStyle={{display: 'flex'}}
          onClick={this.switchExt2}>
          <div style={{marginRight: 16}}>
            <Icon type="build" style={{fontSize: 36, color: '#1890ff'}}/>
          </div>
          <div>
            <div className={styles.cardTitle}>自定义发布</div>
            <div className={styles.cardDesc}>
              你可以完全自己定义发布的所有流程和操作，Spug 负责按顺序依次执行你记录的动作。
            </div>
          </div>
        </Card> */}
      </Modal>
    )
  }
}

export default AddRancherSelect
