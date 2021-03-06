/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React, { useState } from 'react';
import { observer } from 'mobx-react';
import { Link } from 'react-router-dom';
import { Switch, Col, Form, Select, Button,Input } from "antd";
import store from './store';
import noticeStore from '../notice/store';
const { TextArea } = Input;

export default observer(function Ext2Setup1() {
  const [envs, setEnvs] = useState([]);

  function updateEnvs() {
    const ids = store.currentRecord['deploys'].map(x => x.env_id);
    setEnvs(ids.filter(x => x !== store.deploy.env_id))
  }

  // useEffect(() => {
  //   if (store.currentRecord['deploys'] === undefined) {
  //     store.loadDeploys(store.app_id).then(updateEnvs)
  //   } else {
  //     updateEnvs()
  //   }
  // }, [])

  const info = store.record;
  let call_us = noticeStore.records
  call_us = call_us.filter(item => item["dpname"].toLowerCase().includes(info["dpname"].toLowerCase()))
  const call_tmp = []
  if (call_us.length >0 ) {
    call_us.map((item) => {
        call_tmp.push(item["nickname"])
    })
  }

  return (
    <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
      <Form.Item required label="发布环境">
        <Col span={16}>
          <Select disabled value={info["env_id"]} onChange={v => info.env_id = v} placeholder="请选择发布环境">
            {/* {envStore.records.map(item => (
              <Select.Option disabled={envs.includes(item.id)} value={item.id} key={item.id}>{item.name}</Select.Option>
            ))} */}
            <Select.Option disabled value={info["env_id"]} key={info.env_id}>{info["env_id"] ==2 ? "prod" : "dev"}</Select.Option>
          </Select>
        </Col>
        <Col span={6} offset={2}>
          <Link disabled={store.isReadOnly} to="/config/environment">新建环境</Link>
        </Col>
      </Form.Item>
      <Form.Item label="发布审核">
        <Switch
          disabled
          defaultChecked
          checkedChildren="开启"
          unCheckedChildren="关闭"
          checked={info['is_audit']=true}
          // onChange={v => info['is_audit'] = v}
          />
      </Form.Item>
      <Form.Item required label="发布类型">
        <Col span={16}>
          <Select defaultValue={1} onChange={v => store.pbtype = v} placeholder="请选择发布类型">
            <Select.Option  value={1} key={1}>迭代发布</Select.Option>
            <Select.Option  value={2} key={2}>bug发布</Select.Option>
            <Select.Option  value={3} key={3}>紧急发布</Select.Option>
            {/* <Select.Option  value={4} key={4}>回滚发布</Select.Option> */}
          </Select>
        </Col>
      </Form.Item>
      <Form.Item required label="发布功能描述">
        <Col span={16}>
            <TextArea   onChange={store.onChange} placeholder="" autoSize />
        </Col>
      </Form.Item>
      {/* <Form.Item label="消息通知" extra={<span>
        应用审核及发布成功或失败结果通知，
        <a target="_blank" rel="noopener noreferrer"
           href="https://spug.cc/docs/install-error/#%E9%92%89%E9%92%89%E6%94%B6%E4%B8%8D%E5%88%B0%E9%80%9A%E7%9F%A5%EF%BC%9F">钉钉收不到通知？</a>
      </span>}>
        <Input addonBefore={(
          <Select disabled={store.isReadOnly}
                  value={info['rst_notify']['mode']} style={{width: 100}}
                  onChange={v => info['rst_notify']['mode'] = v}>
            <Select.Option value="0">关闭</Select.Option>
            <Select.Option value="1">钉钉</Select.Option>
            <Select.Option value="3">企业微信</Select.Option>
            <Select.Option value="2">Webhook</Select.Option>
          </Select>
        )}
        disabled={store.isReadOnly || info['rst_notify']['mode'] === '0'}
        value={info['rst_notify']['value']}
        onChange={e => info['rst_notify']['value'] = e.target.value}
        placeholder="请输入"/>
      </Form.Item> */}
      <Form.Item  required label="审核通知对象人">
          <Col span={16} >
            {/* notice somebody on backend check the notice table mapping */}
            <Input disabled value={call_tmp.length >0 ? call_tmp.join(";") :  "opsgroup"}/>
          </Col>
          <Col span={6} offset={2}>
          <Link disabled={store.isReadOnly} to="/deploy/rancher/notice">新建审核通知人</Link>
        </Col>
      </Form.Item>
      <Form.Item wrapperCol={{span: 14, offset: 6}}>
        <Button
          type="primary"
          disabled={!info.env_id}
          onClick={() => store.page += 1}>下一步</Button>
      </Form.Item>
    </Form>
  )
})
