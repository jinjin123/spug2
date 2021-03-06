/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Button, Select, DatePicker, Radio, Row, Col, Modal, Form, Input, message,Icon,Divider,Tag } from 'antd';
import { SearchForm, AuthFragment, AuthCard } from 'components';
import SelectApp from './SelectApp';
import Ext1Form from './Ext1Form';
import Ext2Form from './Ext2Form';
import Approve from './Approve';
import ComTable from './Table';
import {http,FormatDate,GetDateDiff,getDatetime,isWeekEnd} from 'libs';
import envStore from 'pages/config/environment/store';
import appStore from 'pages/config/app/store'
import store from './store';
import moment from 'moment';
import DiffForm from './DiffForm';
import RollbackForm from './RollbackForm';

@observer
class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      expire: undefined,
      count: '',
      status: true,
      tips: ""
    }
  }

  componentDidMount() {
    if (envStore.records.length === 0) {
      envStore.fetchRecords()
    }
    if (appStore.records.length === 0) {
      appStore.fetchRecords()
    }
    if(isWeekEnd(getDatetime("week")) === true){
      this.setState({
        status:false,
        tips: "周末例外可解锁提权为运维权限"
      })
    }else{
      let timer = setInterval(() => {
        var current_time = new Date()
        var old_time     = new Date(getDatetime());
        var current_time = FormatDate(current_time, "str" ); 
        var old_time     = FormatDate(old_time,"str"); 
        var res = GetDateDiff( old_time,current_time)
        if (res <=0){
          this.setState({
            status:false,
            tips: "可解锁提权为运维权限"
          })
          clearInterval(timer);
        }else {
          this.setState({
            tips: "还差" + res.toString() + "分钟解锁"
          })
        }
      }, 1000)
    }
  }

  handleBatchDel = () => {
    Modal.confirm({
      icon: 'exclamation-circle',
      title: '批量删除发布申请',
      content: (
        <Form>
          <Form.Item label="截止日期" help={<div>将删除截止日期<span style={{color: 'red'}}>之前</span>的所有发布申请记录。</div>}>
            <DatePicker style={{width: 200}} placeholder="请输入"
                        onChange={val => this.setState({expire: val.format('YYYY-MM-DD')})}/>
          </Form.Item>
          <Form.Item label="保留记录" help="每个应用每个环境仅保留最新的N条发布申请，优先级高于截止日期">
            <Input allowClear style={{width: 200}} placeholder="请输入保留个数"
                   onChange={e => this.setState({count: e.target.value})}/>
          </Form.Item>
        </Form>
      ),
      onOk: () => {
        const {expire, count} = this.state;
        return http.delete('/api/deploy/request/', {params: {expire, count}})
          .then(res => {
            message.success(`成功删除${res}条记录`);
            store.fetchRecords()
          })
      },
    })
  };
  Bootsmater = () => {
      http.post(`/api/deploy/request/master`)
      .then(()=> {
        message.success('提权成功');
        http.get('/api/account/logout/')
        this.props.history.push("/")
      }, () => this.setState({loading: false}))
  }

  render() {
    return (
      <AuthCard auth="deploy.request.view">
        <SearchForm>
          <SearchForm.Item span={6} title="发布环境">
            <Select allowClear value={store.f_env_id} onChange={v => store.f_env_id = v} placeholder="请选择">
              {envStore.records.map(item => (
                <Select.Option key={item.id} value={item.id}>{item.name}</Select.Option>
              ))}
            </Select>
          </SearchForm.Item>
          <SearchForm.Item span={6} title="应用名称">
            <Select 
              showSearch
              filterOption={(input, option) =>
                option.props.children.indexOf(input)  >= 0
              }
              filterSort={(optionA, optionB) =>
                optionA.props.children.localeCompare(optionB.props.children)
              }
            allowClear value={store.f_app_id} onChange={v => store.f_app_id = v} placeholder="请选择">
              {appStore.records.map(item => (
                <Select.Option key={item.id} value={item.id}>{item.name}</Select.Option>
              ))}
            </Select>
          </SearchForm.Item>
          <SearchForm.Item span={8} title="申请时间">
            <DatePicker.RangePicker
              value={store.f_s_date ? [moment(store.f_s_date), moment(store.f_e_date)] : undefined}
              onChange={store.updateDate}/>
          </SearchForm.Item>
          <SearchForm.Item span={4} style={{textAlign: 'right'}}>
            <Button type="primary" icon="sync" onClick={store.fetchRecords}>刷新</Button>
          </SearchForm.Item>
        </SearchForm>
        <Row style={{marginBottom: 16}}>
          <Col span={16}>
            <Radio.Group value={store.f_status} onChange={e => store.f_status = e.target.value}>
              <Radio.Button value="all">全部({store.counter['all'] || 0})</Radio.Button>
              <Radio.Button value="0">待审核({store.counter['0'] || 0})</Radio.Button>
              <Radio.Button value="1">待发布({store.counter['1'] || 0})</Radio.Button>
              <Radio.Button value="3">发布成功({store.counter['3'] || 0})</Radio.Button>
              <Radio.Button value="-3">发布异常({store.counter['-3'] || 0})</Radio.Button>
              <Radio.Button value="99">其他({store.counter['99'] || 0})</Radio.Button>
            </Radio.Group>
          </Col>
          <Col span={8} style={{textAlign: 'right'}}>
              <AuthFragment auth="deploy.request.view">
                <div style={{"display":  "flex"}}>
                  <Button type="primary" disabled={this.state.status} onClick={() =>{this.Bootsmater()}} > <Icon type="android" />临时提权为运维 </Button>
                  <Tag color="magenta">{this.state.tips}</Tag>
                </div>
              </AuthFragment>
              <Divider type="vertical"/>
            {/* <AuthFragment auth="deploy.request.patch">
                <Button type="primary" > <Icon type="thunderbolt" />批量发布</Button>
              </AuthFragment>
              <Divider type="vertical"/> */}
            {/* <AuthFragment auth="deploy.request.del">
              <Button type="primary" icon="delete" onClick={this.handleBatchDel}>批量删除</Button>
            </AuthFragment> */}
            {/* <AuthFragment auth="deploy.request.add">
              <Button
                type="primary"
                icon="plus"
                onClick={() => store.addVisible = true}
                style={{marginLeft: 20}}>新建发布申请</Button>
            </AuthFragment> */}
          </Col>
        </Row>
        <ComTable/>
        {store.addVisible && <SelectApp/>}
        {store.ext1Visible && <Ext1Form/>}
        {store.ext2Visible && <Ext2Form/>}
        {store.diffVisble && <DiffForm/>}
        {store.rollVisible && <RollbackForm/>}


        {store.approveVisible && <Approve/>}
      </AuthCard>
    )
  }
}

export default Index