/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Button,InputNumber,Select,Tag} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import  styles from "./index.module.css";
@observer
class PvcForm extends React.Component {
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
  onCallHostClick = e => {
    switch(e){
      case 0:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 1 ? item["itemdata"].push({"itemk":"","itemtype":"=","itemv":""}): null
        ))}
        break;;
      case 1:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 2 ? item["itemdata"].push({"itemk":"","itemtype":"=","itemv":""}): null
        ))}
        break;;
      case 2:
        {store.rancherCallhost.map((item)=>(
          item["itemid"] === 3 ? item["itemdata"].push({"itemk":"","itemtype":"=","itemv":""}): null
        ))}
        break;;
    }
    console.log(e)
  }
  
  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    formData["mode"] = 666
    console.log(formData)
  };

  onVolumeChange = (action) => {
    switch(action){
      case "host":
        store.rancherVolume.push({"k":"映射主机目录" })
        this.setState({
          moreAction : [{"id": 1,"v":"映射主机目录"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
      case "oldpvc":
        store.rancherVolume.push({"k":"使用现有的PVC" })
        this.setState({
          moreAction : [{"id": 2,"v":"使用现有的PVC"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
      case "newpvc":
          store.rancherVolume.push({"k":"添加新的PVC" })
          this.setState({
            moreAction : [{"id": 3,"v":"使用新的的PVC"}]
          })
          setTimeout(() => {
            this.setState({
              moreAction : "添加卷..."
            })
          },500)
          break;
      case "config":
        store.rancherVolume.push({"k":"配置映射卷"})
        this.setState({
          moreAction : [{"id": 4,"v":"配置映射卷"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
    }
  }
  
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
  onRadioInputChange = e => {
    this.setState({
      input_value: e.target.value,
    });
  };
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
        title={'添加PVC'}
        onCancel={() => store.pvcForm = false}
        onOk={this.handleSubmit}
        >
          <Form  layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称"  rules={[{ required: true, message: '必填volume名' }]}>
                  {getFieldDecorator('pvcname')(
                    <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                  )}
              </Form.Item>

                <Form.Item required label="rancher项目" rules={[{ required: true, message: '必填项目' }]}>
                    {getFieldDecorator('pjname')(
                      <Select  onChange={v=> this.onRjChange(v)} style={{ width: 200 }} >
                          {store.rancherpj.map((item,index)=>(
                              <Option key={item} value={item}>{item}</Option>
                            
                          ))}
                      </Select>
                    )}
                </Form.Item>

                <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                    {getFieldDecorator('nsname')(
                      <Select   style={{ width: 300 }} >
                          {this.state.tmpns.map((item,index)=>(
                              <Option key={index} value={item}>{item}</Option>
                            
                          ))}
                      </Select>
                    )}
                </Form.Item>
                <Form.Item required label="存储类型(Storage Class)" rules={[{ required: true, message: '必填type' }]}>
                    {getFieldDecorator('vtype')(
                      <Select  style={{ width: 400 }} >
                          <Option value={0}>{"使用默认 storage class"}</Option>
                          <Option value={1}>{"managed-nfs-50-128-storage"}</Option>
                          {this.state.pvctype.map((item,index)=>(
                              <Option key={item} value={item}>{item}</Option>
                            
                          ))}
                      </Select>
                    )}
                </Form.Item>
                <Form.Item required label="容量"  rules={[{ required: true, message: '必填size' }]}>
                  <div style={{display: "flex"}}>
                    {getFieldDecorator('pvcsize')(
                      <InputNumber  style={{ width: 410, marginLeft: 10 }}/>
                    )}
                    <Tag style={{ height:32}}>GiB</Tag>
                  </div>
                </Form.Item>
                <Form.Item required label="访问模式" >
                    <Checkbox defaultChecked disabled> 多主机读写模式</Checkbox>
                </Form.Item>
              </Form>
        </Modal>
    )
  }
}
export default Form.create()(PvcForm)
