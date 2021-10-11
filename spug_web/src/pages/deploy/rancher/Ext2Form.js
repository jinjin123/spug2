/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Steps,Form } from 'antd';
import styles from './index.module.css';
import Setup1 from './Ext2Setup1';
import Setup2 from './Ext2Setup2';
import Setup3 from './Ext2Setup3';
import store from './store';

@observer
class Ext2From extends React.Component {
  render(){
    const appName = store.record.dpname;
    let title = `常规发布 - ${appName}`;
    return (
      <Modal
        visible
        width={900}
        maskClosable={false}
        title={title}
        onCancel={() => store.ext2Visible = false}
        footer={null}>
        <Steps current={store.page} className={styles.steps}>
          <Steps.Step key={0} title="基本配置"/>
          <Steps.Step key={1} title="发布参数"/>
          <Steps.Step key={2} title="关联配置修改"/>
        </Steps>
        {store.page === 0 && <Setup1/>}
        {store.page === 1 && <Setup2/>}
        {store.page === 2 && <Setup3/>}
      </Modal>
    )
  }
}

export default Form.create()(Ext2From)
