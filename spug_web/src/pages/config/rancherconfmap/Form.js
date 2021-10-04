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
import envStore from '../environment/store'
import './form.css';
import CodeMirrorWrapper from "./CodeMirrorWrapper";
import { Controlled as CodeMirror } from "react-codemirror2";
import { fullicon } from 'layout'
import index from 'pages/welcome/index';
window.jsyaml = require('js-yaml')
@observer
class ComForm extends React.Component {
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


  handleSubmit = () => {
    console.log(store.configMap)
    this.setState({ loading: true });
    const formData = this.props.form.getFieldsValue();
    formData['old_id'] = store.record.id;
    formData['envs'] = this.state.envs;
    if(this.isModify){
      http.put('/api/config/rsconfig/', formData)
      .then(res => {
        message.success('操作成功');
        store.formVisible = false;
        store.fetchRecords()
      }, () => this.setState({ loading: false }))
      
    }else{
      http.post('/api/config/rsconfig/', formData)
      .then(res => {
        message.success('操作成功');
        store.formVisible = false;
        store.fetchRecords()
      }, () => this.setState({ loading: false }))
    }
  };

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
    const info = store.record;
    const codeRead = store.codeRead;
    const { envs } = this.state;
    // const {fullmode,fullmode_flag} = this.state;
    // console.log(fullmode)、
    const fullmode = store.fullmode;
    const { getFieldDecorator } = this.props.form;
    const configMap = store.configMap;
    const { value, onChange } = this.props;
    return (
      <Modal
        visible
        width={800}
        style={{ float: 'right', top: 0 }}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.record.id ? '更新配置' : '新增配置'}
        onCancel={() => {store.formVisible = false;store.configMap =[]}}
        confirmLoading={this.state.loading}
        onOk={this.handleSubmit}>
        <Form labelCol={{ span: 2 }} wrapperCol={{ span: 20 }}>
          {configMap.map((item,index)=>(
            <div key={index}  style={{marginBottom: 30, position: 'relative'}} >
              <Form.Item required label={`Key${index+1}`} >
                  <Input value={item["k"]} onChange={e => item['k'] = e.target.value} placeholder="请输入" />
              </Form.Item>
              <Form.Item  required label="Value">
                  <Button size="small" className={styles.fullscreen} onClick={this.handleFullmode.bind(this,index,true)}><img src={fullicon} /></Button>
                  {/* {this.props.form.getFieldDecorator('configMap_v', { initialValue: item['configMap_v'] })( */}
                  <CodeMirror
                    onBeforeChange={this.handleChange.bind(this,index,value)}
                    // onChange={(editor, metadata, value) => {
                    //   // final value, no need to setState here
                    //   console.log(value)
                    // }}
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
                  {/* )} */}
              </Form.Item>
              <div className={styles.delAction} onClick={() => configMap.splice(index, 1)}>
                <Icon type="minus-circle"/>移除
              </div>
            </div>
          ))}
          {/* <Form.Item required label="Key">
              {getFieldDecorator('configMap_k', { initialValue: info['configMap_k'] })(
                <Input disabled={this.isModify} placeholder="" />
              )}
          </Form.Item>
          <Form.Item required label="Value">
            <Button size="small" className={styles.fullscreen} onClick={() => store.showFullMode(true)}><img src={fullicon} /></Button>
            {this.props.form.getFieldDecorator('configMap_v', { initialValue: info['configMap_v'] })(
              <CodeMirrorWrapper
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
                  fullScreen: fullmode,
                  readOnly: codeRead
                }}
              />
            )}
          </Form.Item> */}
          <Form.Item hidden={true}>
            {getFieldDecorator('configname', { initialValue: info['configname'] })(
              <Input disabled={true} placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="所属项目">
            <Tooltip title={store.pjtip} color={"black"} key={1}>
              {getFieldDecorator('project', { initialValue: info['project'] })(
                // <Input disabled={this.isModify} placeholder="" onChange={e => store.pjtips = e.target.value}/>
                <Input disabled={this.isModify} placeholder="" onChange={this.handlePjTips}/>
              )}
            </Tooltip>
          </Form.Item>
          <Form.Item label="命名空间">
            <Tooltip title={store.nstip} color={"black"} key={1}>
            {getFieldDecorator('namespace', { initialValue: info['namespace'] })(
              <Input disabled={this.isModify} placeholder=""onChange={this.handleNsTips} />
            )}
            </Tooltip>
          </Form.Item>
          <Form.Item label="配置文件">
            {getFieldDecorator('configname', { initialValue: info['configname'] })(
              <Input disabled={this.isModify} placeholder="" />
            )}
          </Form.Item>
          <Form.Item hidden={true}>
            {getFieldDecorator('configid', { initialValue: info['configid'] })(
              <Input disabled={true} placeholder="" />
            )}
          </Form.Item>
          <Form.Item hidden={true}>
            {getFieldDecorator('project_id', { initialValue: info['project_id'] })(
              <Input disabled={true} placeholder="" />
            )}
          </Form.Item>
          <Form.Item label="选择环境">
            {envStore.records.map((item, index) => (
              <Row
                key={item.id}
                onClick={() => this.handleEnvCheck(item.id)}
                style={{ cursor: 'pointer', borderTop: index ? '1px solid #e8e8e8' : '' }}>
                <Col span={2}><Checkbox disabled={this.isModify} checked={envs.includes(item.id)} /></Col>
                <Col span={4} className={styles.ellipsis}>{item.key}</Col>
                <Col span={9} className={styles.ellipsis}>{item.name}</Col>
                <Col span={9} className={styles.ellipsis}>{item.desc}</Col>
              </Row>
            ))}
          </Form.Item>
          {(
          <Form.Item wrapperCol={{span: 14, offset: 6}}>
            <Button  type="dashed" block onClick={() => {configMap.push({});fullmode.push(false)}}>
              <Icon type="plus"/>添加key:value
            </Button>
          </Form.Item>
        )}
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
