/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Button,Radio,Select,Card,Icon} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import  styles from "./index.module.css";
@observer
class CmpForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      loading: false,
        value: 1,
        hostvalue: 2,
        input_value: 1,
        tmpns: [],
        tmpimg: [],
        pvctype:[],
        moreAction: [{"id":0,"v":"添加卷..."}]

    }
  }
  componentDidMount() {
    let tmp = []
    {store.pvcrecords.map((item,index)=>(
      tmp.push(item['storageid'])
    ))}
    this.setState({
        pvctype: [... new Set(tmp)]
    })
  }

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
  onCallHostChange = e => {
    console.log('radio checked', e.target.value);
    // this.setState({
    //   hostvalue: e.target.value,
    // });
    if(e.target.value === 1){
      store.rancherCallhost = []
      store.rancherCallhost.push({
        "itemid":1,"iteminput":"", 
      })
    }else{
      store.rancherCallhost = []
      store.rancherCallhost.push(
        {"itemid":1,"itemtitle":"必须","itemdata":[{"itemk":"","itemtype":"=","itemv":""}]},
        {"itemid":2,"itemtitle":"最好","itemdata":[{"itemk":"","itemtype":"=","itemv":""}]},
        {"itemid":3,"itemtitle":"首选","itemdata":[{"itemk":"","itemtype":"=","itemv":""}]}
      )
    }
  }

  
  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    console.log(formData,this.state.input_value,store.rancherport,store.rancherenv, store.rancherCallhost)
  };

  
  onCallHostItemClick = (index,tindex) => {
    console.log(index,tindex)
    switch(tindex){
      case 0:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 1 ? item["itemdata"].splice(index,1): null
        ))}
        break;;
      case 1:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 2 ? item["itemdata"].splice(index,1): null
        ))}
        break;;
      case 2:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 3 ? item["itemdata"].splice(index,1): null
        ))}
        break;;
    }
  }

  onRjChange = v => {
    let t = store.records.filter(item => item['pjname'] === v)

    let tmp = []
    let tmpimg = []
    t.map(item =>(
        tmp.push(item["nsname"]),
        tmpimg.push(item['img'])
    ))
    this.setState({
      tmpns: [... new Set(tmp)],
      tmpimg: [... new Set(tmpimg)]
    }) 
  }

  render() {
    // let data = store.vrecords;
    const {value} = this.state;
    const {input_value} = this.state;
    const { Option } = Select;
    const {getFieldDecorator} = this.props.form;

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
        title={'添加配置映射'}
        onCancel={() => store.cmpForm = false}
        onOk={this.handleSubmit}
        >
          <Form  layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称"  rules={[{ required: true, message: '必填名' }]}>
                  {getFieldDecorator('cmp_name')(
                    <Input placeholder="e.g. myapp" style={{ width: 200, marginLeft: 10 }}/>
                  )}
              </Form.Item>

                <Form.Item required label="rancher项目" rules={[{ required: true, message: '必填项目' }]}>
                    {getFieldDecorator('rjproject')(
                      <Select  onChange={v=> this.onRjChange(v)} style={{ width: 200 }} >
                          {store.rancherpj.map((item,index)=>(
                              <Option key={item} value={item}>{item}</Option>
                            
                          ))}
                      </Select>
                    )}
                </Form.Item>

                <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                    {getFieldDecorator('namespace')(
                      <Select   style={{ width: 150 }} >
                          {this.state.tmpns.map((item,index)=>(
                              <Option key={index} value={item}>{item}</Option>
                          ))}
                      </Select>
                    )}
                </Form.Item>
                <Form.Item required label="配置映射" >
                    <Card title="配置映射" style={{ width: 900 }}>
                          {store.ranchercmp.map((item,index)=>(
                              <div key={index} style={{ display: "flex"}}>
                                  <Input value={item['k']} style={{ width: 350, marginRight: 10 }} placeholder="key" />  =  <Input value={item['v']}  style={{ width: 350 , marginLeft: 10}} placeholder="value"/>
                                  <div  onClick={() => store.ranchercmp.splice(index,1)}>
                                    <Icon type="minus-circle"/>移除
                                  </div>  
                              </div>
                          ))} 
                          <Button type="dashed" block  onClick={() =>store.ranchercmp.push({"k":"","v":""})}>
                                <i type="plus">添加配置映射值</i>
                          </Button>
                    </Card>
                </Form.Item>


              </Form>
        </Modal>
    )
  }
}
export default Form.create()(CmpForm)
