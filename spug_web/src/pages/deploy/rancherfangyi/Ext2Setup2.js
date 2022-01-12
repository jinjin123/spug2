/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Form, Button,Input,Row, Col,Checkbox,Switch,message,DatePicker } from "antd";
import { hasHostPermission,http,FormatDate } from 'libs';
import store from './store';
import styles from './index.module.css';
import envStore from 'pages/config/environment/store'
import moment from 'moment';

@observer
class Ext2Setup2 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      // updatecmap: true,
      args: {"date": null},

    }
  }
  
  componentDidMount() {
    if (envStore.records.length === 0) {
      envStore.fetchRecords()
    }
    store.record["update_img"] = true
    store.record["app_name"] = ""
    store.record["update_cmap"] = true
    store.record["trigger"] = "" 
    store.record["trigger_args"] = "" 
  }
  handleArgs = (type, value) => {
    // value = moment(value).format('YYYY-MM-DD HH:mm:ss')
    // console.log(moment(value).format('YYYY-MM-DD HH:mm:ss'))
    // console.log(moment(),moment(value),moment.locale());
    const args = Object.assign(this.state.args, {"date": value});
    this.setState({args})
    store.tmptime = moment(this.state.args['date']).format('YYYY-MM-DD HH:mm:ss') 

  };
  _parse_args = (trigger) => {
    switch (trigger) {
      case 'date':
        return moment(this.state.args['date']).format('YYYY-MM-DD HH:mm:ss');
      case 'cron':
        const {rule, start, stop} = this.state.args['cron'];
        return JSON.stringify({
          rule,
          start: start ? moment(start).format('YYYY-MM-DD HH:mm:ss') : null,
          stop: stop ? moment(stop).format('YYYY-MM-DD HH:mm:ss') : null
        });
      default:
        return this.state.args[trigger];
    }
  };
  handleSubmit = () => {
    if (this.state.args['date'] <= moment()) {
      return message.error('任务执行时间不能早于当前时间')
    }
    this.props.form.validateFields((err, formData) => {
        if(!err){
          this.setState({loading: true});
          store.record["pbtype"] = store.pbtype
          store.record["state"] = false
          store.record["desccomment"] = store.desccomment
          store.record["app_name"] = store.record['dpname']+FormatDate(new Date(),"sec")
          store.record['trigger'] = 'date'
          store.record['trigger_args'] = moment(this.state.args['date']).format('YYYY-MM-DD HH:mm:ss') 
          if (store.record['update_img'] === true && store.record['update_cmap'] === true){
            return message.error("必须更新镜像 或者是  配置映射卷")
        }
          http.post('/api/deploy/request/rancher/', store.record)
            .then( ()=> {
              message.success('建立发布审批单成功！');
              store.ext2Visible = false;
              store.addRancherVisible = false;
              store.page = 0;

            }, () => this.setState({loading: false}))
        }
    })
  };

  render() {
    const info = store.record;
    const envs = [info.env_id];
    const {args} = this.state;

    const {getFieldDecorator} = this.props.form;
    return (
      <Form labelCol={{span: 6}} wrapperCol={{span: 14}}>
        <Form.Item required label="发布版本命名唯一" >
            {getFieldDecorator('app_name', {initialValue: info['dpname']+FormatDate(new Date(),"sec"),rules: [{required: true, message: '必填发布名 '}]})(
              <Input placeholder="填写发版命名唯一方便追溯" onChange={e => info.app_name = e.target.value} />
            )}
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
        <Form.Item required label="命名空间">
            {getFieldDecorator('pjname', {initialValue: info['nsname']})(
              <Input placeholder="命名空间" disabled/>
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
          <Form.Item required label="发布时间" extra="仅在指定时间运行一次。">
            {getFieldDecorator('trigger', {valuePropName: 'activeKey',initialValue: 'date' })(
              <DatePicker
                showTime
                disabledDate={v => v && v.format('YYYY-MM-DD') < moment().format('YYYY-MM-DD')}
                style={{width: 150}}
                placeholder="请选择发布时间+1分钟"
                onOk={() => false}
                value={args['date'] ? moment(args['date']) : undefined}
                onChange={v => this.handleArgs('date', v)}/>
              )}
          </Form.Item>
        <Form.Item wrapperCol={{span: 14, offset: 6}}>
          <Switch
              // defaultChecked
              checkedChildren="不更新配置映射卷"
              unCheckedChildren="更新配置映射卷"
              checked={info["update_cmap"]}
              onChange={v => info['update_cmap'] = v}
              />
          {/* <Button disabled={info['host_ids'].filter(x => x).length === 0} type="primary" onClick={() => store.page += 1}>下一步</Button> */}
          <Button  type="primary" onClick={() =>  info['update_cmap']  ?   this.handleSubmit() :  store.page += 1  }> { info['update_cmap']  ? "提交发布" : "下一步"}</Button>
          <Button style={{marginLeft: 20}} onClick={() => store.page -= 1}>上一步</Button>
        </Form.Item>

      </Form>
    )
  }
}

export default Form.create()(Ext2Setup2)