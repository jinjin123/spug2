/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Form, Button,Input,Row, Col,Checkbox,Switch } from "antd";
import { hasHostPermission } from 'libs';
import store from './store';
import styles from './index.module.css';
import envStore from 'pages/config/environment/store'
@observer
class Ext2Setup2 extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    if (envStore.records.length === 0) {
      envStore.fetchRecords()
    }
    store.record["update_img"] = true
    store.record["app_name"] = ""
  }

  render() {
    const info = store.record;
    const envs = [info.env_id];
    console.log(info)
    const {getFieldDecorator} = this.props.form;
    return (
      <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
        <Form.Item required label="发布版本命名唯一">
              <Input placeholder="发布命名写点相关的字把" onChange={e => info.app_name = e.target.value} />
        </Form.Item>
        <Form.Item required label="实体项目">
            {getFieldDecorator('top_project', {initialValue: info['top_project']})(
              <Input placeholder="实体项目"disabled/>
            )}
        </Form.Item>
        <Form.Item required label="rancher细分项目">
            {getFieldDecorator('pjname', {initialValue: info['pjname']})(
              <Input placeholder="rancher细分项目" disabled/>
            )}
        </Form.Item>
        <Form.Item required label="应用名">
            {getFieldDecorator('dpname', {initialValue: info['dpname']})(
              <Input placeholder="应用名" disabled />
            )}
        </Form.Item>
        <Form.Item required label="镜像">
            {getFieldDecorator('img', {initialValue: info['img']})(
              <Input placeholder="镜像名"  disabled={info["update_img"]} onChange={e => info.img = e.target.value}/>
            )}
              <Switch
              // defaultChecked
              checkedChildren="不更新"
              unCheckedChildren="更新"
              checked={info['update_img']}
              onChange={v => info['update_img'] = v}
              />
        </Form.Item>
        <Form.Item label="选择环境">
            {envStore.records.map((item, index) => (
              <Row
                key={item.id}
                style={{ cursor: 'pointer', borderTop: index ? '1px solid #e8e8e8' : '' }}>
                <Col span={2}><Checkbox disabled checked={envs.includes(item.id)} /></Col>
                <Col span={4} className={styles.ellipsis}>{item.key}</Col>
                <Col span={9} className={styles.ellipsis}>{item.name}</Col>
                <Col span={9} className={styles.ellipsis}>{item.desc}</Col>
              </Row>
            ))}
          </Form.Item>
        <Form.Item wrapperCol={{span: 14, offset: 6}}>
          {/* <Button disabled={info['host_ids'].filter(x => x).length === 0} type="primary" onClick={() => store.page += 1}>下一步</Button> */}
          <Button  type="primary" onClick={() => store.page += 1}>下一步</Button>
          <Button style={{marginLeft: 20}} onClick={() => store.page -= 1}>上一步</Button>
        </Form.Item>

      </Form>
    )
  }
}

export default Form.create()(Ext2Setup2)