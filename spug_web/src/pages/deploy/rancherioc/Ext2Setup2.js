/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Form, Button,Input,Row, Col,Checkbox,Switch,message, DatePicker} from "antd";
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
    // const formData = this.props.form.getFieldsValue();
    if (this.state.args['date'] <= moment()) {
      return message.error('??????????????????????????????????????????')
    }
    this.props.form.validateFields((err) => {
        if(!err){
          
          this.setState({loading: true});
          store.record["pbtype"] = store.pbtype
          store.record["state"] = false
          store.record["desccomment"] = store.desccomment
          store.record["app_name"] = store.record['dpname']+FormatDate(new Date(),"sec")
          store.record['trigger'] = 'date'
          store.record['trigger_args'] = moment(this.state.args['date']).format('YYYY-MM-DD HH:mm:ss') 
          
          if (store.record['update_img'] === true && store.record['update_cmap'] === true){
              return message.error("?????????????????? ?????????  ???????????????")
          }
          console.log(store.record) 
          http.post('/api/deploy/request/rancher/', store.record)
            .then( ()=> {
              message.success('??????????????????????????????');
              store.ext2Visible = false;
              store.page = 0;
              store.addRancherVisible = false;

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
        <Form.Item required label="????????????????????????" >
            {getFieldDecorator('app_name', {initialValue: info['dpname']+FormatDate(new Date(),"sec"),rules: [{required: true, message: '??????????????? '}]})(
              <Input placeholder="????????????????????????????????????"  onChange={e => info.app_name = e.target.value} />
            )}
        </Form.Item>
        <Form.Item required label="????????????">
            {getFieldDecorator('top_project', {initialValue: info['top_project']})(
              <Input placeholder="????????????"disabled/>
            )}
        </Form.Item>
        <Form.Item required label="rancher????????????">
            {getFieldDecorator('pjname', {initialValue: info['pjname']})(
              <Input placeholder="rancher????????????" disabled/>
            )}
        </Form.Item>
        <Form.Item required label="????????????">
            {getFieldDecorator('pjname', {initialValue: info['nsname']})(
              <Input placeholder="????????????" disabled/>
            )}
        </Form.Item>
        <Form.Item required label="?????????">
            {getFieldDecorator('dpname', {initialValue: info['dpname']})(
              <Input placeholder="?????????" disabled />
            )}
        </Form.Item>
        <Form.Item required label="??????">
            {getFieldDecorator('img', {initialValue: info['img']})(
              <Input placeholder="?????????"  disabled={info["update_img"]} onChange={e => info.img = e.target.value}/>
            )}
              <Switch
              // defaultChecked
              checkedChildren="?????????"
              unCheckedChildren="??????"
              checked={info['update_img']}
              onChange={v => info['update_img'] = v}
              />
        </Form.Item>
        <Form.Item label="????????????">
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
          <Form.Item required label="????????????" extra="?????????????????????????????????">
            {getFieldDecorator('trigger', {valuePropName: 'activeKey',initialValue: 'date' })(
              <DatePicker
                showTime
                disabledDate={v => v && v.format('YYYY-MM-DD') < moment().format('YYYY-MM-DD')}
                style={{width: 150}}
                placeholder="?????????????????????+1??????"
                onOk={() => false}
                value={args['date'] ? moment(args['date']) : undefined}
                onChange={v => this.handleArgs('date', v)}/>
              )}
          </Form.Item>
        <Form.Item wrapperCol={{span: 14, offset: 6}}>
          <Switch
              // defaultChecked
              checkedChildren="????????????????????????"
              unCheckedChildren="?????????????????????"
              checked={info["update_cmap"]}
              onChange={v => info['update_cmap'] = v}
              />
          {/* <Button disabled={info['host_ids'].filter(x => x).length === 0} type="primary" onClick={() => store.page += 1}>?????????</Button> */}
          <Button  type="primary" onClick={() =>  info['update_cmap']  ?   this.handleSubmit() :  store.page += 1  }> { info['update_cmap']  ? "????????????" : "?????????"}</Button>
          <Button style={{marginLeft: 20}} onClick={() => store.page -= 1}>?????????</Button>
        </Form.Item>

      </Form>
    )
  }
}

export default Form.create()(Ext2Setup2)