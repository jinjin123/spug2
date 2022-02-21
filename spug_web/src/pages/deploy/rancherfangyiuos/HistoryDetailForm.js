/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, Checkbox, Row, Col, message, Button,Tooltip,Icon} from 'antd';
import http from 'libs/http';
// import request from 'libs/request';
import store from './store';
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
import styles from './form.module.css';
// import './form.css';
import CodeMirrorWrapper from "./CodeMirrorWrapper";
import { Controlled as CodeMirror } from "react-codemirror2";
import { fullicon } from 'layout'
import index from 'pages/welcome/index';
window.jsyaml = require('js-yaml')
@observer
class HistorDetailForm extends React.Component {
  constructor(props) {
    super(props);
    this.isModify = store.record.id !== undefined;
    this.state = {
      loading: false,
      envs: this.isModify ? [store.record.env_id] : [],
      full: false,
      // configMap_v: [],
      fullmode:[],
      fullmode_flag: 0
    }
  }


  // handleSubmit = () => {
  //   console.log(store.configMap)
  //   this.setState({ loading: true });
  //   const formData = this.props.form.getFieldsValue();
  //   formData['old_id'] = store.record.id;
  //   formData['envs'] = this.state.envs;
  //   if(this.isModify){
  //     http.put('/api/config/rsconfig/', formData)
  //     .then(res => {
  //       message.success('操作成功');
  //       store.formVisible = false;
  //       store.fetchRecords()
  //     }, () => this.setState({ loading: false }))
      
  //   }else{
  //     http.post('/api/config/rsconfig/', formData)
  //     .then(res => {
  //       message.success('操作成功');
  //       store.formVisible = false;
  //       store.fetchRecords()
  //     }, () => this.setState({ loading: false }))
  //   }
  // };

  handleEnvCheck = (id) => {
    if (!this.isModify) {
      const index = this.state.envs.indexOf(id);
      if (index !== -1) {
        this.state.envs.splice(index, 1);
      } else {
        this.state.envs.push(id);
      }
      this.setState({ envs: this.state.envs })
    }
  };
  handlePjTips = e => {
    store.pjtip = store.pjtips.filter(item=>item.toLowerCase().includes((e.target.value).toLowerCase())).join(",")
  }

  handleNsTips = e => {
    store.nstip = store.nstips.filter(item=>item.toLowerCase().includes((e.target.value).toLowerCase())).join(",")
  }
  handleChange = (index,...value) => {
    store.configMap[index]["v"] = value[3]
    // console.log(index,value)
    // this.setState({
    //   confingMap_v : this.state.configMap_v[index] = value[3]
    // })
  };
  handleFullmode = (index,status) => {
    //  console.log(index,status)
    store.showFullMode(index,status)
  }
  render() {
    const info = store.historytmpdetail;
    const codeRead = store.codeRead;
    // const {fullmode,fullmode_flag} = this.state;
    const fullmode = store.fullmode;
    const { getFieldDecorator } = this.props.form;
    const { value, onChange } = this.props;
    return (
      <Modal
        visible
        width={800}
        style={{ float: 'right', top: 0 }}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={"历史版本查看"}
        onCancel={() => {store.historyDetailVisible = false}}
        confirmLoading={this.state.loading}
        onOk={() => {store.historyDetailVisible = false}}>
        <Form labelCol={{ span: 2 }} wrapperCol={{ span: 20 }}>
          <Form.Item label="顶级项目">
              {getFieldDecorator('top_project', { initialValue: info['top_project'] })(
                // <Input disabled={this.isModify} placeholder="" onChange={e => store.pjtips = e.target.value}/>
                <Input disabled placeholder="" />
              )}
            
          </Form.Item>
          <Form.Item label="所属项目">
              {getFieldDecorator('pjname', { initialValue: info['pjname'] })(
                // <Input disabled={this.isModify} placeholder="" onChange={e => store.pjtips = e.target.value}/>
                <Input disabled placeholder="" />
              )}
            
          </Form.Item>
          <Form.Item label="命名空间">
            {getFieldDecorator('nsname', { initialValue: info['nsname'] })(
              <Input disabled placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="应用名">
            {getFieldDecorator('dpname', { initialValue: info['dpname'] })(
              <Input disabled placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="镜像">
            {getFieldDecorator('img', { initialValue: info['img'] })(
              <Input disabled placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="副本">
            {getFieldDecorator('replica', { initialValue: info['replica'] })(
              <Input disabled placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="配置文件">
            {getFieldDecorator('configName', { initialValue: info['configName'] })(
              <Input disabled placeholder="" />
            )}
          </Form.Item>

          <Form.Item label={"配置详情"}>
              {info["configMap"].length >0 ?
                info["configMap"].map((item,index)=> (
                  <div key={index}  style={{marginBottom: 30, position: 'relative'}} >
                  <Form.Item required label={`Key${index+1}`} >
                      <Input value={item["k"]} disabled placeholder="请输入" />
                  </Form.Item>
                  <Form.Item  required label="Value">
                      <Button size="small" className={styles.fullscreen} onClick={this.handleFullmode.bind(this,index,true)}><img src={fullicon} /></Button>
                      <CodeMirror
                        // onBeforeChange={this.handleChange.bind(this,index,value)}
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
                          readOnly: false
                        }}
                      />
                  </Form.Item>
                </div>
              )) 
            :null}
          </Form.Item>  
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(HistorDetailForm)
