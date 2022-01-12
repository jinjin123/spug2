/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Button,Radio,Select,Card,Icon,Tag} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import  styles from "./index.module.css";
import 'codemirror/lib/codemirror.js';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/yaml/yaml.js';
import 'codemirror/theme/monokai.css';
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/match-highlighter.js'
import 'codemirror/addon/search/jump-to-line.js'

import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/search.js'
// 折叠
import 'codemirror/addon/fold/foldcode.js';  // 代码折叠
import 'codemirror/addon/fold/foldgutter.js'; // 代码折叠
import 'codemirror/addon/fold/brace-fold.js'; // 代码折叠
import 'codemirror/addon/fold/comment-fold.js'; // 代码折叠
import 'codemirror/addon/lint/lint.js';  // 错误校验
import 'codemirror/addon/lint/javascript-lint.js';  // js错误校验
import 'codemirror/addon/lint/yaml-lint.js';
import 'codemirror/addon/selection/active-line.js';  // 当前行高亮
import 'codemirror/addon/lint/lint.css'  // 代码错误提示

import 'codemirror/addon/display/fullscreen.css';
import 'codemirror/addon/display/fullscreen.js';
import { Controlled as CodeMirror } from "react-codemirror2";
import { fullicon } from 'layout'
import index from 'pages/welcome/index';
window.jsyaml = require('js-yaml')
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
        fullmode:[],
        fullmode_flag: 0,
        moreAction: [{"id":0,"v":"添加卷..."}],
        choosens: {},
        tmpnsV: null,
        newNs: null,

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
  handleFullmode = (index,status) => {
    // console.log(index,status)
    store.showFullMode(index,status)
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
    const tmp = {}
    
    store.ranchercmp.map((item,index)=>(
      // tmp['"' + item['k'] + '"']= item["v"]
      tmp[item['k']]= item["v"]
    ))
    formData["namespaceId"] = this.state.tmpnsV
    formData["newNs"] = this.state.newNs

    formData["data"] = tmp
    formData["dbdata"] =  store.ranchercmp
    formData["type"] = "configMap"
    formData["labels"] = {}
    http.post('/api/app/deploy/cmapop/', {"data":formData,"env":2,"tag":"ioc"})
    .then(() => {
        message.success('操作成功');
        store.cmpForm = false;
        store.fetchRecords()
      
    }, () => this.setState({loading: false}))
    console.log(formData)
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
  handleChange = (index,...value) => {
    // console.log(index)
    store.cmaprecord["configMap"][index]["v"] = value[3]
    // console.log(value[3])
  };
  handleNewEditChange = (index,...value) => {
    // console.log(index)
    store.ranchercmp[index]["v"] = value[3]
    // console.log(value[3])
  };
  onCallNsChange = e => {
    if (e.target.value === 1) {
      this.setState({
        choosens: { "tag": "select" },
      });
    } else {
      this.setState({
        choosens: { "tag": "input" },
      });
    }
  }
  render() {
    const info = store.cmaprecord;
    const {value} = this.state;
    const {input_value} = this.state;
    const { Option } = Select;
    const {getFieldDecorator} = this.props.form;
    const fullmode = store.fullmode;
    const codeRead = store.codeRead;


    return (
        <Modal
        visible
        width={1100}
        style={{ float: 'right',top: 0}}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.cmaprecord.id ? '编辑配置映射' : '添加配置映射'}
        onCancel={() => (store.cmpForm = false,store.cmaprecord={})}
        onOk={this.handleSubmit}
        >
          <Form  layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称"  rules={[{ required: true, message: '必填名' }]}>
                  {getFieldDecorator('name',{initialValue: info['configName']})(
                    <Input placeholder="e.g. myapp" style={{ width: 200, marginLeft: 10 }}/>
                  )}
              </Form.Item>

                <Form.Item required label="rancher项目" rules={[{ required: true, message: '必填项目' }]}>
                    {getFieldDecorator('pjname',{initialValue:info['pjname']} )(
                      (info.id ?
                        <Select onChange={v=> this.onRjChange(v)} style={{ width: 200 }} >
                        {store.rancherpj.map((item,index)=>(
                            <Option key={item} value={item}>{item}</Option>
                        ))}
                        </Select>
                      :
                      <Select  onChange={v=> this.onRjChange(v)} style={{ width: 200 }} >
                      {store.rancherpj.map((item,index)=>(
                          <Option key={item} value={item}>{item}</Option>
                      ))}
                      </Select>
                      )
                    )}
                </Form.Item>

                <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                      {getFieldDecorator('namespaceId',{initialValue:info['nsname']} )(
                        <Radio.Group  onChange={this.onCallNsChange} >
                          <Radio value={1}>使用现有：
                            { this.state.choosens["tag"] == "select"
                            ?
                              <Select   
                              onChange={v => { this.setState({ tmpnsV: v, newNs: false }) }} 
                              style={{ width: 150 }} >
                                {this.state.tmpns.map((item,index)=>(
                                    <Option key={index} value={item}>{item}</Option>
                                ))} 
                                </Select>
                            :  
                                null
                            }
                            </Radio>
                            <Radio value={2}>创建命名空间：
                                {this.state.choosens["tag"] == "input"
                                  ?
                                  <Input defaultValue={info.nsname} onChange={e => { this.setState({ tmpnsV: e.target.value, newNs: true }) }} placeholder="namespace" style={{ width: 150, marginLeft: 10 }} />
                                  : null
                                }
                              </Radio>
                          </Radio.Group>
                        
                    )}
                </Form.Item>
                <Form.Item required label="配置映射" >
                    <Card title="配置映射" style={{ width: 1000 }}>
                        {info.id ?
                          info["configMap"].map((item,index)=>(
                            <div className={"cmpeditor"} key={index} style={{ padding:10,display: "flex"}}>
                              <Input value={item["k"]} onChange={e => item['k'] = e.target.value} style={{ width:350, marginRight: 10 }} placeholder="请输入" />
                              <Tag style={{ height:32}}>=</Tag>

                              <Button size="small" className={styles.fullscreen} onClick={this.handleFullmode.bind(this,index,true)}><img src={fullicon} /></Button>
                              <CodeMirror
                                  onBeforeChange={this.handleChange.bind(this,index,value)}
                                  value={item["v"]}
                                  options={{
                                    mode: 'text/yaml',
                                    theme: 'monokai',
                                    smartIndent: true,
                                    foldGutter: true,
                                    lineWrapping: true,
                                    gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter', 'CodeMirror-lint-markers'],
                                    matchBrackets: true,
                                    lineNumbers: true,
                                    lint: true,
                                    styleActiveLine: true,          // 选中行高亮
                                    indentUnit: 4,
                                    fullScreen: fullmode[index],
                                    readOnly: codeRead
                                  }}
                                />
                                  <div style={{width:50}}  onClick={() => {info["configMap"].splice(index,1);fullmode.splice(index,1)}}>
                                    <Icon type="minus-circle"/>移除
                                  </div>  
                            </div>
                          ))
                        :
                            store.ranchercmp.map((item,index) => (
                              <div key={index} style={{ padding:10,display: "flex"}}>
                                <Input value={item["k"]} onChange={e => item['k'] = e.target.value} style={{ width:350, marginRight: 10 }} placeholder="请输入" />
                                <Tag style={{ height:32}}>=</Tag>
                                <Button size="small" className={styles.fullscreen} onClick={this.handleFullmode.bind(this,index,true)}><img src={fullicon} /></Button>

                                <CodeMirror
                                  onBeforeChange={this.handleNewEditChange.bind(this,index,value)}
                                  value={item["v"]}
                                  options={{
                                    mode: 'text/yaml',
                                    theme: 'monokai',
                                    smartIndent: true,
                                    foldGutter: true,
                                    lineWrapping: true,
                                    gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter', 'CodeMirror-lint-markers'],
                                    matchBrackets: true,
                                    lineNumbers: true,
                                    lint: true,
                                    styleActiveLine: true,          // 选中行高亮
                                    indentUnit: 4,
                                    fullScreen: fullmode[index],
                                    readOnly: codeRead
                                  }}
                                />
                                <div style={{width:50}} onClick={() => {store.ranchercmp.splice(index,1);fullmode.splice(index,1)}}>
                                  <Icon type="minus-circle"/>移除
                                </div>  
                              </div>
                            ))                          
                        }
                        {info.id ?
                            <Button type="dashed" block  onClick={() =>{info["configMap"].push({"k":"","v":"占位填充，需要自行删除------------------------------------------>"});fullmode.push(false)}}>
                            <i type="plus">添加配置映射值</i>
                            </Button>
                          :                            
                            <Button type="dashed" block  onClick={() =>{store.ranchercmp.push({"k":"","v":"占位填充，需要自行删除------------------------------------------>"});fullmode.push(false)}}>
                                <i type="plus">添加配置映射值</i>
                            </Button>
                        }
                    </Card>
                </Form.Item>
              </Form>
        </Modal>
    )
  }
}
export default Form.create()(CmpForm)
